#!usr/bin/python3 -0
#-*-coding:utf-8 -*
import sys,csv, re

#USAGE:
#For nouns:
#cat ../dataset/lemma.al.conv.weight.csv | grep -E ",noun\s" | python3 assign_weights-030517.py nouns
#For adjectives:
#cat ../dataset/lemma.al.conv.weight.csv | grep -E ",adj\s" | python3 assign_weights-030517.py adjectives
#For verbs:
#cat ../dataset/lemma.al.conv.weight.csv | grep -E ",verb\s" | python3 assign_weights-030517.py verbs

dictionary={} #contains lemmas as keys and weights as their values
lst=[]

#----------read the .csv file containing lemmas and their weights from raw input

for row in csv.reader(iter(sys.stdin.readline, '')):#reading csv file from the stream
    print(row)
    #row[2]=float(row[2].replace(',','.'))#replace "," with ".": 2,24873066021786 with 2.24873066021786
    if "," in row[0]:
        row_split=row[0].split(",") #to deal with cases such as "уж, уже, узкий" to split it into separate words
        for el in row_split:
            dictionary[el] = row[1]
    else:
        dictionary[row[0]] = row[1] # key:север, value: 2,0003
        #'первозданный': ['2.508596147048128', 'adj'], 'пантера': ['2.308406458020636', 'noun']
print(dictionary)


#--------open and read line by line .lexc file containing verbal stems
entry=sys.argv[1] #the type of lemma you want to analyse: verb, noun or adjective
stemFile=open("../stems/"+entry+".lexc", "r")#location for the output file
verblexc=stemFile.readlines()
outputFile=open("../stems/"+entry+".lexc.weight", "w")

def insertWeight(string, weight):
    if string.count(';') == 1:
        a = string.split(";")[0] + '"weight: '+ str(weight) +'" ;' +string.split(";")[1] # string.split(";")[0] is part of the string before ";", +string.split(";")[1] is the part of the string after ";"
    elif string.count(';') > 1:
        string_list = string.split(';')
        a = ';'.join(string_list[:-1]) + '"weight: '+ str(weight) +'" ;' + string_list[-1] + " ! SEMICOLONS!" #';'.join(string_list[:-1]) extracts thepart preceding the string with weight
    # elif string.count('weight') > 1:#these are the cases, when the weights are already inserted and you want to replace their value with the new one
    #     a = string.split('weight: ')[0] + '"weight: '+ str(weight) +'" ;' +string.split('"')[1] #
    #     #q ='работящий:работя́щ п_a "weight: 2.4323659507373856" ; ! Z 4a'
    #     #>>> q.split('weight: ')[0]
    #     #'работящий:работя́щ п_a "'
    else:
        raise ValueError('This line has no semicolons! ' + string)
    return a

#--------iterate through lemmas and weights and assign weights to the lines from the .lexc which contains lemmas found in the dictionary
for line in verblexc:
    verb=line.strip().split(":")[0] #split the line "казнить:казн св-нсв_4b ;" into list containing ['казнить','казн св-нсв_4b ;'], line.strip().split(":")[0] is 'казнить'
    #print(verb)
    if verb in dictionary:
        #print(verb)
        #print(dictionary[verb])
        lineWeight=insertWeight(line,dictionary[verb]) #insert the weight to the line containing the lemma
        outputFile.write(lineWeight)
    else:
        outputFile.write(line)

stemFile.close()
outputFile.close()


#tf4-hsl-m0032:stems upe007$ comm -23 <(sort verbs_weight.lexc) <(sort verbs.lexc)
#these commands are used in order to compare the content of the two files:
#comm -23 <(sort verbs.lexc.weight) <(sort verbs.lexc) will output only those in verbs.lexc.weight and not in verbs.lexc
#it can go either way: stems upe007$ comm -23 <(sort verbs.lex) <(sort verbs.lexc.weight)
