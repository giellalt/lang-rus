#!/usr/bin/env python
# -*- coding: utf-8 -*-


# RESERVED WORDS/CHARACTERS IN HFST TWOLC
# Alphabet  Definitions  Rules  Sets 
# !         ;            ?      :        
# _         |            =>     <=        
# <=>       /<=          [      ]
# (         )            *      +
# $         $.           ~      <
# >         -            "      \
# =         0            ^      #
# %

# RESERVED WORDS/CHARACTERS IN HFST LEXC
# 

# ZALIZNJAK CODES
# м мо с со ж жо мо-жо мн. мн. неод. мн. одуш. мн. от (gender/animacy/tantumness)
# 0-8 nominal stem type
# * - fleeting vowel ** - кружочек means special stem changes, like имя, христианин, etc.
# a-f - stress pattern
# irregular patterns circle1-circle9 (pg 42,43,53 or 77?)
# ё
# 
# - hypothetical                                                    {-}
# П2 Р2                                                             {^П2 ^Р2}
# §1-12 irregular patterns (see pg 73)
# TRIANGLE - irregular forms (pp. 16, 35, 89)
# DIAMOND - irregularities in particular idioms
# : shows that word is only used in the listed idioms
# // equivalent variants, with scope delimited by , ; : TRIANGLE DIAMOND HATCHED-CIRCLE []
# The order of equivalent forms conveys normativity
# [] facultative variant
# 
# Delimiters: , ; : TRIANGLE DIAMOND HATCHED-CIRCLE 

import codecs
import re

# RESERVED CHARACTERS IN FOMA (hfst's default lexc compiler)
# ! " # $ % & ( ) * + , - . / 0 : ; < > ? [ \ ] ^ _ ` { | } 
# ~ ¬ ¹ × Σ ε ⁻ ₁ ₂ → ↔ ∀ ∃ ∅ ∈ ∘ ∥ ∧ ∨ ∩ ∪ ≤ ≥ ≺ ≻
# Of those listed above, only the following are present in the original Zaliznjak
# ! " % ( ) * , - . / 0 : ; < > ? [ ] ^ _ { }  # USED IN ZALIZNJAK
# The following are ASCII characters that are not reserved in foma
#   ' 1 2 3 4 5 6 7 8 9 = @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z 
# The following are ASCII characters that are not reserved in foma, 
# and are not used in the original Zaliznjak. (== [A-Za-z])
# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z
# Of these, only the following are unlikely to be confused with Russian symbols
# F G I J L N Q R S V W Z b d f g h i j l q r s t v z
# In each pair, the reserved character is first, what it is transformed into is given 2nd.
foma_trans   = [(u"!" , u"z"), 
                (u"[" , u"["), 
                (u"]" , u"]"), 
                (u'"' , u"v"), 
                (u"%" , u"%"), 
                (u"(" , u"[["), 
                (u")" , u"[["), 
                (u"*" , u"*"), 
                (u"," , u","), 
                (u"-" , u"-"), 
                (u"." , u"."), 
                (u"/" , u"/"), 
                (u"0" , u"0"), 
                (u":" , u"_AS_IN_"), 
                (u";" , u"_OR_"), 
                (u"<" , u"["), 
                (u">" , u"]"), 
                (u"?" , u"defect"), 
                (u"^" , u"_INCL_"), 
                (u"_" , u"_"), 
                (u"{" , u"[[["), 
                (u"}" , u"]]]")]

def foma_replace ( myinput ) :
    for i,j in foma_trans :
        myinput = myinput.replace(i,j)
    return myinput

def combiner ( typelist , codelist ) :
    outputList = []
    for i in typelist :
        for j in codelist :
            outputList.extend([i+u" "+j])
    return outputList

Masc = [u"М", u"МО"]
MascFcodes = [u"1*А", u"1*В", u"1*Е", u"2*А", u"2*В", u"2*Е", u"3*А", u"3*В", u"3*Д", u"5*А", u"5*В", u"6*А", u"6*В"]
Fem = [u"Ж", u"ЖО"]
Fem8codes = [u"8*В'", u"8*Е"]
Pro = [u"МС"]
ProFcodes = [u"1*В", u"2*В", u"6*В"]
MiscM = []
Fgroup1 = combiner(Masc,MascFcodes) + combiner(Fem,Fem8codes) + combiner (Pro,ProFcodes) + MiscM
# Fgroup1 = [ u"М 1*А" , u"М 1*В" , u"М 1*Е" , u"М 2*А" , u"М 2*В" , u"М 2*Е" , 
#             u"М 3*А" , u"М 3*В" , u"М 5*А" , u"М 5*В" , u"М 6*А" , u"М 6*В" , 
#             u"МО 1*А" , u"МО 1*В" , u"МО 1*Е" , u"МО 2*А" , u"МО 2*В" , u"МО 2*Е" , 
#             u"МО 3*А" , u"МО 3*В" , u"МО 5*А" , u"МО 5*В" , u"МО 6*А" , u"МО 6*В" , 
#             u"Ж 8*В'" , u"Ж 8*Е" , u"ЖО 8*В'" , u"ЖО 8*Е" , 
#             u"МС 1*В" , u"МС 2*В" , u"МС 6*В"]

FemFcodesS = [u"1*В", u"1*Е", u"1*Ф", u"2*В", u"2*Е", u"2*Ф", u"3*В", u"3*Ф", u"3*Ф'", u"5*В", u"6*В"]
Neut = [u"С", u"СО"]
NeutFcodesS = [u"1*В", u"1*С", u"3*В", u"3*С", u"5*В", u"5*С", u"5*Ф", u"6*В"]
Adj = [u"П"]
AdjFcodesS = [u"1*А/В", u"1*В"]
MiscS = [u"МН. <М 3*В>",u"МН. <М 5*В>"] # These aren't working
Fgroup2stressed = combiner(Fem,FemFcodesS) + combiner(Neut,NeutFcodesS) + combiner(Adj,AdjFcodesS) + MiscS

FemFcodesU = [u"1*А", u"1*Д", u"2*А", u"2*Д", u"2*Д'", u"3*А", u"3*Д", u"5*А", u"5*Д", u"6*А", u"6*Д"]
NeutFcodesU = [u"1*А", u"1*Д", u"3*А", u"3*Д", u"5*А", u"5*Д", u"6*А", u"6*Д"]
AdjFcodesU = [u"1*А", u"1*А'", u"1*А/С", u"1*А/С'", u"1*А/С''", u"1*В/С'", u"1*В/С''", u"2*А", u"3*А", u"3*А'", u"3*А/С", u"3*А/С'", u"3*А/С''"]
MiscU = [u"МН. <М 2*А>",u"МН. <М 3*А>",u"МН. <М 5*А>"] # These aren't working
Fgroup2unstressed = combiner(Fem,FemFcodesU) + combiner(Neut,NeutFcodesU) + combiner(Adj,AdjFcodesU) + MiscU

def fleeter ( myinput , mycode ) : # decide whether word belongs to Fgroup1 (Mfleeter) or Fgroup2 (Ffleeter, stressed or unstressed)
    # print "Running fleeter...",myinput,mycode
    tester1 = 0
    for i in Fgroup1 :
        if i in mycode :
            tester1 += 1
            #print i,
    tester2 = 0
    for i in Fgroup2stressed :
        if i in mycode :
            tester2 += 1
            #print i,
    tester3 = 0
    for i in Fgroup2unstressed :
        if i in mycode :
            tester3 += 1
            #print i,
    if tester1 > 0 :
        return Mfleeter (myinput,mycode)
    elif tester2 > 0 :
        return Ffleeter (myinput,mycode,stress="stressed")
    elif tester3 > 0 :
        return Ffleeter (myinput,mycode,stress="unstressed")
    else :
        print "Warning: Fleeting vowel added with FEM/NEUT/PL UNSTRESSED conventions (FV tag) :",myinput,mycode,
        return Ffleeter (myinput,mycode,stress="unstressed",confidence=0)

def Mfleeter (myinput,mycode) : # add (or don't add) ь or й to "alternate" with fleeting vowel
    # print "Running Mfleeter...",myinput,mycode,">>>>",
    Findex = myinput.find(u"F")
    if u"Fо" in myinput :
        return myinput
    elif (u"Fе" in myinput or u"Fё" in myinput) :
        if myinput[Findex-1] in u"аэоуыяеёюиа́э́о́у́ы́я́е́ю́и́" :
            return myinput[:Findex]+u"й"+myinput[Findex:]
        elif myinput[Findex-1] == u"л" :
            return myinput[:Findex]+u"ь"+myinput[Findex:]
        elif myinput[Findex-1] in u"бвгдзйкмнпрстфх" and (u"М 3*" in mycode or u"МО 3*" in mycode):
            return myinput[:Findex]+u"ь"+myinput[Findex:]
        else :
            return myinput
    else :
        print "Warning: Fleeting vowel added with FEM/NEUT/PL UNSTRESSED conventions (FV tag) :",myinput,mycode,
        return Ffleeter (myinput,mycode,stress="unstressed",confidence=0)

    # MAKE WARNINGS PRINT AT THE BOTTOM OF OUTPUT FILES!


def Ffleeter (myinput,mycode,stress,confidence=1) :
    # print "Running Ffleeter...",myinput,mycode,stress,">>>>",
    Findex = myinput.find(u"F")
    if u"6*" in mycode :
        if stress == "unstressed" :
            TheVowel = u"и"
        elif stress == "stressed" :
            TheVowel = u"е́"
    elif ( myinput[Findex-1] == u"ь" or myinput[Findex-1] == u"й" ) and myinput[Findex+1] == u"ц" :
        if stress == "unstressed" :
            TheVowel = u"е"
        elif stress == "stressed" :
            TheVowel = u"е́"
    elif ( myinput[Findex-1] == u"ь" or myinput[Findex-1] == u"й" ) and myinput[Findex+1] != u"ц" :
        if stress == "unstressed" :
            TheVowel = u"е"
        elif stress == "stressed" :
            TheVowel = u"ё"
    elif myinput[Findex-1] == u"к" or myinput[Findex-1] == u"г" or myinput[Findex-1] == u"х" :
        if stress == "unstressed" :
            TheVowel = u"о"
        elif stress == "stressed" :
            TheVowel = u"о́"
    elif myinput[Findex-1] == u"ж" or myinput[Findex-1] == u"ш" or myinput[Findex-1] == u"щ" or myinput[Findex-1] == u"ч" or myinput[Findex-1] == u"ц":
        if stress == "unstressed" :
            TheVowel = u"е"
        elif stress == "stressed" :
            TheVowel = u"о́"
    elif myinput[Findex+1] == u"к" or myinput[Findex+1] == u"г" or myinput[Findex+1] == u"х" :
        if stress == "unstressed" :
            TheVowel = u"о"
        elif stress == "stressed" :
            TheVowel = u"о́"
    else :
        if stress == "unstressed" :
            TheVowel = u"е"
        elif stress == "stressed" :
            TheVowel = u"ё"
    if confidence == 0 :
        print "\t>>>>>\t"+myinput[:Findex+1]+TheVowel+myinput[Findex+1:]+u"FV"
        return myinput[:Findex+1]+TheVowel+myinput[Findex+1:]+u"FV"
    return myinput[:Findex+1]+TheVowel+myinput[Findex+1:]

def stress_shifter ( myinput , mycode ) : # called by stresser2(); places stress mark on stem for Д and Ф patterns
    backwar = myinput[-3::-1]
    Vcount = Vowel.findall( backwar )
    if u"ЙО" in mycode and Vcount[0] == u"е" :
        V2index = len(myinput)-(backwar.find(Vcount[0])+3)
        myinput = myinput[:V2index]+u"ё"+myinput[V2index+1:]
    else :
        V2index = len(myinput)-(backwar.find(Vcount[0])+2)
        myinput = myinput[:V2index]+u"\u0301"+myinput[V2index:]
    if u"F" in myinput :
        return fleeter (myinput,mycode)
    else :
        return myinput

NSSfinder = re.compile(u"[1-8]\\*?[ДФ]")

def stresser2 ( myinput , mycode ) : # called by stresser(); places secondary stress (grave accent)
    # print "Running stresser2...",myinput,mycode
    position = myinput.find('>')
    if position == -1 :
        if NSSfinder.search(mycode) :
            return stress_shifter(myinput,mycode)
        elif u"F" in myinput :
            return fleeter (myinput,mycode)
        else :
            return myinput
    elif position > -1 :
        inputList = list(myinput)
        inputList[position] = inputList[position+1]
        inputList[position+1] = u'\u0300'
        return stresser2 (''.join(inputList),mycode)

def stresser ( myinput , mycode ) : # places primary stress (acute accent), then calls stresser2 to place 2ndary stress.
    # print "Running stresser...",myinput,mycode
    Vcount = Vowel.findall( myinput )
    if len(Vcount) == 1 :
        myoutput = myinput.replace(u'<','')
        myoutput = myoutput[:myoutput.index(Vcount[0])+1]+u'\u0301'+myoutput[myoutput.index(Vcount[0])+1:]
        return myoutput
    position = myinput.find('<')
    if position == -1 :
        return stresser2 (myinput,mycode)
    if position > -1 :
        inputList = list(myinput)
        if inputList[position+1] == u'ё' :
            del inputList[position]
        else :
            inputList[position] = inputList[position+1]
            inputList[position+1] = u'\u0301'
        return stresser (''.join(inputList),mycode)

def CodeCleaner ( myinput ) : # generates the (preliminary) name of the continuation class
    output = myinput.split("%")[0]
    output = output.split(":")[0]
    output = re.sub( "\(_.*?_\)" , "" , output )                 # remove irrelevant semantic labels
    output = re.sub( "\\[\\/\\/.*?\\]" , "" , output )            # remove variant labels
    output = re.sub( "\\<(.*?)\\>" , "[\\1]" , output )         # change <  > to [ ]   
    output = foma_replace( output )
    return output.strip()

def NStemCodeStrip ( myinput ) : # For nouns, remove stem labels and fleeting vowel markers from continuation class name generated by CodeCleaner
    output = re.sub( " [1-7]" , " " , myinput )
    output = re.sub( "\\*" , "" , output )
    return output

def A_stemmer ( instem , code ) : # generates lexical stem for adjectives (including substantivized)
    # print "Running A_stemmer...",instem,code
    instem = instem[:-2]
    if instem[-1:] == u"<" :
        instem = instem[:-1]
    if u'***' in code or ( not  '**' in code and '*' in code ) :    # If the code indicates that there is a fleeting vowel
        instem = list(instem)
        instem.insert(len(instem)-1,u"F")
        instem = ''.join(instem)
    return stresser ( instem , code )

Cons = re.compile(u"[бвгджзйклмнпрстфхцчшщ]")
SoftSign = re.compile(u"[ь]")
Vowel = re.compile(u"[аэоуыяеёюи]")
VowEnd = re.compile(u"[аяоёеыи]")
StressRE = re.compile(u"[<>]")

def N_stemmer ( instem , code ) :
    # print "Running N_stemmer...",instem,code
    if u"<П " not in code and u"<П, " not in code :
        if u'***' in code or ( not  '**' in code and '*' in code ) :    # If the code indicates that there is a fleeting vowel
            instem = instem[::-1]
            Cindex = Cons.search(instem)
            SSindex = SoftSign.search(instem)
            Vindex = VowEnd.search(instem)
            Sindex = StressRE.search(instem)
            if Cindex.start() > Vindex.start() : # if the stem ends in a vowel...
                if SSindex : # if there is a soft sign in the word
                    if Cindex.start() < SSindex.start() : # if the soft sign is before the final consonant
                        Findex = Cindex.start()+1
                    elif Cindex.start() > SSindex.start() : # if the soft sign is after the final consonant
                        Findex = SSindex.start()+1
                        instem = instem[:Findex-1]+u"й"+instem[Findex:]
                else : # if there is no soft sign in the word
                    Findex = Cindex.start()+1
            else :
                if Sindex : # if the word ends in a consonant and has stress
                    if Sindex.start() == Vindex.start()+1 : # if the word ends in a consonant and the fleeting vowel is stressed
                        Findex = Vindex.start()+2
                    else : # if the word ends in a consonant and the fleeting vowel is not stressed
                        Findex = Vindex.start()+1
                else : # if the word ends in a consonant and has no stress
                    Findex = Vindex.start()+1
            instem = list(instem)
            instem.insert(Findex,u"F")
            instem = ''.join(instem)
            instem = instem[::-1]
        return stresser ( instem , code )
    else : # if the word is a substantivized adjective...
        return A_stemmer ( instem , code )

def AStemCodeStrip ( myinput ) :
    output = re.sub( " [1-7]" , " " , myinput )
    output = re.sub( "\\*" , "" , output )    
    return output

myFile = codecs.open ( 'Zaliznjak_IlolaMustajoki_UTF8_preproc.txt' , mode='r' , encoding='utf-8' )
Zlist = myFile.readlines() # Put the file into a list object
Ndict = {} # Nouns dictionary
Adict = {} # Adjectives dictionary
Vdict = {} # Verbs dictionary
Advdict = {} # Adverbs dictionary
Cdict = {} # Conjunctions dictionary
Idict = {} # Interjections dictionary
Numdict = {} # Numerals dictionary
Pdict = {} # Prepositions dictionary
Prodict = {} # Pronouns dictionary
Sdict = {} # Subjunctions dictionary
Odict = {} # miscellaneous dictionary

for n in range(len(Zlist)) : # Parse each line and the put entries in one of the dictionaries.
    lemma = Zlist[n][:24].strip().lower()       # lemma
    number = Zlist[n][25:29]                    # index number?? (ignored) 
    homonymy = Zlist[n][29:30]                  # homonym code (ignored)
    lexeme = Zlist[n][30:].split()[0].lower()   # lexical stem (< is primary stress, > is secondary stress)
    codesList = Zlist[n][30:].split()[1:]       # Zaliznjak code
    codes = CodeCleaner( ' '.join(codesList) )  # remove useless parts of the code
    #print lemma,number,homonymy,lexeme,codes
    if codesList[0] in u'м мо мо-жо с со ж жо мн. м, мо, мо-жо, с, со, ж, жо, мн.,'.upper().split() :
        if codes in Ndict :
            Ndict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Ndict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u'п'.upper() :                                          # Do ordinals go in adjectives or numerals?
        if codes in Adict :
            Adict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Adict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u'нсв св св-нсв нсв, св, св-нсв,'.upper().split() :
        if codes in Vdict :
            Vdict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Vdict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u'н'.upper() :
        if codes in Advdict :
            Advdict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Advdict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u'союз'.upper() :
        if codes in Cdict :
            Cdict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Cdict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u'межд.'.upper() :
        if codes in Idict :
            Idict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Idict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u'числ. числ.-п'.upper() :
        if codes in Numdict :
            Numdict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Numdict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u'предл.'.upper() :
        if codes in Pdict :
            Pdict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Pdict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u'мс мс-п'.upper() :
        if codes in Prodict :
            Prodict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Prodict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    elif codesList[0] in u''.upper() :
        if codes in Sdict :
            Sdict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Sdict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]
    else :
        if codes in Odict :
            Odict[codes].append([lemma,number,homonymy,lexeme,' '.join(codesList)])
        else :
            Odict[codes] = [[lemma,number,homonymy,lexeme,' '.join(codesList)]]

print len(Zlist),"lines in input."
print len(Ndict)+len(Adict)+len(Vdict)+len(Odict),'categories in output.'
for d , n in [ (Ndict,"noun") , (Adict,"adjective") , (Vdict,"verb") , (Advdict,"adverb") , 
               (Cdict,"conjunction") , (Idict,"interjection") , (Numdict,"numeral") , 
               (Pdict,"preposition") , (Prodict,"pronoun") , (Sdict,"subjunction") , (Odict,"miscellaneous") ] :
    print len(d),'\t',n,'categories in output.'

with codecs.open ( "nouns.lexc" , mode='w' , encoding='utf-8' ) as Nfile :
    print "Writing nouns.lexc ..."
    Nfile.write( u'LEXICON Noun\n' )
    for k in sorted ( Ndict , reverse=False ) :
        k2 = NStemCodeStrip (k)
        code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(Ndict[k])) + u'\n!' + u' '*35 + k.replace(u" ",u"_") + u'\n'
        Nfile.write(code_header)
        Nfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
        if len(k) > 9 and len(Ndict[k]) < 100 : # if the code is longer than 4 characters and there are less than, comment out all the entries
            comment = u"! "
        else :
            comment = u""
        for v in sorted ( Ndict[k] , key=lambda x: x[0][::-1]) :
            entry = comment + v[0]+u":"+N_stemmer ( v[3] , k )+u" "+k2.replace(u" ",u"_")+u" ;" 
            entry += u' '*(50-len(entry))+u"\t! "+v[2]+u'\t'+v[4]  # add unmodified code as comment
            if (not u'\u0301' in entry and not u"ё" in entry) and (not u'В' in k2) :
                entry += u'\tWARNING: no stress on stem'
            entry += u'\n'
            Nfile.write(entry)
        Nfile.write( u'\n' )

with codecs.open ( "adjectives.lexc" , mode='w' , encoding='utf-8' ) as Afile :
    print "Writing adjectives.lexc ..."
    Afile.write( u"DON'T FORGET THAT ....\n adjectives 2*a ~Fений have masc short-form in 0, not ь\nDON'T FORGET!")
    Afile.write( u'LEXICON Adjective\n' )
    for k in sorted ( Adict, key=lambda k: len(Adict[k]), reverse=True ) :
        k2 = AStemCodeStrip (k)
        code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(Adict[k])) + u'\n!' + u' '*35 + k.replace(u" ",u"_") + u'\n'
        Afile.write(code_header)
        Afile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
        for v in sorted ( Adict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+A_stemmer( v[3] , k )+u" "+k2.replace(u" ",u"_")+u" ;"
            entry += u' '*(50-len(entry))+u"\t! "+v[2]+u'\t'+v[4]+u'\n'
            Afile.write(entry)

with codecs.open ( "verbs.lexc" , mode='w' , encoding='utf-8' ) as Vfile :
    print "Writing verbs.lexc ..."
    Vfile.write( u'LEXICON Verb\n' )
    for k in sorted ( Vdict, key=lambda k: len(Vdict[k]), reverse=True ) :
        k2 = k
        code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(Vdict[k])) + u'\n!' + u' '*35 + k.replace(u" ",u"_") + u'\n'
        Vfile.write(code_header)
        Vfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
        for v in sorted ( Vdict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+stresser(v[3],k)+u" "+k2.replace(u" ",u"_")+u" ;"
            entry += u' '*(50-len(entry))+u"\t! "+v[2]+u'\t'+v[4]+u'\n'
            Vfile.write(entry)

with codecs.open ( "numerals.lexc" , mode='w' , encoding='utf-8' ) as Numfile :
    print "Writing numerals.lexc ..."
    Numfile.write( u'LEXICON Numeral\n' )
    for k in sorted ( Numdict, key=lambda k: len(Numdict[k]), reverse=True ) :
        k2 = k
        code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(Numdict[k])) + u'\n!' + u' '*35 + k.replace(u" ",u"_") + u'\n'
        Numfile.write(code_header)
        Numfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
        for v in sorted ( Numdict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+stresser(v[3],k)+u" "+k2.replace(u" ",u"_")+u" ;"
            entry += u' '*(50-len(entry))+u"\t! "+v[2]+u'\t'+v[4]+u'\n'
            Numfile.write(entry)

for d , f , l in [ (Advdict,"adverbs.lexc",u"Adverb") , (Cdict,"conjunctions.lexc",u"Conjunction") , (Idict,"interjections.lexc",u"Interjection") , 
               (Pdict,"prepositions.lexc",u"Preposition") , (Prodict,"pronouns.lexc",u"Pronoun") , (Sdict,"subjunctions.lexc",u"Subjunction") , 
               (Odict,"other.lexc",u"THESE LEXICA NEED TO BE CATEGORIZED AND LABELED") ] :
    print "Writing",f,"..."
    with codecs.open ( f , mode='w' , encoding='utf-8' ) as Myfile :
        Myfile.write( u'LEXICON ' + l + u'\n' )
        for k in sorted ( d, key=lambda k: len(d[k]), reverse=True ) :
            k2 = k
            code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(d[k])) + u'\n!' + u' '*35 + k.replace(u" ",u"_") + u'\n'
            Myfile.write(code_header)
            Myfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
            for v in sorted ( d[k] , key=lambda x: x[0][::-1]) :
                entry = v[0]+u":"+stresser(v[3],k)+u" "+k2.replace(u" ",u"_")+u" ;"
                entry += u' '*(50-len(entry))+u"\t! "+v[2]+u'\t'+v[4]+u'\n'
                Myfile.write(entry)
