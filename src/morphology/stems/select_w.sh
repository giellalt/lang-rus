#!/bin/bash
#INFO: the scrips selects weights for lemmas from finite/infinite verbal wordforms (indic_inf) or participial wordforms (ptcp) from the file wverbs.lexc. It assigns these weights to entries in verbs.lexc.
#USAGE: 
#sh select_w.sh ptcp
#sh select_w.sh indic_inf

input="wverbs.lexc"
output="verbs.lexc"

if [ "$1" = "ptcp" ] ; then
cat $input | sed 's/"weight_indic_inf[^"]*" //' | sed 's/weight_ptcp/weight/' > $output
elif [ "$1" = "indic_inf" ] ; then
cat $input | sed 's/"weight_ptcp[^"]*" //' | sed 's/weight_indic_inf/weight/' > $output
else
	echo 'Try again'
fi
