#!usr/bin/pyhton -0
#-*-coding:utf-8 -*


#USAGE: python3 weight-convert.py ../dataset/lemma.al.conv ../dataset/lemma.al.conv.weight.csv

import sys
import math
import csv

dataFile = sys.argv[1]
outFile=sys.argv[2]
print(outFile)
corpusSizePm=16336972.0/1000000.0 #corpus size per million
typesNbPm=32617.0/1000000.0 #number of types per million



print(dataFile)
with open(dataFile, "r") as f:
    content = f.readlines()
    content = [x.strip().split() for x in content]
    #['32617', '5.45', 'ящичек', 'noun']
f.close()

with open(outFile, "w") as f1:
    writer = csv.writer(f1, delimiter =",",quoting=csv.QUOTE_MINIMAL)
    for el in content:
        rawFreqSmooth=float(el[1])+1.0
        weight=math.log((rawFreqSmooth/(corpusSizePm + typesNbPm)), 10) + 3.0
        values=[el[2],weight,el[3]]
        writer.writerow(values)
f1.close()
