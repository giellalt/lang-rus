#!usr/bin/pyhton -0
#-*-coding:utf-8 -*
import sys,csv, re

#USAGE: python3 assign_weights.py lemma_file-location POS
#POS: verbs/adjectives/nouns
#lemma_file-location: ../dataset/lemma.al.conv.weight.csv


dictionary={} #contains lemmas as keys and weights as their values

lemmaFile=sys.argv[1]
#----------open and read the .csv file containing lemmas and their weights
inputFile=open(lemmaFile, "r")#the location of the file is defined here; it is also possible to save the location of the file in sys.argv[2]
csvReader = csv.reader( inputFile, delimiter="," )
for row in csvReader:
    #row[2]=float(row[2].replace(',','.'))#replace "," with ".": 2,24873066021786 with 2.24873066021786
    if "," in row[0]:
        row_split=row[0].split(",") #deal with cases such as "уж, уже, узкий" to split it into separate words
        for el in row_split:
            dictionary[el] = row[1]
    else:
        dictionary[row[0]] = row[1] # key:север, value: 2,0003


#--------open and read line by line .lexc file containing verbal stems
entry=sys.argv[2] #the type of lemma you want to analyse: verb, noun or adjective
stemFile=open("../stems/"+entry+".lexc", "r")#location for the output file
verblexc=stemFile.readlines()
outputFile=open("../stems/"+entry+".lexc.weight", "w")

def insertWeight(string, weight):
    if string.count(';') == 1:
        a = string.split(";")[0] + '"weight: '+ str(weight) +'" ;' +string.split(";")[1] # string.split(";")[0] is part of the string before ";", +string.split(";")[1] is the part of the string after ";"
    elif string.count(';') > 1:
        string_list = string.split(';')
        a = ';'.join(string_list[:-1]) + '"weight: '+ str(weight) +'" ;' + string_list[-1] + " ! SEMICOLONS!" #';'.join(string_list[:-1]) extracts thepart preceding the string with weight
    else:
        raise ValueError('This line has no semicolons! ' + string)
    return a

#--------iterate through lemmas and weights and assign weights to the lines from the .lexc which contains lemmas found in the dictionary
for line in verblexc:
    verb=line.strip().split(":")[0] #split the line "казнить:казн св-нсв_4b ;" into list containing ['казнить','казн св-нсв_4b ;'], line.strip().split(":")[0] is 'казнить'
    if verb in dictionary:
        print(verb)
        print(dictionary[verb])
        lineWeight=insertWeight(line,dictionary[verb]) #insert the weight to the line containing the lemma
        outputFile.write(lineWeight)
    else:
        outputFile.write(line)

inputFile.close()
stemFile.close()
outputFile.close()


#tf4-hsl-m0032:stems upe007$ comm -23 <(sort verbs_weight.lexc) <(sort verbs.lexc)
#these commands are used in order to compare the content of the two files:
#comm -23 <(sort verbs.lexc.weight) <(sort verbs.lexc) will output only those in verbs.lexc.weight and not in verbs.lexc
#it can go either way: stems upe007$ comm -23 <(sort verbs.lex) <(sort verbs.lexc.weight)
