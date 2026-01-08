#!/usr/bin/env python3
"""
Verify FST coverage against UD gold annotations.
Reports results in 3 groups:
1. Good alignment + lemma found → report tagging accuracy
2. Failed alignment (>50% mismatch) → FST output wrong text
3. Good alignment + lemma missing → vocabulary gaps
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import Counter
import conllu


def normalize_form(form: str) -> str:
    """Normalize token form for comparison."""
    return form.lower().strip()


def normalize_lemma(lemma: str) -> str:
    """Normalize lemma by removing Unicode superscript numbers."""
    if lemma is None:
        return ""
    # Remove superscript numbers: так¹ → так, и² → и
    return re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+', '', lemma)


def ud_features_to_tagset(feats: Dict) -> Set[str]:
    """Convert UD features dict to set of tags."""
    if feats is None:
        return set()
    tags = set()
    for key, value in feats.items():
        if isinstance(value, list):
            for v in value:
                tags.add(f"{key}={v}")
        else:
            tags.add(f"{key}={value}")
    return tags


def parse_cg2ud_file(filepath: Path) -> Dict[str, List[Dict]]:
    """
    Parse CG2UD file into sentences.
    Returns dict mapping sent_id to list of token dicts.
    """
    sentences = {}
    current_sent_id = None
    current_tokens = []
    current_token = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            
            # Sentence ID
            if line.startswith('# sent_id = '):
                if current_sent_id and current_tokens:
                    sentences[current_sent_id] = current_tokens
                current_sent_id = line.split('=', 1)[1].strip()
                current_tokens = []
                current_token = None
            
            # Error marker
            elif line.startswith('# ERROR:'):
                # Skip sentences with errors
                current_sent_id = None
                current_tokens = []
                current_token = None
            
            # Word form (starts with "<)
            elif line.startswith('"<'):
                if current_token:
                    current_tokens.append(current_token)
                
                # Extract form between "<" and ">"
                form = line[2:line.rfind('>')]
                current_token = {
                    'form': form,
                    'analyses': []
                }
            
            # Analysis line (starts with whitespace and ")
            elif line.startswith('\t"') or line.startswith('        "'):
                if current_token is None:
                    continue
                
                # Parse analysis: "lemma" tags
                line = line.strip()
                if not line.startswith('"'):
                    continue
                
                # Extract lemma and tags
                parts = line.split('" ', 1)
                if len(parts) != 2:
                    continue
                
                lemma = parts[0][1:]  # Remove leading "
                tags_str = parts[1]
                
                # Parse tags
                tags = set()
                for tag in tags_str.split():
                    tags.add(tag)
                
                current_token['analyses'].append({
                    'lemma': lemma,
                    'tags': tags
                })
    
    # Add last token/sentence
    if current_token:
        current_tokens.append(current_token)
    if current_sent_id and current_tokens:
        sentences[current_sent_id] = current_tokens
    
    return sentences


def align_tokens(ud_tokens: List, cg_tokens: List) -> List[Tuple[Optional[Dict], Optional[Dict], str]]:
    """
    Align UD and CG tokens using Needleman-Wunsch algorithm.
    Returns list of (ud_token, cg_token, alignment_type) tuples.
    """
    # Needleman-Wunsch parameters
    MATCH_SCORE = 2
    MISMATCH_PENALTY = -2
    GAP_PENALTY = -1
    
    n = len(ud_tokens)
    m = len(cg_tokens)
    
    # Initialize scoring matrix
    score = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Initialize first row and column
    for i in range(n + 1):
        score[i][0] = i * GAP_PENALTY
    for j in range(m + 1):
        score[0][j] = j * GAP_PENALTY
    
    # Fill scoring matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            ud_form = normalize_form(ud_tokens[i-1]['form'])
            cg_form = normalize_form(cg_tokens[j-1]['form'])
            
            match = score[i-1][j-1] + (MATCH_SCORE if ud_form == cg_form else MISMATCH_PENALTY)
            delete = score[i-1][j] + GAP_PENALTY
            insert = score[i][j-1] + GAP_PENALTY
            
            score[i][j] = max(match, delete, insert)
    
    # Traceback to get alignment
    alignments = []
    i, j = n, m
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            ud_form = normalize_form(ud_tokens[i-1]['form'])
            cg_form = normalize_form(cg_tokens[j-1]['form'])
            
            if score[i][j] == score[i-1][j-1] + (MATCH_SCORE if ud_form == cg_form else MISMATCH_PENALTY):
                # Match or mismatch
                align_type = 'exact' if ud_form == cg_form else 'mismatch'
                alignments.append((ud_tokens[i-1], cg_tokens[j-1], align_type))
                i -= 1
                j -= 1
                continue
        
        if i > 0 and score[i][j] == score[i-1][j] + GAP_PENALTY:
            # Gap in CG (UD token missing in CG)
            alignments.append((ud_tokens[i-1], None, 'missing_cg'))
            i -= 1
        elif j > 0 and score[i][j] == score[i][j-1] + GAP_PENALTY:
            # Gap in UD (extra CG token)
            alignments.append((None, cg_tokens[j-1], 'extra_cg'))
            j -= 1
        else:
            # Shouldn't happen, but break to avoid infinite loop
            break
    
    # Reverse since we traced backwards
    alignments.reverse()
    
    return alignments


def compare_files_grouped(conllu_file: Path, cg2ud_file: Path) -> Dict:
    """
    Compare UD file with CG2UD file, grouping results into three categories.
    
    Returns dict with stats for each group.
    """
    # Parse both files
    with open(conllu_file, 'r', encoding='utf-8') as f:
        ud_sentences = conllu.parse(f.read())
    
    cg_sentences = parse_cg2ud_file(cg2ud_file)
    
    # Initialize group statistics
    results = {
        'total_sentences': 0,
        'exact_tokenization': 0,
        
        # Group 1: Good alignment + lemma found
        'group1_tokens': 0,
        'group1_correct_tags': 0,
        'group1_wrong_tags': 0,
        
        # Group 2: Failed alignment
        'group2_sentences': 0,
        'group2_tokens': 0,
        'group2_failed': [],  # List of failure details
        
        # Group 3: Good alignment + lemma missing
        'group3_tokens': 0,
        'group3_missing': []  # List of missing lemma details
    }
    
    for ud_sent in ud_sentences:
        sent_id = ud_sent.metadata.get('sent_id', 'unknown')
        results['total_sentences'] += 1
        
        # Check if sentence was tokenized
        if sent_id not in cg_sentences:
            ud_tokens = [t for t in ud_sent if not isinstance(t['id'], tuple)]
            results['group2_sentences'] += 1
            results['group2_tokens'] += len(ud_tokens)
            results['group2_failed'].append({
                'sent_id': sent_id,
                'reason': 'not_tokenized',
                'tokens': len(ud_tokens)
            })
            continue
        
        # Get tokens
        ud_tokens = [t for t in ud_sent if not isinstance(t['id'], tuple)]
        cg_tokens = cg_sentences[sent_id]
        
        # Align tokens
        alignments = align_tokens(ud_tokens, cg_tokens)
        
        # Check alignment quality
        mismatch_count = sum(1 for a in alignments if a[2] in ('mismatch', 'missing_cg', 'extra_cg'))
        mismatch_rate = mismatch_count / len(ud_tokens) if ud_tokens else 0
        
        # Group 2: Severe alignment failure (>50% mismatched)
        if mismatch_rate > 0.5:
            results['group2_sentences'] += 1
            results['group2_tokens'] += len(ud_tokens)
            results['group2_failed'].append({
                'sent_id': sent_id,
                'reason': 'severe_mismatch',
                'tokens': len(ud_tokens),
                'mismatch_rate': mismatch_rate
            })
            continue
        
        # Good alignment
        if mismatch_count == 0:
            results['exact_tokenization'] += 1
        
        # Process each aligned token
        for ud_tok, cg_tok, align_type in alignments:
            if ud_tok is None:
                continue
            
            ud_form = ud_tok['form']
            ud_lemma = normalize_lemma(ud_tok['lemma'])
            ud_upos = ud_tok['upos']
            ud_feats = ud_features_to_tagset(ud_tok['feats'])
            ud_tags = {ud_upos} | ud_feats
            
            # Skip if alignment failed
            if cg_tok is None or align_type in ('missing_cg', 'mismatch'):
                results['group3_tokens'] += 1
                results['group3_missing'].append({
                    'form': ud_form,
                    'lemma': ud_lemma,
                    'upos': ud_upos,
                    'reason': 'alignment_issue'
                })
                continue
            
            # Check CG analyses for lemma match
            cg_analyses = cg_tok.get('analyses', [])
            lemma_found = False
            tags_correct = False
            
            for analysis in cg_analyses:
                cg_lemma = normalize_lemma(analysis['lemma'])
                cg_tags = analysis['tags']
                
                # Skip unknown words
                if '?' in cg_tags:
                    continue
                
                # Check lemma match
                if cg_lemma.lower() == ud_lemma.lower():
                    lemma_found = True
                    
                    # Check if tags match
                    if ud_tags.issubset(cg_tags):
                        tags_correct = True
                        break
            
            if lemma_found:
                # Group 1: Lemma found
                results['group1_tokens'] += 1
                if tags_correct:
                    results['group1_correct_tags'] += 1
                else:
                    results['group1_wrong_tags'] += 1
            else:
                # Group 3: Lemma not found
                results['group3_tokens'] += 1
                has_analyses = any('?' not in a['tags'] for a in cg_analyses)
                results['group3_missing'].append({
                    'form': ud_form,
                    'lemma': ud_lemma,
                    'upos': ud_upos,
                    'reason': 'lemma_not_found' if has_analyses else 'unknown_word'
                })
    
    return results


def main():
    # Find all UD and CG2UD file pairs
    ud_files = sorted(Path('.').glob('UD_*/**/*.conllu'))
    
    if not ud_files:
        print("No UD files found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Comparing {len(ud_files)} file pairs...\n")
    
    # Aggregate results
    total_results = {
        'total_sentences': 0,
        'exact_tokenization': 0,
        'group1_tokens': 0,
        'group1_correct_tags': 0,
        'group1_wrong_tags': 0,
        'group2_sentences': 0,
        'group2_tokens': 0,
        'group2_failed': [],
        'group3_tokens': 0,
        'group3_missing': []
    }
    
    file_results = {}
    
    for conllu_file in ud_files:
        treebank = conllu_file.parts[-2]
        cg2ud_file = Path('gt_tokenized') / treebank / conllu_file.name.replace('.conllu', '.cg2ud')
        
        if not cg2ud_file.exists():
            print(f"Warning: {cg2ud_file} not found", file=sys.stderr)
            continue
        
        results = compare_files_grouped(conllu_file, cg2ud_file)
        file_results[conllu_file.name] = results
        
        # Aggregate
        for key in ['total_sentences', 'exact_tokenization', 'group1_tokens', 
                    'group1_correct_tags', 'group1_wrong_tags', 'group2_sentences',
                    'group2_tokens', 'group3_tokens']:
            total_results[key] += results[key]
        
        total_results['group2_failed'].extend([{**f, 'file': conllu_file.name} for f in results['group2_failed']])
        total_results['group3_missing'].extend([{**m, 'file': conllu_file.name} for m in results['group3_missing']])
        
        # Print per-file summary
        g1_total = results['group1_tokens']
        g1_acc = (results['group1_correct_tags'] / g1_total * 100) if g1_total > 0 else 0
        print(f"{conllu_file.name}:")
        print(f"  Group 1 (lemma found): {g1_total} tokens, {g1_acc:.1f}% correct tags")
        print(f"  Group 2 (failed align): {results['group2_sentences']} sentences, {results['group2_tokens']} tokens")
        print(f"  Group 3 (lemma missing): {results['group3_tokens']} tokens")
    
    # Print overall summary
    print("\n" + "="*70)
    print("OVERALL RESULTS")
    print("="*70)
    print(f"Total sentences: {total_results['total_sentences']}")
    print(f"Exact tokenization: {total_results['exact_tokenization']} ({total_results['exact_tokenization']/total_results['total_sentences']*100:.1f}%)")
    
    print(f"\nGROUP 1: Good alignment + lemma found")
    g1_total = total_results['group1_tokens']
    g1_correct = total_results['group1_correct_tags']
    g1_wrong = total_results['group1_wrong_tags']
    print(f"  Total tokens: {g1_total}")
    print(f"  Correct tags: {g1_correct} ({g1_correct/g1_total*100:.1f}%)")
    print(f"  Wrong tags: {g1_wrong} ({g1_wrong/g1_total*100:.1f}%)")
    print(f"  → Tagging accuracy when lemma is found: {g1_correct/g1_total*100:.1f}%")
    
    print(f"\nGROUP 2: Failed alignment")
    print(f"  Failed sentences: {total_results['group2_sentences']}")
    print(f"  Affected tokens: {total_results['group2_tokens']}")
    print(f"  → {total_results['group2_sentences']/total_results['total_sentences']*100:.1f}% of sentences")
    
    print(f"\nGROUP 3: Good alignment + lemma missing")
    print(f"  Tokens with missing lemmas: {total_results['group3_tokens']}")
    print(f"  → Vocabulary coverage: {g1_total/(g1_total+total_results['group3_tokens'])*100:.1f}%")
    
    # Write detailed failures
    if total_results['group2_failed']:
        with open('sentence_failures.txt', 'w', encoding='utf-8') as f:
            f.write(f"# GROUP 2: Failed alignment ({len(total_results['group2_failed'])} sentences)\n\n")
            for failure in total_results['group2_failed']:
                f.write(f"File: {failure['file']}\n")
                f.write(f"Sentence: {failure['sent_id']}\n")
                f.write(f"Reason: {failure['reason']}\n")
                f.write(f"Tokens: {failure['tokens']}\n\n")
        print(f"\nDetailed failures written to: sentence_failures.txt")
    
    # Write missing lemmas
    if total_results['group3_missing']:
        lemma_counts = Counter((m['lemma'], m['upos']) for m in total_results['group3_missing'])
        with open('missing_lemmas.txt', 'w', encoding='utf-8') as f:
            f.write(f"# GROUP 3: Missing lemmas ({len(total_results['group3_missing'])} tokens)\n\n")
            for (lemma, upos), count in lemma_counts.most_common(200):
                f.write(f"{lemma}\t{upos}\t{count}\n")
        print(f"Missing lemmas written to: missing_lemmas.txt")


if __name__ == '__main__':
    main()
