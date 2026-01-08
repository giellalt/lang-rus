#!/bin/bash
# Clone Russian Universal Dependencies treebanks
# These are needed for evaluation but should not be committed to this repository

set -e

echo "Cloning Russian UD treebanks..."
echo "This will download ~200MB of data"
echo ""

# Clone each Russian UD treebank
git clone https://github.com/UniversalDependencies/UD_Russian-GSD.git
git clone https://github.com/UniversalDependencies/UD_Russian-SynTagRus.git
git clone https://github.com/UniversalDependencies/UD_Russian-Taiga.git
git clone https://github.com/UniversalDependencies/UD_Russian-Poetry.git
git clone https://github.com/UniversalDependencies/UD_Russian-PUD.git

echo ""
echo "Done! Cloned 5 Russian UD treebanks:"
echo "  - UD_Russian-GSD (news, Wikipedia)"
echo "  - UD_Russian-SynTagRus (formal texts)"
echo "  - UD_Russian-Taiga (social media)"
echo "  - UD_Russian-Poetry (literary)"
echo "  - UD_Russian-PUD (parallel test set)"
echo ""
echo "To run the evaluation pipeline:"
echo "  1. python3 process_with_gt.py    # Tokenize with FST"
echo "  2. python3 apply_gt2ud.py        # Convert GT→UD tags"
echo "  3. python3 verify_coverage.py    # Evaluate and report"
