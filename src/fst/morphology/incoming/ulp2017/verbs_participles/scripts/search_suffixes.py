#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
import re
import string
mypath="../snjatnik_texts/"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#regex=r"^(.*?(?:ущ|ющ|ащ|ящ|вш|ш|ем|ом|им|нн|енн|ённ|т)(?:ый|ого|ому|ым|ом|ое|ого|ому|ая|ой|ую|ою|ые|ых|ым|ыми|ий|его|ему|ий|им|ем|ее|ая|ей|ую|ею|ие|их|ими))$"

regexFullForm=r"\b((?:.{3,})(?:ущ|ющ|ащ|ящ|вш|ш|ем|ом|им|нн|енн|ённ|т)(?:ый|ого|ому|ым|ом|ое|ого|ому|ая|ой|ую|ою|ые|ых|ым|ыми|ий|его|ему|ий|им|ем|ее|ая|ей|ую|ею|ие|их|ими)(?:ся)?)\b"

regexShortForm=r"\b((?:.{3,})(?:н|ен|[иыоя]т|ем|ом|им)(?:а|о|ы)?)\b"

outfile= open("../snjatnik_texts_out.txt", "w")

for f in onlyfiles:
    tokensLst=[]
    infile = open("../snjatnik_texts/"+f, "r")
    lines=infile.read()
    #print(lines)
    tokensLst=lines.split()
    #print(tokensLst)
    for token in tokensLst:
        matchesFullForm = re.findall(regexFullForm, token)
        matchesShortFrom = re.findall(regexShortForm, token)
        print(matchesFullForm)
        print(matchesShortFrom)
        for val1, val2 in zip(matchesFullForm,matchesShortFrom):
            if len(val1)>0 or len(val2)>0:
                outfile.write(val1+"\n")
                outfile.write(val2+"\n")

outfile.close()
