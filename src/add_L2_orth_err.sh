#!/bin/bash

# usage: ./add_L2_orth_err.sh <src_transducer> <tag1> <tag2> <tag3> ...

set -x

src_tr=$1
shift
tags="$*"
echo "Adding the following tags to ${src_tr} in parallel: ${tags}"

tmp_tr1=add_L2_orth_err.tmp1.hfst
tmp_tr2=add_L2_orth_err.tmp2.hfst

compile_fst () {
    hfst-regexp2fst --format=foma -v -S orthography/L2_$1.regex \
        | hfst-compose-intersect -1 - -2 ${src_tr} \
        | hfst-subtract -F -1 - -2 ${src_tr} \
        > $1.uniq.tmp.hfst
    echo "[ ? -> ... \"\+Err\/L2_$1\" || _ .#. ]" \
        | hfst-regexp2fst --format=foma -v -S \
        | hfst-compose-intersect -v -1 $1.uniq.tmp.hfst -2 - \
        | hfst-prune-alphabet \
        | hfst-remove-epsilons \
        | hfst-determinize \
        | hfst-minimize \
        > $1.tmp.hfst
    rm $1.uniq.tmp.hfst
}

for tag in ${tags}
do
    compile_fst ${tag} &
done
wait


cp ${src_tr} ${tmp_tr1}
for tag in ${tags}
do
    hfst-disjunct -1 ${tmp_tr1} -2 ${tag}.tmp.hfst \
        > ${tmp_tr2}
    mv ${tmp_tr2} ${tmp_tr1}
    # rm ${tag}.tmp.hfst
done

hfst-prune-alphabet ${tmp_tr1} \
    | hfst-remove-epsilons \
    | hfst-determinize \
    | hfst-minimize \
    > ${src_tr}

rm ${tmp_tr1}
