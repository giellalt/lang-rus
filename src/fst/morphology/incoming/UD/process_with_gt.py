#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "conllu>=4.5",
# ]
# ///

"""
Process all UD treebanks through GiellaLT FST tokenizer for GT/UD comparison.

This script:
1. Extracts raw text from all .conllu files
2. Runs text through hfst-tokenize with the GiellaLT Russian FST
3. Saves output in parallel directory structure for easy comparison
4. Preserves sentence boundaries and metadata for alignment
5. Uses multiprocessing to speed up processing

Output structure:
  gt_tokenized/
    UD_Russian-GSD/
      ru_gsd-ud-train.cg
      ...
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple
from multiprocessing import Pool, cpu_count
import conllu


def extract_sentences_with_metadata(conllu_file: Path) -> List[Tuple[str, str, str]]:
    """
    Extract sentences with metadata from a .conllu file.
    
    Returns list of (sent_id, text, raw_text) tuples.
    """
    sentences = []
    
    try:
        with open(conllu_file, 'r', encoding='utf-8') as f:
            parsed = conllu.parse(f.read())
            
        for sentence in parsed:
            sent_id = sentence.metadata.get('sent_id', 'unknown')
            text = sentence.metadata.get('text', '')
            
            # Fallback: reconstruct text from tokens if not in metadata
            if not text and sentence:
                tokens = []
                for token in sentence:
                    if isinstance(token['id'], int):
                        tokens.append(token['form'])
                text = ' '.join(tokens)
            
            sentences.append((sent_id, text, text))
                
    except Exception as e:
        print(f"Error processing {conllu_file}: {e}", file=sys.stderr)
        return []
    
    return sentences


def run_hfst_tokenize_file(texts: List[str], tokenizer_path: Path) -> str:
    """
    Run all texts from a file through hfst-tokenize in one call.
    Returns complete CG format output.
    """
    if not texts:
        return ""
    
    # Join all texts with newlines - FST will process them as separate sentences
    batch_input = '\n'.join(texts) + '\n'
    
    try:
        result = subprocess.run(
            ['hfst-tokenize', '--giella-cg', str(tokenizer_path)],
            input=batch_input,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=600  # 10 minutes for large files
        )
        
        if result.returncode != 0:
            print(f"Warning: hfst-tokenize returned {result.returncode}", file=sys.stderr)
            if result.stderr:
                print(f"  stderr: {result.stderr[:500]}", file=sys.stderr)
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        print(f"Error: hfst-tokenize timed out", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Error running hfst-tokenize: {e}", file=sys.stderr)
        return ""


def parse_cg_output_into_sentences(cg_output: str, expected_count: int) -> List[str]:
    """
    Parse CG format output and split it into individual sentences.
    
    Key insight: hfst-tokenize outputs ":\\n" (colon-backslash-n, literally 3 chars)
    at sentence boundaries, and ": " (colon-space) or ": \n" after tokens within a sentence.
    """
    if not cg_output.strip():
        return [""] * expected_count
    
    # Split on the literal string ":\\n" (colon-backslash-n) which marks sentence boundaries
    # This is output by hfst-tokenize to mark end of each input line
    raw_sentences = cg_output.split(':\\n')
    
    sentences = []
    for sent in raw_sentences:
        sent = sent.strip()
        if sent:  # Filter out empty parts
            # Add back the ":" at the end for consistency with CG format
            sentences.append(sent + '\n:')
    
    # Adjust to expected count
    if len(sentences) < expected_count:
        sentences.extend([""] * (expected_count - len(sentences)))
    elif len(sentences) > expected_count:
        print(f"Warning: Got {len(sentences)} sentences, expected {expected_count}", file=sys.stderr)
        sentences = sentences[:expected_count]
    
    return sentences


def process_conllu_file(args) -> Tuple[str, int]:
    """
    Process a single .conllu file through the FST tokenizer.
    Process entire file at once for efficiency.
    """
    conllu_file, tokenizer_path, output_dir = args
    
    # Extract sentences
    sentences = extract_sentences_with_metadata(conllu_file)
    
    if not sentences:
        return (conllu_file.name, 0)
    
    # Extract just the texts for batch processing
    texts = [text for _, text, _ in sentences]
    
    # Run entire file through FST tokenizer at once
    cg_output = run_hfst_tokenize_file(texts, tokenizer_path)
    
    # Parse output back into individual sentences
    cg_sentences = parse_cg_output_into_sentences(cg_output, len(sentences))
    
    # Create output file with .cg extension
    output_file = output_dir / conllu_file.name.replace('.conllu', '.cg')
    
    success_count = 0
    error_count = 0
    
    # Write output with metadata
    with open(output_file, 'w', encoding='utf-8') as out:
        for (sent_id, text, _), cg_sent in zip(sentences, cg_sentences):
            if not text.strip():
                continue
            
            # Write metadata header
            out.write(f"# sent_id = {sent_id}\n")
            out.write(f"# text = {text}\n")
            
            if cg_sent.strip():
                out.write(cg_sent)
                # Ensure sentence boundary
                if not cg_sent.endswith('\n'):
                    out.write('\n')
                out.write('\n')
                success_count += 1
            else:
                out.write("# ERROR: No output from tokenizer\n\n")
                error_count += 1
    
    if error_count > 0:
        print(f"  {conllu_file.name}: {success_count} OK, {error_count} errors", file=sys.stderr)
    
    return (conllu_file.name, len(sentences))


def main():
    # Configuration
    tokenizer_path = Path("../../../../../tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst")
    
    if not tokenizer_path.exists():
        print(f"Error: Tokenizer not found at {tokenizer_path}", file=sys.stderr)
        sys.exit(1)
    
    # Find all .conllu files
    current_dir = Path('.')
    conllu_files = sorted(current_dir.glob('UD_*/**/*.conllu'))
    
    if not conllu_files:
        print("No .conllu files found in UD_* directories", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory structure
    output_base = current_dir / "gt_tokenized"
    output_base.mkdir(exist_ok=True)
    
    print(f"Processing {len(conllu_files)} .conllu files...", file=sys.stderr)
    print(f"Using tokenizer: {tokenizer_path}", file=sys.stderr)
    print(f"Output directory: {output_base}", file=sys.stderr)
    print()
    
    # Group files by treebank
    treebanks = {}
    for conllu_file in conllu_files:
        treebank = conllu_file.parts[-2]  # e.g., "UD_Russian-GSD"
        if treebank not in treebanks:
            treebanks[treebank] = []
        treebanks[treebank].append(conllu_file)
    
    # Prepare all processing tasks
    tasks = []
    for treebank, files in sorted(treebanks.items()):
        # Create treebank output directory
        treebank_output = output_base / treebank
        treebank_output.mkdir(exist_ok=True)
        
        for conllu_file in files:
            tasks.append((conllu_file, tokenizer_path, treebank_output))
    
    # Process with multiprocessing
    num_workers = max(1, cpu_count() - 1)  # Leave one core free
    print(f"Using {num_workers} parallel workers\n", file=sys.stderr)
    
    with Pool(num_workers) as pool:
        results = pool.map(process_conllu_file, tasks)
    
    # Report results
    print("\nProcessing complete!", file=sys.stderr)
    for filename, sent_count in results:
        print(f"  {filename}: {sent_count} sentences", file=sys.stderr)
    
    print(f"\nDone! Output written to {output_base}/", file=sys.stderr)
    print(f"\nTo compare a file:", file=sys.stderr)
    print(f"  Original: UD_Russian-GSD/ru_gsd-ud-train.conllu", file=sys.stderr)
    print(f"  GT tags:  gt_tokenized/UD_Russian-GSD/ru_gsd-ud-train.cg", file=sys.stderr)


if __name__ == '__main__':
    main()
