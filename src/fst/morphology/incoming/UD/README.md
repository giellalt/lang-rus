# GiellaLT Russian FST Evaluation Against Universal Dependencies

This directory contains scripts and tools for evaluating the GiellaLT Russian morphological analyzer (FST) against Universal Dependencies treebanks.

## Purpose

Verify FST coverage and GT→UD tag conversion accuracy by:
1. Tokenizing UD sentences with the FST
2. Converting GiellaLT (GT) morphological tags to UD format
3. Comparing FST output against UD gold annotations
4. Identifying vocabulary gaps and tagging issues

## Requirements

- Python 3.7+
- `hfst-tokenize` (from GiellaLT infrastructure)
- `vislcg3` (for CG3 grammar)
- `conllu` Python package: `pip install conllu`
- GiellaLT Russian FST installed at: `~/repos/giellalt/lang-rus/tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst`

## Setup

### 1. Clone UD Treebanks

```bash
./clone_ud_repos.sh
```

This downloads 5 Russian UD treebanks (~200MB):
- UD_Russian-GSD (news, Wikipedia)
- UD_Russian-SynTagRus (formal texts)  
- UD_Russian-Taiga (social media)
- UD_Russian-Poetry (literary)
- UD_Russian-PUD (parallel test set)

**Note**: These repositories are in .gitignore and won't be committed.

### 2. Install Python Dependencies

```bash
pip install conllu
```

## Evaluation Pipeline

Run the three scripts in order:

### Step 1: Tokenize with FST

```bash
python3 process_with_gt.py
```

- Extracts sentences from all `.conllu` files
- Runs them through `hfst-tokenize`
- Outputs CG format files to `gt_tokenized/`
- Takes ~2-5 minutes for all treebanks

### Step 2: Convert GT→UD Tags

```bash
python3 apply_gt2ud.py
```

- Applies `gt2ud.cg3` grammar to convert GiellaLT tags to UD
- Uses `vislcg3` with multiprocessing
- Creates `.cg2ud` files in `gt_tokenized/`
- Takes ~1-2 minutes

### Step 3: Evaluate Coverage

```bash
python3 verify_coverage.py
```

- Compares FST output against UD gold annotations
- Uses Needleman-Wunsch alignment for robust token matching
- Generates three-group analysis:
  - **Group 1**: Good alignment + lemma found → tagging accuracy
  - **Group 2**: Failed alignment → tokenization issues
  - **Group 3**: Good alignment + lemma missing → vocabulary gaps
- Outputs: `missing_lemmas.txt`, `sentence_failures.txt`
- Takes ~3-5 minutes

## Understanding Results

### Three-Group Analysis

**Group 1: Good Alignment + Lemma Found**
- Measures GT→UD tag conversion accuracy
- When FST has the word and alignment works
- Current result: ~64% accuracy

**Group 2: Failed Alignment**  
- Sentences where FST output doesn't match input
- Usually tokenization issues or special characters
- Current result: ~7% of sentences
- See `sentence_failures.txt` for details

**Group 3: Good Alignment + Lemma Missing**
- Words not in FST lexicon
- Identifies vocabulary gaps
- Current result: ~7% of tokens
- See `missing_lemmas.txt` for priorities

### Example Output

```
GROUP 1: Good alignment + lemma found
  Total tokens: 2,967,559
  Correct tags: 1,887,553 (63.6%)
  Wrong tags: 1,080,006 (36.4%)
  → Tagging accuracy when lemma is found: 63.6%

GROUP 2: Failed alignment
  Failed sentences: 14,884
  Affected tokens: 264,523
  → 6.8% of sentences

GROUP 3: Good alignment + lemma missing
  Tokens with missing lemmas: 223,875
  → Vocabulary coverage: 93.0%
```

## Files

### Core Scripts
- `process_with_gt.py` - Tokenize UD sentences with FST
- `apply_gt2ud.py` - Convert GT tags to UD format
- `verify_coverage.py` - Evaluate and report results
- `gt2ud.cg3` - CG3 grammar for GT→UD tag conversion

### Configuration
- `clone_ud_repos.sh` - Download UD treebanks
- `.gitignore` - Exclude UD repos and generated files

### Generated Files (not in git)
- `gt_tokenized/` - FST output in CG format
- `missing_lemmas.txt` - High-frequency missing vocabulary
- `sentence_failures.txt` - Sentences with alignment failures
- `FINAL_RESULTS_GROUPED.md` - Comprehensive analysis report

## Key Findings (Current)

- **Tagging Accuracy**: 63.6% (when lemma is found)
- **Vocabulary Coverage**: 93.0% of tokens
- **Tokenization Success**: 93.2% of sentences
- **Main Issue**: 36.4% wrong tags → need better GT→UD conversion rules

## Improving Results

### 1. Improve Tagging Accuracy (Priority: High)

Edit `gt2ud.cg3` to add/refine conversion rules:

```cg3
# Example: Better handling of participles
MAP (VerbForm=Part) TARGET (V PrsPrc);
MAP (Tense=Pres) TARGET (V PrsPrc);
```

### 2. Add Missing Vocabulary (Priority: Medium)

Review `missing_lemmas.txt` and add high-frequency words to FST lexicon.

### 3. Fix Tokenization Issues (Priority: Medium)

Investigate sentences in `sentence_failures.txt`, especially:
- Taiga-b (12,000+ failures)
- Taiga-dev (1,100+ failures)
- Taiga-test (600+ failures)

## Technical Details

### Needleman-Wunsch Alignment

Uses dynamic programming to find optimal token alignment even when:
- FST tokenizes differently than UD (e.g., "#word" → "#" + "word")
- Some tokens are missing or misaligned
- Text contains special characters

### Subset Matching

A match requires:
- **Lemma**: Normalized match (ignoring superscripts: так¹ = так)
- **Tags**: All UD tags must be present in GT tags (GT can have extras)

This allows GT tags like `TV` (transitive), `IV` (intransitive), `Der/`, etc. that aren't in UD.

### GT→UD Tag Mapping

The `gt2ud.cg3` grammar handles:
- POS conversion (N→NOUN, V→VERB, etc.)
- Feature mapping (Sg→Number=Sing, Gen→Case=Gen, etc.)
- Aspect, tense, mood, voice for verbs
- VerbForm (Fin, Inf, Part, Conv)
- Removing GT-specific tags (Err/Orth, Use/*, LEFT, RIGHT)

## Troubleshooting

### "No module named 'conllu'"
```bash
pip install conllu
```

### "Tokenizer not found"
Check that FST exists at:
```
~/repos/giellalt/lang-rus/tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst
```

Update path in `process_with_gt.py` if different.

### "vislcg3: command not found"
Install VISL-CG3:
```bash
# Ubuntu/Debian
sudo apt-get install cg3

# macOS
brew install apertium-all-dev
```

## References

- [Universal Dependencies](https://universaldependencies.org/)
- [GiellaLT Infrastructure](https://giellalt.uit.no/)
- [VISL CG3 Documentation](https://visl.sdu.dk/cg3.html)

## Citation

If you use this evaluation framework, please cite:
- The Universal Dependencies project
- The GiellaLT infrastructure project
- The relevant UD Russian treebanks

## License

Scripts in this directory: Same license as GiellaLT infrastructure (GPL/LGPL)

UD treebanks: CC BY-SA 4.0 (see individual repositories)
