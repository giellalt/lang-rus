#!/usr/bin/env python3
import sys
import re
from collections import defaultdict
from tqdm import tqdm

# Files
MISSING_FILE = "google_missing.txt"
FREQ_FILE = "googlebooks_freqlist.txt"
OUT_ADJ = "missing_adjectives.txt"
OUT_VERB = "missing_verbs.txt"
OUT_NOUN = "missing_nouns.txt"

# Regex for modern Russian alphabet (excluding punctuation, digits, latin)
# Strict interpretation: ^[а-яА-ЯёЁ]+$
RUSSIAN_WORD_RE = re.compile(r"^[а-яА-ЯёЁ]+$")

# Morphology Heuristics

# Adjectives
# Sort endings by length descending to match longest first.
adj_endings_list = [
    "ыми", "ими", "ого", "его", "ому", "ему", "ую", "юю", "ых", "их",
    "ая", "яя", "ое", "ее", "ые", "ие", "ый", "ий", "ой", "ым", "им", "ом", "ем"
]
ADJ_ENDINGS = "(" + "|".join(adj_endings_list) + ")$"
ADJ_RE = re.compile(ADJ_ENDINGS)

# Verbs
# Reflexive suffix
reflexive_list = ["ся", "сь"]
REFLEXIVE_RE = re.compile("(" + "|".join(reflexive_list) + ")$")

# Verb inflection
verb_endings_list = [
    "ешь", "ишь", "ете", "ите",
    "ет", "ит", "ут", "ют", "ат", "ят",
    "ем", "им",
    "ть", "ти", "чь",
    "ла", "ло", "ли", "л"
]
verb_endings_list.sort(key=len, reverse=True)
VERB_ENDINGS = "(" + "|".join(verb_endings_list) + ")$"
VERB_RE = re.compile(VERB_ENDINGS)

# Nouns
noun_endings_list = [
    "ами", "ями",
    "ом", "ем", "ов", "ев", "ей", "ам", "ям", "ах", "ях",
    "а", "я", "о", "е", "ы", "и", "у", "ю", "ь"
]
noun_endings_list.sort(key=len, reverse=True)
NOUN_ENDINGS = "(" + "|".join(noun_endings_list) + ")$"
NOUN_RE = re.compile(NOUN_ENDINGS)

def get_stem_adj(word):
    match = ADJ_RE.search(word)
    if match:
        return word[:match.start()]
    return word

def get_stem_verb(word):
    # Remove reflexive
    w = REFLEXIVE_RE.sub("", word)
    # Remove ending
    match = VERB_RE.search(w)
    if match:
        return w[:match.start()]
    return w

def get_stem_noun(word):
    match = NOUN_RE.search(word)
    if match:
        return word[:match.start()]
    return word

def classify_and_stem(word):
    # 1. Adjectives (Long forms)
    if ADJ_RE.search(word):
        return 'ADJ', get_stem_adj(word)

    # 2. Verbs
    # Check reflexive first
    is_reflexive = bool(REFLEXIVE_RE.search(word))
    temp_word = REFLEXIVE_RE.sub("", word)

    if VERB_RE.search(temp_word):
        return 'VERB', get_stem_verb(word)

    # 3. Nouns (Default)
    return 'NOUN', get_stem_noun(word)

def main():
    print("Loading missing words...")
    missing_words = set()
    try:
        with open(MISSING_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if RUSSIAN_WORD_RE.match(word):
                    missing_words.add(word)
    except FileNotFoundError:
        print(f"Error: {MISSING_FILE} not found.")
        sys.exit(1)

    print(f"Loaded {len(missing_words)} valid Russian missing words.")

    adj_groups = defaultdict(lambda: {'forms': set(), 'freq': 0})
    verb_groups = defaultdict(lambda: {'forms': set(), 'freq': 0})
    noun_groups = defaultdict(lambda: {'forms': set(), 'freq': 0})

    print("Processing frequency list...")
    try:
        with open(FREQ_FILE, 'r', encoding='utf-8') as f:
            for line in tqdm(f, unit="lines"):
                parts = line.strip().split('\t')
                if len(parts) < 3:
                    continue
                word = parts[0]

                if word in missing_words:
                    try:
                        freq = int(parts[2])
                    except ValueError:
                        continue

                    pos, stem = classify_and_stem(word)

                    if pos == 'ADJ':
                        adj_groups[stem]['forms'].add(word)
                        adj_groups[stem]['freq'] += freq
                    elif pos == 'VERB':
                        verb_groups[stem]['forms'].add(word)
                        verb_groups[stem]['freq'] += freq
                    else:
                        noun_groups[stem]['forms'].add(word)
                        noun_groups[stem]['freq'] += freq
    except FileNotFoundError:
        print(f"Error: {FREQ_FILE} not found.")
        sys.exit(1)

    # Output functions
    def write_groups(filename, groups):
        sorted_groups = sorted(groups.items(), key=lambda x: x[1]['freq'], reverse=True)
        with open(filename, 'w', encoding='utf-8') as f:
            for stem, data in sorted_groups:
                forms_str = ", ".join(sorted(data['forms']))
                f.write(f"Stem: {stem} | Freq: {data['freq']} | Forms: {forms_str}\n")

    print("Writing output files...")
    write_groups(OUT_ADJ, adj_groups)
    write_groups(OUT_VERB, verb_groups)
    write_groups(OUT_NOUN, noun_groups)
    print("Done.")

if __name__ == "__main__":
    main()
