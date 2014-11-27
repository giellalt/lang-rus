#!/bin/bash

for f in *.src
do
  name=$(echo $f | rev | cut -c 5- | rev)
  echo "Processing $name file..."
  cat $name.src  | apertium-destxt | hfst-proc -w ~/main/langs/rus/tools/mt/apertium/analyser-mt-apertium-desc.und.hfstol 2>/dev/null | cg-proc -n -1 -w ~/apertium-rus/rus.rlx.bin  | gsed 's/<@[A-Za-z→←]\+>//g' | hfst-proc -n ~/main/langs/rus/tools/mt/apertium/generator-mt-apertium-norm.hfstol  | apertium-retxt > $name.tst
done
echo "Done!"