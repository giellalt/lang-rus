#!/bin/bash

# usage: ./add_L2_orth_err.sh <src_transducer> <tag1> <tag2> <tag3> ...

# TODO: probably more efficient way to clear metadata than `hfst-fst2txt | hfst-txt2fst` (hfst-edit-metadata?)

set -x

src_tr=$1
shift
tags="$*"
echo "Adding the following tags to ${src_tr} in parallel: ${tags}"

tmp_tr1=add_L2_orth_err.tmp1.hfst
tmp_tr2=add_L2_orth_err.tmp2.hfst

for tag in ${tags}
do
    hfst-regexp2fst --format=foma -v -S orthography/L2_${tag}.regex \
        | hfst-compose-intersect -1 - -2 ${src_tr} \
        | hfst-subtract -F -1 - -2 ${src_tr} \
        > ${tag}.uniq.tmp.hfst
    echo "[ ? -> ... \"\+Err\/L2_${tag}\" || _ .#. ]" \
        | hfst-regexp2fst --format=foma -v -S \
        | hfst-compose-intersect -v -1 ${tag}.uniq.tmp.hfst -2 - \
        | hfst-prune-alphabet \
        | hfst-remove-epsilons \
        | hfst-determinize \
        | hfst-minimize \
        | hfst-fst2txt \
	| hfst-txt2fst --format=foma \
        > ${tag}.tmp.hfst
done


cp ${src_tr} ${tmp_tr1}
for tag in ${tags}
do
    hfst-disjunct -1 ${tmp_tr1} -2 ${tag}.tmp.hfst \
        > ${tmp_tr2}
    mv ${tmp_tr2} ${tmp_tr1}
done

hfst-prune-alphabet ${tmp_tr1} \
    | hfst-remove-epsilons \
    | hfst-determinize \
    | hfst-minimize \
    | hfst-fst2txt \
    | hfst-txt2fst --format=foma \
    > ${src_tr}

rm ${tmp_tr1} ${tag}.uniq.tmp.hfst ${tag}.tmp.hfst
