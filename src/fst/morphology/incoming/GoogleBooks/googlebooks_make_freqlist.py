#!/usr/bin/env python3
import os
import glob
from collections import defaultdict
from tqdm import tqdm

# Directory containing the Google Books Ngram files
DATA_DIR = "./"
FILE_PATTERN = "1-0000*"

# Output file
OUTPUT_FILE = "googlebooks_freqlist.txt"

def main():
    freq = defaultdict(int)
    files = glob.glob(os.path.join(DATA_DIR, FILE_PATTERN))
    for fname in tqdm(files, desc="Files", unit="file"):
        # Count lines for tqdm progress bar
        try:
            total_lines = sum(1 for _ in open(fname, "rt", encoding="utf-8", errors="replace"))
        except Exception:
            total_lines = None
        with open(fname, "rt", encoding="utf-8", errors="replace") as f:
            for line in tqdm(f, desc=f"Lines in {os.path.basename(fname)}", unit="line", total=total_lines, leave=False):
                parts = line.rstrip().split()
                if not parts or len(parts) < 2:
                    continue
                wordform = parts[0]
                if '_' in wordform:
                    wf, pos = wordform.rsplit('_', 1)
                else:
                    wf, pos = wordform, 'UNK'
                # Sum all counts from the rest of the columns
                total_count = 0
                for col in parts[1:]:
                    # Each col is like '1843,2,1' (year,count,count)
                    fields = col.split(',')
                    if len(fields) >= 2:
                        try:
                            count = int(fields[1])
                            total_count += count
                        except ValueError:
                            continue
                freq[(wf, pos)] += total_count
    # Filter out tokens without any Cyrillic characters
    import re
    cyrillic_re = re.compile(r"[\u0400-\u04FF]")
    filtered_freq = {}
    dropped = 0
    for (wf, pos), count in freq.items():
        if cyrillic_re.search(wf):
            filtered_freq[(wf, pos)] = count
        else:
            dropped += 1
    total = len(freq)
    percent = (dropped / total * 100) if total else 0
    # Write output sorted alphabetically by wordform, then POS
    with open(OUTPUT_FILE, "wt", encoding="utf-8") as out:
        for (wf, pos) in tqdm(sorted(filtered_freq), desc="Writing output", unit="item"):
            out.write(f"{wf}\t{pos}\t{filtered_freq[(wf, pos)]}\n")
    print(f"Dropped {dropped} of {total} unique tokens ({percent:.2f}%) without Cyrillic characters.")

if __name__ == "__main__":
    main()
