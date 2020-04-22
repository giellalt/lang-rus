#!/usr/bin/env python3

import os
from os import listdir
from os.path import isfile, join
import re
import string


inputpath = "../sample_ar_txt/"

#regex=r"^(.*?(?:ущ|ющ|ащ|ящ|вш|ш|ем|ом|им|нн|енн|ённ|т)(?:ый|ого|ому|ым|ом|ое|ого|ому|ая|ой|ую|ою|ые|ых|ым|ыми|ий|его|ему|ий|им|ем|ее|ая|ей|ую|ею|ие|их|ими))$"

regexFullForm=r"\b(.{3,}(?:ущ|ющ|ащ|ящ|[^в]ш|вш|ем|ом|им|[^её]нн|енн|ённ|т)(?:ый|ого|ому|ым|ом|ое|ого|ому|ая|ой|ую|ою|ые|ых|ым|ыми|ий|его|ему|ий|им|ем|ее|ая|ей|ую|ею|ие|их|ими)(?:ся)?)\b"

regexShortForm=r"\b((?:.{3,})(?:[^е]н|ен|[иыоя]т|ем|ом|им)(?:а|о|ы)?)\b"

outfile= open("../sample_ar_suffixes.v1.txt", "w")

for subdir, dirs, files in os.walk(inputpath):
    for file in files:
        matchesFullForm = []
        matchesShortForm= []

        fileLocation=os.path.join(subdir, file)
        inFile = open(fileLocation, "r")
        tokensLst=[]

        lines=inFile.read()
        #print(lines)
        tokensLst=lines.split()
        print(tokensLst)
        for token in tokensLst:
            matchesFullForm = re.findall(regexFullForm, token)
            matchesShortFrom = re.findall(regexShortForm, token)
            print(matchesFullForm)
            print(matchesShortFrom)
            if len(matchesFullForm) != 0:
                outfile.write(matchesFullForm[0]+"\n")
            if len(matchesShortForm) != 0:
                outfile.write(matchesShortForm[0]+"\n")

outfile.close()
