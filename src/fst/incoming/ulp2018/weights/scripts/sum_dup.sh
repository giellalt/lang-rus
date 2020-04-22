#!/bin/bash

####################################PRONOUNS####################################
#Sum duplicate row values with awk
cat duplicates_pronouns.txt | while read line; do cat rnc-modern-lpos.num | grep "P" | grep -E "\b$line\b" |  tr '[:upper:]' '[:lower:]' | LC_COLLATE=C sort -k3,3 | LC_ALL=C awk '{seen[$3]+=$2} END {for (i in seen) print seen[i],i,"P"}' ; done > pronouns.dup.freq
#remove duplicates
cat pronouns.dup.freq | awk '!array[$1,$2,$3]++' > pronouns.nodup.freq

#This line allows to see the duplicates, their freqiencies and tags
cat duplicates_pronouns.txt | while read line
do
cat rnc-modern-lpos.num.sorted | grep -E "\b$line\b" | grep "P" | LC_ALL=C sort -k3,3
done

####################################NUMERALS####################################

#MC: Sum duplicate row values with awk
cat duplicates_numerals_mc.txt | while read line; do cat rnc-modern-lpos.num.sorted | grep -E "\b$line\b" | grep "Mc" | LC_COLLATE=C sort -k3,3 | LC_ALL=C awk '{seen[$3]+=$2} END {for (i in seen) print seen[i],i,"Mc"}'; done > num_mc.dup.freq
#remove duplicates
cat num_mc.dup.freq | awk '!array[$1,$2,$3]++' > num_mc.nodup.freq

#MC:this line allows to see the duplicates, their freqiencies and tags
cat duplicates_list_propernouns.txt | while read line
do
cat rnc-modern-lpos.num.sorted | grep -E "\b$line\b" | grep "Mc" | LC_COLLATE=C sort -k3,3
done

#Mo: Sum duplicate row values with awk
cat duplicates_numerals_mo.txt | while read line;
do cat rnc-modern-lpos.num| grep -E "\b$line\b" | grep "Mo" | LC_COLLATE=C sort -k3,3 | LC_ALL=C awk '{seen[$3]+=$2} END {for (i in seen) print i, seen[i],"Mo"}'; done > num_mo.dup.freq
#remove duplicates
cat num_mo.dup.freq | awk '!array[$1,$2,$3]++' > num_mo.nodup.freq

#Mo:this line allows to see the duplicates, their freqiencies and tags
cat duplicates_numerals_mo.txt | while read line
do
cat rnc-modern-lpos.num | grep -E "\b$line\b" | grep "Mo" | LC_COLLATE=C sort -k3,3
done
#######################################PROPER NOUNS#############################

#Np: Sum duplicate row values with awk
cat duplicates_propernouns.txt | while read line
do
cat rnc-modern-lpos.num | grep -E "\b$line\b" | grep "Np" | tr '[:upper:]' '[:lower:]' | LC_COLLATE=C sort -k3,3 | LC_ALL=C awk '{seen[$3]+=$2} END {for (i in seen) print i, seen[i],"Np"}'
done > propernouns.dup.freq
#remove duplicates
cat propernouns.dup.freq | awk '!array[$1,$2,$3]++' > propernouns.nodup.freq


#Np: this line allows to see the duplicates, their freqiencies and tags
cat duplicates_propernouns.txt | while read
do
cat rnc-modern-lpos.num | grep -E "\b$line\b" | grep "Np" | LC_COLLATE=C sort -k3,3
done
#or
cat duplicates_propernouns.txt | while read; do cat rnc-modern-lpos.num |  grep -E "\b$line\b.*Np.*" ; done






#cat duplicates.sorted | grep -E "\b$line\b" | grep "Np" | tr '[:upper:]' '[:lower:]' | sort -k2,2
#|  awk '{sum+=$1;} END { print $2" "sum" "$3}1'
#| awk '{sum+=$1;} END { print sum}1'
#END { print $2" "sum"	"$3}1'
#cat duplicates.sorted | while read line
#do
#echo $line
#done
#awk '{sum+=$1;} END { print $2" "sum"	"$3}1'
#a=$(awk '{print $2;}')
#awk '{sum+=$1;} END { print '$2' sum }1'
#58 156702 вот	Q
#awk '$2 != field && field { print line } { field = $2; line = $0 }'
#awk '{sum+=$1;} END { print $2" "sum"	"$3}1'
