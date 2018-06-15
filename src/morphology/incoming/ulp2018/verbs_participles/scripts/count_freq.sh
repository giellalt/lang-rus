#files = "../experiments/paradigm/summary-"*txt
[ -e "$folder"freq.txt ] && rm "$folder"freq.txt

for fic in ../experiments/paradigm/pos-*txt
  do
    cat $fic | sort -f | uniq -c | sort -nr | head  -30 >> ./freq/"$folder"freq.txt #saves the 30 most frequent instances of wordforms
    echo "------------------------------------------------" >> "$folder"freq.txt
  done
