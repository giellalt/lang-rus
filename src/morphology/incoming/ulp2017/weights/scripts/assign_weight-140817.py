#!usr/bin/pyhton -0
#-*-coding:utf-8 -*
import sys,csv, re


#USAGE: python3 assign_weights.py lemma_file-location POS
#POS: verbs/adjectives/nouns/conjunctions/abbreviations/interjections/prepositions/other
#other: particles

#EXAMPLE: $ python3 assign_weights-140817.py ../dataset/rnc-modern-lpos.num.ord.weight.conj.csv conjunctions
#or
#python3 assign_weight-140817.py ../dataset/lemma.al.conv.weight.csv adjectives

#lexc files are at revision 153415.

dictionary={} #contains lemmas as keys and weights as their values
lemmaFile=sys.argv[1]  #file which contains lemmas, weights and tags
pos = sys.argv[2] #information about the part of speech

#----------open and read the .csv file containing lemmas and their weights

inputFile=open(lemmaFile, "r")#the location of the file is defined here;
csvReader = csv.reader( inputFile, delimiter="," )
for row in csvReader:
    dictionary[row[0]] = row[1]

print(dictionary)

#--------open and read line by line .lexc file containing verbal stems
entry=sys.argv[2] #the type of lemma you want to analyse: verb, noun, adjective, conjunction, etc.
stemFile=open("../stems/"+entry+".lexc", "r")#location of the lexc file
lexc=stemFile.readlines()
outputFile=open("../stems/"+entry+".lexc.weight", "w+")

def insertWeight(string, weight):
    if string.count(';') == 1:
        a = string.split(";")[0] + '"weight: '+ str(weight) +'" ;' +string.split(";")[1] # string.split(";")[0] is part of the string before ";", +string.split(";")[1] is the part of the string after ";"
    elif string.count(';') > 1:
        string_list = string.split(';')
        a = ';'.join(string_list[:-1]) + '"weight: '+ str(weight) +'" ;' + string_list[-1] + " ! SEMICOLONS!" #';'.join(string_list[:-1]) extracts thepart preceding the string with weight
    else:
        raise ValueError('This line has no semicolons! ' + string)
    return a

def change_lemma(lemma):
    char=["⁶", "⁵", "⁴", "³","²","¹"]
    char2="%"
    if len(lemma)>1:
        for elt in char:#deal with cases such as то% ли, что²
            if elt in lemma:
                print("lemma before", lemma)
                lemma=lemma.replace(elt,"")
                print("lemma after", lemma)
        if char2 in lemma:
            print("lemma before", lemma)
            lemma=lemma.replace(char2,"")
            print("lemma after", lemma)
    return(lemma)

#--------iterate through lemmas and weights and assign weights to the lines from the .lexc which contains lemmas found in the dictionary
for line in lexc:
    lemma=line.strip().split(":")[0] #split the line "казнить:казн св-нсв_4b ;" into list containing ['казнить','казн св-нсв_4b ;'], line.strip().split(":")[0] is 'казнить'
    lemma=change_lemma(lemma)
    if lemma.lower() in dictionary:
        print(lemma)
        lineWeight=insertWeight(line,dictionary[lemma.lower()]) #insert the weight to the line containing the lemma
        outputFile.write(lineWeight)
    else:
        print(line)
        outputFile.write(line)
        continue

inputFile.close()
stemFile.close()
outputFile.close()

#tf4-hsl-m0032:stems upe007$ comm -23 <(sort verbs_weight.lexc) <(sort verbs.lexc)
#these commands are used in order to compare the content of the two files:
#comm -23 <(sort verbs.lexc.weight) <(sort verbs.lexc) will output only those in verbs.lexc.weight and not in verbs.lexc
#it can go either way: stems upe007$ comm -23 <(sort verbs.lex) <(sort verbs.lexc.weight)
