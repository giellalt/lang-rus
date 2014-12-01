#!/bin/bash

GTROOT=$1
ALANGS=$2
SED=sed

# Filetypes
#   .ref - stressed gold standard
#   .src - unstressed
#   .tst - stressed
#       .GTnoCGguess - Giellatekno FST > blindly select the first reading
#       .GTnoCGsure - Giellatekno FST > resolve stress-irrelevant ambiguity, abstain from remaining ambiguity
#       .GTCGguess - Giellatekno FST > CG > blindly select the first reading
#       .GTCGsure - Giellatekno FST > CG > resolve stress-irrelevant ambiguity, abstain from remaining ambiguity
#       .RG - RusGram plugin       

echo "Generating .src files from .ref files..."
for f in *.ref
do
  name=$(echo $f | rev | cut -c 5- | rev)
  echo -e "\t generating $name.src ..."
  cat $name.ref | $SED 's/\o314\o201//g' | $SED 's/ё/е/g' | $SED 's/Ё/Е/g' > $name.src
done

for f in *.src
do
  name=$(echo $f | rev | cut -c 5- | rev)
  echo "Processing $name.src ..."
#       .GTnoCGguess - Giellatekno FST > blindly select the first reading
# TODO pipeline
#       .GTnoCGsure - Giellatekno FST > resolve stress-irrelevant ambiguity, abstain from remaining ambiguity
  echo -e "\tgenerating $name.GTnoCGsure.tst ..."
  cat $name.src  | apertium-destxt | hfst-proc -w $GTROOT/langs/rus/tools/mt/apertium/analyser-mt-apertium-desc.und.hfstol 2>/dev/null | python3.4 show-all-rus.py $GTROOT/langs/rus/tools/mt/apertium/generator-mt-apertium-norm.hfstol | apertium-retxt > test_files/$name.GTnoCGsure.tst
#       .GTCGguess - Giellatekno FST > CG > blindly select the first reading
  echo -e "\tgenerating $name.GTCGguess.tst ..."
  cat $name.src  | apertium-destxt | hfst-proc -w $GTROOT/langs/rus/tools/mt/apertium/analyser-mt-apertium-desc.und.hfstol 2>/dev/null | cg-proc -n -1 -w $ALANGS/apertium-rus/rus.rlx.bin  | $SED 's/<@[A-Za-z→←]\+>//g' | hfst-proc -n $GTROOT/langs/rus/tools/mt/apertium/generator-mt-apertium-norm.hfstol | apertium-retxt > test_files/$name.GTCGguess.tst
#       .GTCGsure - Giellatekno FST > CG > resolve stress-irrelevant ambiguity, abstain from remaining ambiguity
# TODO pipeline
done

# concatenate results for each condition
cat *.ref > all.ref
cat *.src > all.src
cat test_files/*.GTnoCGguess.tst > test_files/all.GTnoCGguess.tst
cat test_files/*.GTnoCGsure.tst > test_files/all.GTnoCGsure.tst
cat test_files/*.GTCGguess.tst > test_files/all.GTCGguess.tst
cat test_files/*.GTCGsure.tst > test_files/all.GTCGsure.tst
cat test_files/*.RG.tst > test_files/all.RG.tst

echo "Done!"
