#! /bin/bash

for file in *.xhtml; do
    iconv -f WINDOWS-1251 -t UTF-8 | sed -i 's/`//g' "$file" -o "${file%.xhtml}.utf8.xhtml"
done
