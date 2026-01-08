# /// script
# dependencies = [
#   "pexpect",
#   "tqdm"
# ]
# ///

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Find OpenCorpora (OC) wordforms missing from lang-rus HFST analyser.

Input format (dict.opcorpora.txt):
- Lexemes start with a numeric ID on its own line.
- Followed by wordform lines:  WORD<TAB/SPACE>TAGSTRING
- Lexemes are separated by a blank line.

For each wordform, the script:
- converts it to title case,
- runs `hfst-lookup` against a lang-rus analyser (.hfstol),
- considers the wordform missing if:
  - hfst-lookup returns only `+?` analyses, or
  - none of the analyses contain tags aligning with OC tags (best-effort mapping).

If any wordforms in a lexeme are missing, the lexeme is stored in a nested dict:

Outer key (tuple):
  (INVARIANT_TAGS, INFLECTION_TAGS_FORM_1, INFLECTION_TAGS_FORM_2, ...)
Where INVARIANT_TAGS is a tuple like ('NOUN','anim','masc'), and each
INFLECTION_TAGS_FORM_i is a tuple like ('sing','nomn').

Inner key (tuple):
  (ENDING_1, ENDING_2, ...)
Value:
  [STEM_1, STEM_2, ...]

Because JSON keys must be strings, both tuple keys are serialized using `repr()`.
They can be round-tripped with `ast.literal_eval()`.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
from pathlib import Path
import pexpect
import sys
import time
from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Sequence, Tuple

from tqdm import tqdm


# --- Tag mapping (OC -> tags commonly seen in lang-rus outputs) ------------

_OC_TO_GIELLA = {
	# POS
	"NOUN": "N",
	"ADJF": "A",
	"ADJS": "A",
	"VERB": "V",
	"INFN": "V",
	"PRTF": "V",
	"PRTS": "V",
	"GRND": "V",
	"NUMR": "Num",
	"ADVB": "Adv",
	"NPRO": "Pron",
	"PREP": "Pr",
	"CONJ": "CC",
	"PRCL": "Part",
	"INTJ": "Interj",

	# Gender
	"masc": "Msc",
	"femn": "Fem",
	"neut": "Neu",

	# Animacy
	"anim": "Anim",
	"inan": "Inan",

	# Number
	"sing": "Sg",
	"plur": "Pl",

	# Case
	"nomn": "Nom",
	"gent": "Gen",
	"datv": "Dat",
	"accs": "Acc",
	"ablt": "Ins",
	"loct": "Loc",

	# Aspect / transitivity (best-effort)
	"perf": "Perf",
	"impf": "Impf",
	"tran": "TV",
	"intr": "IV",
}


def _title_case(surface: str) -> str:
	if not surface:
		return surface
	# OC surfaces are usually ALLCAPS; we want “Ёж”, not “ЁЖ”.
	if surface == surface.upper():
		return surface[:1].upper() + surface[1:].lower()
	return surface.title()


def _longest_common_prefix(strings: Sequence[str]) -> str:
	if not strings:
		return ""
	prefix = strings[0]
	for s in strings[1:]:
		limit = min(len(prefix), len(s))
		i = 0
		while i < limit and prefix[i] == s[i]:
			i += 1
		prefix = prefix[:i]
		if not prefix:
			break
	return prefix


def _tuple_key(obj: object) -> str:
	return repr(obj)


def _find_repo_root(start: Path) -> Path:
	"""Best-effort find the lang-rus repo root from a starting path."""
	for p in [start] + list(start.parents):
		if (p / "configure.ac").exists() and (p / "src").is_dir():
			return p
		if (p / "src" / "fst").is_dir() and (p / "README.md").exists():
			return p
	return Path.cwd()


# --- OC parsing ------------------------------------------------------------


_WORD_LINE_RE = re.compile(r"^(?P<form>\S+)\s+(?P<tags>.+?)\s*$")


@dataclass(frozen=True)
class OCForm:
	surface_raw: str
	surface_title: str
	invariant_tags: Tuple[str, ...]
	infl_tags: Tuple[str, ...]


@dataclass
class OCLexeme:
	lexeme_id: str
	forms: List[OCForm]


def iter_oc_lexemes(path: str) -> Iterator[OCLexeme]:
	"""Yield lexemes from a dict.opcorpora.txt-like file, streaming line-by-line."""

	def flush(current_id: Optional[str], current_forms: List[OCForm]) -> Optional[OCLexeme]:
		if current_id is None or not current_forms:
			return None
		return OCLexeme(lexeme_id=current_id, forms=current_forms)

	current_id: Optional[str] = None
	current_forms: List[OCForm] = []

	with open(path, "r", encoding="utf-8", errors="replace") as f:
		for raw_line in f:
			line = raw_line.rstrip("\n")
			stripped = line.strip()

			if not stripped:
				lex = flush(current_id, current_forms)
				if lex is not None:
					yield lex
				current_id = None
				current_forms = []
				continue

			if stripped.isdigit():
				lex = flush(current_id, current_forms)
				if lex is not None:
					yield lex
				current_id = stripped
				current_forms = []
				continue

			if current_id is None:
				continue

			m = _WORD_LINE_RE.match(line)
			if not m:
				continue

			surface = m.group("form")
			tag_str = m.group("tags").strip()
			tag_parts = tag_str.split()
			if not tag_parts:
				continue

			invariant = tuple(t for t in tag_parts[0].split(",") if t)
			if len(tag_parts) == 1:
				infl: Tuple[str, ...] = ()
			else:
				infl = tuple(t for part in tag_parts[1:] for t in part.split(",") if t)

			current_forms.append(
				OCForm(
					surface_raw=surface,
					surface_title=_title_case(surface),
					invariant_tags=invariant,
					infl_tags=infl,
				)
			)

	lex = flush(current_id, current_forms)
	if lex is not None:
		yield lex


def iter_oc_lexemes_with_pos(path: str) -> Iterator[Tuple[OCLexeme, int]]:
	"""Yield (lexeme, byte_offset) from a dict.opcorpora.txt-like file.

	The byte_offset is `file.tell()` at the point the lexeme is yielded.
	"""

	def flush(current_id: Optional[str], current_forms: List[OCForm]) -> Optional[OCLexeme]:
		if current_id is None or not current_forms:
			return None
		return OCLexeme(lexeme_id=current_id, forms=current_forms)

	current_id: Optional[str] = None
	current_forms: List[OCForm] = []

	with open(path, "r", encoding="utf-8", errors="replace") as f:
		while True:
			pos_before = f.tell()
			raw_line = f.readline()
			if not raw_line:
				break
			line = raw_line.rstrip("\n")
			stripped = line.strip()

			if not stripped:
				lex = flush(current_id, current_forms)
				if lex is not None:
					yield (lex, pos_before)
				current_id = None
				current_forms = []
				continue

			if stripped.isdigit():
				lex = flush(current_id, current_forms)
				if lex is not None:
					yield (lex, pos_before)
				current_id = stripped
				current_forms = []
				continue

			if current_id is None:
				continue

			m = _WORD_LINE_RE.match(line)
			if not m:
				continue

			surface = m.group("form")
			tag_str = m.group("tags").strip()
			tag_parts = tag_str.split()
			if not tag_parts:
				continue

			invariant = tuple(t for t in tag_parts[0].split(",") if t)
			if len(tag_parts) == 1:
				infl: Tuple[str, ...] = ()
			else:
				infl = tuple(t for part in tag_parts[1:] for t in part.split(",") if t)

			current_forms.append(
				OCForm(
					surface_raw=surface,
					surface_title=_title_case(surface),
					invariant_tags=invariant,
					infl_tags=infl,
				)
			)

	lex = flush(current_id, current_forms)
	if lex is not None:
		yield (lex, os.path.getsize(path))


# --- HFST lookup -----------------------------------------------------------


class HFSTLookup:
	"""Persistent hfst-lookup session.

	hfst-lookup is interactive and prints a "> " prompt. We read output
	incrementally until the prompt to delimit responses.
	"""


	def __init__(self, analyser_path: str) -> None:
		self.analyser_path = analyser_path
		self._proc: Optional[pexpect.spawn] = None

	def __enter__(self) -> "HFSTLookup":
		sys.stderr.write(f"[DEBUG] Starting hfst-lookup (pexpect): {self.analyser_path}\n")
		sys.stderr.flush()
		self._proc = pexpect.spawn(f"hfst-lookup {self.analyser_path}", encoding="utf-8", timeout=30)
		self._proc.expect("> ")
		sys.stderr.write("[DEBUG] hfst-lookup prompt received.\n")
		sys.stderr.flush()
		return self

	def __exit__(self, exc_type, exc, tb) -> None:
		if self._proc is not None:
			self._proc.terminate(force=True)

	def lookup(self, surface: str) -> List[str]:
		if self._proc is None:
			raise RuntimeError("HFSTLookup not started")
		self._proc.sendline(surface)
		self._proc.expect("> ")
		# pexpect.before contains everything up to the prompt, including the command just sent
		# The first line is the echoed input, the rest is output
		lines = self._proc.before.splitlines()
		# Remove the echoed input line
		if lines and lines[0].strip() == surface.strip():
			lines = lines[1:]
		return [ln for ln in lines if ln.strip()]


class LRUCache:
	def __init__(self, max_size: int) -> None:
		self.max_size = max_size
		self._data: "collections.OrderedDict[str, List[str]]" = collections.OrderedDict()

	def get(self, key: str) -> Optional[List[str]]:
		if key not in self._data:
			return None
		self._data.move_to_end(key)
		return self._data[key]

	def put(self, key: str, value: List[str]) -> None:
		self._data[key] = value
		self._data.move_to_end(key)
		if len(self._data) > self.max_size:
			self._data.popitem(last=False)


# --- Alignment -------------------------------------------------------------


def _extract_analysis_strings(lookup_lines: Sequence[str]) -> List[str]:
	analyses: List[str] = []
	for ln in lookup_lines:
		parts = ln.split("\t")
		if len(parts) >= 2:
			analyses.append(parts[1].strip())
		else:
			analyses.append(ln.strip())
	return analyses


def _is_unknown_analysis(analysis: str) -> bool:
	return "+?" in analysis


def _tokenize_analysis(analysis: str) -> List[str]:
	# Typical analyser output: lemma+N+Msc+Anim+Sg+Nom
	return [t for t in analysis.replace("^", "").replace("$", "").split("+") if t]


def _mapped_expected_tags(oc_invariant: Tuple[str, ...], oc_inflection: Tuple[str, ...]) -> List[str]:
	expected: List[str] = []
	for t in list(oc_invariant) + list(oc_inflection):
		mapped = _OC_TO_GIELLA.get(t)
		if mapped:
			expected.append(mapped)
	return expected


def analysis_aligns_with_oc(
	lookup_lines: Sequence[str],
	oc_invariant: Tuple[str, ...],
	oc_inflection: Tuple[str, ...],
) -> bool:
	analyses = _extract_analysis_strings(lookup_lines)
	if not analyses:
		return False

	expected = _mapped_expected_tags(oc_invariant, oc_inflection)

	# If we can't map tags, treat anything other than +? as “found”.
	if not expected:
		return any(not _is_unknown_analysis(a) for a in analyses)

	for a in analyses:
		if _is_unknown_analysis(a):
			continue
		tokens = set(_tokenize_analysis(a))
		if all(tag in tokens for tag in expected):
			return True
	return False


# --- Main ------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
	script_path = Path(__file__).resolve()
	script_dir = script_path.parent
	repo_root = _find_repo_root(script_dir)

	parser = argparse.ArgumentParser(
		description="Parse OpenCorpora dict and find forms missing from lang-rus analyser"
	)
	parser.add_argument(
		"--oc",
		default=str(script_dir / "dict.opcorpora.txt"),
		help="Path to dict.opcorpora.txt",
	)
	parser.add_argument(
		"--analyser",
		default=str(repo_root / "src" / "fst" / "analyser-gt-desc.hfstol"),
		help="Path to analyser .hfstol (for hfst-lookup)",
	)
	parser.add_argument(
		"--out",
		default="missing_from_OC.json",
		help="Output JSON path",
	)
	parser.add_argument(
		"--limit-lexemes",
		type=int,
		default=0,
		help="Stop after N lexemes (0 = no limit)",
	)
	parser.add_argument(
		"--cache-size",
		type=int,
		default=200000,
		help="LRU cache size for hfst-lookup surfaces",
	)
	parser.add_argument(
		"--skip-lookup",
		action="store_true",
		help="Only parse OC; do not run hfst-lookup (debugging)",
	)
	parser.add_argument(
		"--progress-seconds",
		type=float,
		default=10.0,
		help="Print progress every N seconds (0 disables time-based progress)",
	)
	parser.add_argument(
		"--progress-lexemes",
		type=int,
		default=5000,
		help="Print progress every N lexemes (0 disables lexeme-based progress)",
	)
	args = parser.parse_args(argv)

	if not os.path.exists(args.oc):
		sys.stderr.write(f"ERROR: OC dict not found: {args.oc}\n")
		return 2

	if not args.skip_lookup and not os.path.exists(args.analyser):
		sys.stderr.write(
			f"ERROR: analyser transducer not found: {args.analyser}\n"
			"Build it first, or pass --analyser PATH.\n"
		)
		return 2


	missing: Dict[str, Dict[str, List[str]]] = {}
	cache = LRUCache(max_size=max(0, args.cache_size))
	total_bytes = os.path.getsize(args.oc)

	# Count total lexemes for tqdm
	sys.stderr.write("[DEBUG] Counting total lexemes for progress bar...\n")
	sys.stderr.flush()
	total_lexemes = 0
	for _, _ in iter_oc_lexemes_with_pos(args.oc):
		total_lexemes += 1
		if args.limit_lexemes and total_lexemes >= args.limit_lexemes:
			break

	processed_lexemes = 0
	stored_lexemes = 0

	if args.skip_lookup:
		with tqdm(total=total_lexemes, desc="Lexemes", unit="lex") as pbar:
			for lex, pos in iter_oc_lexemes_with_pos(args.oc):
				processed_lexemes += 1
				if args.limit_lexemes and processed_lexemes > args.limit_lexemes:
					break
				pbar.update(1)

		with open(args.out, "w", encoding="utf-8") as out_f:
			json.dump(missing, out_f, ensure_ascii=False, indent=2)
		sys.stderr.write(f"Parsed {processed_lexemes} lexemes (skip-lookup). Wrote {args.out}\n")
		return 0

	def get_lookup_lines(lookup: HFSTLookup, surface: str) -> List[str]:
		if cache.max_size > 0:
			cached = cache.get(surface)
			if cached is not None:
				return cached
		lines = lookup.lookup(surface)
		if cache.max_size > 0:
			cache.put(surface, lines)
		return lines

	sys.stderr.write(f"[DEBUG] Entering HFSTLookup context with analyser: {args.analyser}\n")
	sys.stderr.flush()
	with HFSTLookup(args.analyser) as lookup, tqdm(total=total_lexemes, desc="Lexemes", unit="lex") as pbar:
		for lex, pos in iter_oc_lexemes_with_pos(args.oc):
			processed_lexemes += 1
			if args.limit_lexemes and processed_lexemes > args.limit_lexemes:
				break

			if not lex.forms:
				pbar.update(1)
				continue

			invariant = lex.forms[0].invariant_tags
			inflections = tuple(f.infl_tags for f in lex.forms)
			outer_key = _tuple_key((invariant,) + inflections)

			title_forms = [f.surface_title for f in lex.forms]
			stem = _longest_common_prefix(title_forms)
			endings = tuple(tf[len(stem) :] for tf in title_forms)
			inner_key = _tuple_key(endings)

			any_missing = False
			for f in lex.forms:
				lookup_lines = get_lookup_lines(lookup, f.surface_title)
				if not analysis_aligns_with_oc(lookup_lines, f.invariant_tags, f.infl_tags):
					any_missing = True
					break

			if any_missing:
				missing.setdefault(outer_key, {}).setdefault(inner_key, []).append(stem)
				stored_lexemes += 1
			pbar.update(1)

	with open(args.out, "w", encoding="utf-8") as out_f:
		json.dump(missing, out_f, ensure_ascii=False, indent=2)

	sys.stderr.write(
		f"Done. Processed {processed_lexemes} lexemes; stored {stored_lexemes}.\n"
		f"Wrote {args.out}\n"
	)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
