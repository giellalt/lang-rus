#! /bin/bash


for file in ../sample_ar/TEXTS/*/*.xhtml; do
     iconv -f WINDOWS-1251 -t UTF-8 "$file" |sed 's/`//g' | sed 's/"windows-1251"/"utf-8"/g' > "${file%.xhtml}.utf8.xhtml";
 done


#for file in *.xhtml; do
 #   iconv -f WINDOWS-1251 -t UTF-8 "$file" > "${file%.xhtml}.utf8.xhtml"
#done

#-o
# sed -i 's/`//g'
