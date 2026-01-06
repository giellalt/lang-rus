## L2 transducers (Oahpa “learner” analyser)

This directory contains an optional L2 analyser intended for Oahpa / learner-facing tools.
It extends the normal analyser with additional paths that model typical learner errors and
tag them as `+Err/L2_*`.

### Enabling the build

The L2 analyser is built only when configure is run with L2 enabled:

- `./configure --enable-L2`

> WARNING: The build is extremely slow and the resulting transducer is extremely large!

### What gets built

The main target is:

- `src/fst/analyser-gt-desc-L2.hfst`

It is added to `GT_ANALYSERS` under `if WANT_L2` in `src/fst/Makefile.am`.

### How it is built (Makefile pipeline)

The L2 analyser is assembled in `src/fst/Makefile.am` as follows:

1. Build alternative L2 phonology rule files `phonology-err-L2_*.twolc` by concatenating
	selected `src/fst/phonology-rules/*` fragments (variants: `ii`, `FV`, `NoFV`, `Pal`, `SRo`).
2. Compile each `.twolc` into an HFST transducer `phonology-err-L2_%.hfst`.
3. For each variant, compose the lexicon with the L2 phonology:
	`morphology/lexicon.hfst` ∘ `phonology-err-L2_$*.hfst`.
4. Subtract the standard generator (`generator-raw-gt-desc.hfst`) so the L2 generator contains
	only the “extra” paths introduced by the error phonology.
5. Compose with tag-cleanup/reordering filters (in `src/fst/filters/`) and materialise
	`generator-raw-gt-desc-err-L2_%.hfst`.
6. Copy/invert/filter into an analyser-side transducer, applying the usual analyser filters and
	orthography compose steps (e.g. init-uppercase/spellrelax).
7. Optionally apply `orthography/destressOptional.compose.hfst`.
8. Add the error tag for that variant: paths are annotated with `+Err/L2_$*`.
9. Create the final `analyser-gt-desc-L2.hfst` by starting from `analyser-gt-desc.hfst` and
	disjuncting (`hfst-disjunct`) in each `analyser-gt-desc-err-L2_*.tmp2.hfst`.

Finally, additional orthographic error paths are injected with:

- `src/add_L2_orth_err.sh` (called several times from the `analyser-gt-desc-L2.hfst` rule)

### Building locally

From the repo top-level:

- `./autogen.sh` (if needed)
- `./configure --enable-L2`
- `make`

Or, after configure, from this directory:

- `make analyser-gt-desc-L2.hfst`
