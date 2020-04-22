L2_ERRS="ii FV NoFV Pal SRo SRy"

echo "##### rebuilding twolc source files from rules/ ..."
bash make-twolc.sh

echo "##### compiling the standard two-level phonology..."
test -r rus-phon.hfst && /usr/local/bin/hfst-twolc -v \
                        --format=openfst-tropical \
                        -i rus-phon.twolc \
                        -o rus-phon.hfst

echo "##### compiling the raw standard generator FST..."
/usr/local/bin/hfst-determinize -v  ../morphology/lexicon.hfst \
    | /usr/local/bin/hfst-minimize -v  \
    | /usr/local/bin/hfst-compose-intersect  \
    -v  \
    -2 rus-phon.hfst \
    | /usr/local/bin/hfst-minimize -v  \
    -o generator-raw-gt-desc.tmp1.hfst

for tag in ${L2_ERRS}
do
    echo "##### compiling add-tag-err-L2_${tag} FST..."
    /usr/local/bin/hfst-regexp2fst  --format=openfst-tropical \
        --xerox-composition=ON -v -S add-tag-err-L2_${tag}.regex \
        -o add-tag-err-L2_${tag}.hfst

    echo "##### compiling the ${tag} two-level phonology..."
    /usr/local/bin/hfst-twolc -v \
        --format=openfst-tropical -i rus-phon-err-L2_${tag}.twolc \
        -o rus-phon-err-L2_${tag}.hfst

    echo "##### compiling the raw ${tag} generator FST..."
    /usr/local/bin/hfst-determinize -v  ../morphology/lexicon.hfst \
        | /usr/local/bin/hfst-minimize -v  \
        | /usr/local/bin/hfst-compose-intersect  \
        -v  \
        -2 rus-phon-err-L2_${tag}.hfst \
        | /usr/local/bin/hfst-minimize -v  \
        -o generator-raw-gt-desc-err-L2_${tag}.tmp1.hfst

    echo "##### removing entries in ${tag} that overlap with the std FST..."
    /usr/local/bin/hfst-subtract generator-raw-gt-desc-err-L2_${tag}.tmp1.hfst \
        generator-raw-gt-desc.tmp1.hfst \
        > generator-raw-gt-desc-err-L2_${tag}.tmp2.hfst

    echo "##### composing ${tag} with some filters for the generator..."
    /opt/local/libexec/gnubin/printf "read regex \
                @\"../filters/reorder-subpos-tags.hfst\"   \
            .o. @\"../filters/reorder-semantic-tags.hfst\" \
            .o. @\"../filters/remove-mwe-tags.hfst\"       \
            .o. @\"generator-raw-gt-desc-err-L2_${tag}.tmp2.hfst\" \
            ;\n\
         save stack generator-raw-gt-desc-err-L2_${tag}.tmp.hfst\n\
         quit\n" | /usr/local/bin/hfst-xfst -p -v --format=openfst-tropical

    cp -f generator-raw-gt-desc-err-L2_${tag}.tmp.hfst generator-raw-gt-desc-err-L2_${tag}.hfst
    cp generator-raw-gt-desc-err-L2_${tag}.hfst analyser-raw-gt-desc-err-L2_${tag}.hfst
    /opt/local/libexec/gnubin/printf "read regex \
                @\"../filters/remove-area-tags.hfst\"                \
            .o. @\"../filters/remove-dialect-tags.hfst\"             \
            .o. @\"../filters/remove-number-string-tags.hfst\"       \
            .o. @\"../filters/remove-usage-tags.hfst\"               \
            .o. @\"../filters/remove-semantic-tags.hfst\"            \
            .o. @\"../filters/remove-orig_lang-tags.hfst\"           \
            .o. @\"../filters/remove-orthography-tags.hfst\"         \
            .o. @\"../filters/remove-Orth_IPA-strings.hfst\"         \
            .o. @\"analyser-raw-gt-desc-err-L2_${tag}.hfst\" \
            .o. @\"../orthography/downcase-derived_proper-strings.compose.hfst\" \
            .o. @\"../filters/remove-hyphenation-marks.hfst\"        \
            .o. @\"../filters/remove-infl_deriv-borders.hfst\"       \
            .o. @\"../filters/remove-word-boundary.hfst\"            \
            ; \n\
            define fst \n\
            set flag-is-epsilon ON\n\
            read regex fst \
            .o. @\"../orthography/inituppercase.compose.hfst\"       \
            .o. @\"../orthography/spellrelax.compose.hfst\"          \
            ;\n\
         save stack analyser-gt-desc-err-L2_${tag}.tmp.hfst\n\
         quit\n" | /usr/local/bin/hfst-xfst -p -v --format=openfst-tropical

    echo "##### making stress optional for ${tag}..."
    /opt/local/libexec/gnubin/printf "read regex @\"analyser-gt-desc-err-L2_${tag}.tmp.hfst\" \
            .o. @\"../orthography/destressOptional.compose.hfst\" \
            ;\n \
            invert net\n \
            save stack analyser-gt-desc-err-L2_${tag}.tmp1.hfst\n \
            quit\n" | /usr/local/bin/hfst-xfst -p -v --format=openfst-tropical


    echo "##### adding +Err tags to the ${tag} transducer..."
    hfst-compose-intersect -v -1 analyser-gt-desc-err-L2_${tag}.tmp1.hfst \
                          -2 add-tag-err-L2_${tag}.hfst \
                          -o analyser-gt-desc-err-L2_${tag}.tmp2.hfst
done

echo "##### combining FSTs..."
cp ../analyser-gt-desc.hfst analyser-gt-desc.hfst
for tag in ${L2_ERRS}
do
    /usr/local/bin/hfst-disjunct -1 analyser-gt-desc.hfst \
                                 -2 analyser-gt-desc-err-L2_${tag}.tmp2.hfst \
                                 > err.tmp.hfst
    mv err.tmp.hfst analyser-gt-desc.hfst
done
hfst-minimize analyser-gt-desc.hfst > fst.tmp
mv fst.tmp analyser-gt-desc.hfst
hfst-fst2fst -w -i analyser-gt-desc.hfst -o analyser-gt-desc.hfstol

rm *tmp*
