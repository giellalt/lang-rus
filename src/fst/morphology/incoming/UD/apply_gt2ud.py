#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

"""
Apply gt2ud.cg3 grammar to all CG files.

Converts GiellaLT format tags to UD format tags using VISL-CG3.
"""

import sys
import subprocess
from pathlib import Path
from multiprocessing import Pool, cpu_count


def apply_cg_grammar(args) -> tuple[str, bool]:
    """Apply CG3 grammar to a single file."""
    cg_file, grammar_path, output_dir = args
    
    try:
        # Read input
        with open(cg_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        
        # Run through vislcg3
        result = subprocess.run(
            ['vislcg3', '--grammar', str(grammar_path)],
            input=input_text,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"Warning: vislcg3 returned {result.returncode} for {cg_file.name}", file=sys.stderr)
            if result.stderr:
                print(f"  stderr: {result.stderr[:200]}", file=sys.stderr)
        
        # Create output file with .cg2ud extension
        output_file = output_dir / cg_file.name.replace('.cg', '.cg2ud')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        
        return (cg_file.name, True)
        
    except subprocess.TimeoutExpired:
        print(f"Error: vislcg3 timed out on {cg_file.name}", file=sys.stderr)
        return (cg_file.name, False)
    except Exception as e:
        print(f"Error processing {cg_file.name}: {e}", file=sys.stderr)
        return (cg_file.name, False)


def main():
    grammar_path = Path('../../../../cg3/gt2ud.cg3')
    
    if not grammar_path.exists():
        print("Error: gt2ud.cg3 not found", file=sys.stderr)
        sys.exit(1)
    
    # Find all .cg files
    gt_dir = Path('gt_tokenized')
    
    if not gt_dir.exists():
        print("Error: gt_tokenized directory not found", file=sys.stderr)
        sys.exit(1)
    
    cg_files = sorted(gt_dir.glob('**/*.cg'))
    
    if not cg_files:
        print("No .cg files found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Applying gt2ud.cg3 to {len(cg_files)} files...", file=sys.stderr)
    
    # Prepare tasks
    tasks = []
    for cg_file in cg_files:
        output_dir = cg_file.parent
        tasks.append((cg_file, grammar_path, output_dir))
    
    # Process with multiprocessing
    num_workers = max(1, cpu_count() - 1)
    print(f"Using {num_workers} parallel workers\n", file=sys.stderr)
    
    with Pool(num_workers) as pool:
        results = pool.map(apply_cg_grammar, tasks)
    
    # Report results
    print("\nConversion complete!", file=sys.stderr)
    successful = sum(1 for _, success in results if success)
    print(f"Successfully converted: {successful}/{len(results)} files", file=sys.stderr)


if __name__ == '__main__':
    main()
