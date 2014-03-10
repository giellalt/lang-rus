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
foma_trans   = [(u"!" , u"s"), 
                (u"[" , u"["), 
                (u"]" , u"]"), 
                (u'"' , u""), 
                (u"%" , u"%"), 
                (u"(" , u"["), 
                (u")" , u"]"), 
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
                (u"?" , u"?"), 
                (u"^" , u"_INCL_"), 
                (u"_" , u"_"), 
                (u"{" , u""), 
                (u"}" , u"")]

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

def Vstresser ( myinput ) : # places primary stress (acute accent), then calls stresser2 to place 2ndary stress.
    # print "Running Vstresser..." , myinput , stress2 , stress1 , mycode
    #if u'c' in myinput['paradigm'] :   # if verb has shifting stress, then add a primary stress mark to stem
    #    Vcount = Vowel.findall( myinput['lexeme'] )
    #    print 'SHIFTING STRESS for ' + myinput['lemma'] + '! Vcount is ', Vcount
    mystresses = []
    if myinput['stress1'] == [] :
        print 'Stress index missing for' , myinput['lemma']
        return myinput

    for i in myinput['stress1'] :
        if i <= len (myinput['lexeme']) :
            mystresses.append((i,u'\u0301'))
    for i in myinput['stress2'] : 
        if i <= len (myinput['lexeme']) :
            mystresses.append((i,u'\u0300'))
    mystresses = sorted( mystresses , key = lambda x : x[0] , reverse = True )
    lexemeList = list(myinput['lexeme'])
    for i , j in mystresses :
        if lexemeList[i-1] not in u'аэоуыяеёюи' :
            print 'WARNING: stress index over consonant for',myinput['lemma']
        lexemeList.insert( i , j )
    #print ''.join(lexemeList)
    myinput['lexeme'] = ''.join(lexemeList)
    return myinput

def CodeCleaner ( myinput ) : # generates the (preliminary) name of the continuation class
    output = re.sub( "\\<(.*?)\\>" , "[\\1]" , myinput )         # change <  > to [ ]   
    output = foma_replace( output )
    output = output.strip()
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
        instem.insert(len(instem)-1,u"%^F")
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
            instem.insert(Findex,u"F^%")
            instem = ''.join(instem)
            instem = instem[::-1]
        return stresser ( instem , code )
    else : # if the word is a substantivized adjective...
        return A_stemmer ( instem , code )

def V_add_stress ( myinput ) : # adds stress index for the last syllable of the stem
    if len(myinput['UnstressedVowelPositions']) > 0 :
        myinput['stress1'].append(myinput['UnstressedVowelPositions'][-1])
        myinput['stress1'].sort()
    return myinput

def V_add_suffix_to_code ( myinput ) : # adds stressed suffix to paradigm code (e.g. а́ть)
    myinput['paradigm'] = myinput['paradigm'] + u'_' + myinput['lexeme'][-1] + u'́ть'
    myinput['lexeme'] = myinput['lexeme'][:-1]
    return myinput

def V_stemmer ( myinput ) : # generates lexical stem for verbs
    #print "Running V_stemmer...",repr(myinput)
    # Remove infinitive ending (ть, ться, чь, чься, ти, тись)
    if myinput['lexeme'][-2:] == u"ся" or myinput['lexeme'][-2:] == u"сь" :
        myinput['lexeme'] = myinput['lexeme'][:-4]
    else :
        myinput['lexeme'] = myinput['lexeme'][:-2]
    
    # Remove more, depending on inflection class
    if myinput['paradigm'][:2] == '14' or myinput['paradigm'][:5] == u"нп 14" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
    elif myinput['paradigm'][:2] == '13' or myinput['paradigm'][:5] == u"нп 13" :
        myinput['lexeme'] = myinput['lexeme'][:-2]
    elif myinput['paradigm'][:2] == '12' or myinput['paradigm'][:5] == u"нп 12" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
    elif myinput['paradigm'][:2] == '11' or myinput['paradigm'][:5] == u"нп 11" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
    elif myinput['paradigm'][:2] == '10' or myinput['paradigm'][:5] == u"нп 10" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
    elif myinput['paradigm'][:1] == '9' or myinput['paradigm'][:4] == u"нп 9" :
        myinput['lexeme'] = myinput['lexeme'][:-3]
    elif myinput['paradigm'][:1] == '6' or myinput['paradigm'][:4] == u"нп 6" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
    elif myinput['paradigm'][:1] == '5' or myinput['paradigm'][:4] == u"нп 5" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
        if myinput['pos'][:2] == u'св' :  # If the verb is perfective or biaspectual
            if myinput['stress1'][-1] == len(myinput['lexeme']) :
                myinput = V_add_suffix_to_code(myinput)

    elif myinput['paradigm'][:1] == '4' or myinput['paradigm'][:4] == u"нп 4" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
    elif myinput['paradigm'][:1] == '3' or myinput['paradigm'][:4] == u"нп 3" : # уть
        myinput['lexeme'] = myinput['lexeme'][:-1]
        if u'3°a' in myinput['paradigm'] :
            myinput['paradigm'] = myinput['paradigm'].replace(u'3°a',u'3a_zero')
        if u'3b' in myinput['paradigm'] :
            if len(myinput['VowelPositions']) > 2 and myinput['lemma'][-2:] != u'ся' :
                myinput['paradigm'] = myinput['paradigm'] + u'_multisyll'
                myinput = V_add_stress(myinput)
            elif len(myinput['VowelPositions']) == 2 and myinput['lemma'][-2:] != u'ся' :
                myinput['paradigm'] = myinput['paradigm'] + u'_unisyll'
    elif myinput['paradigm'][:1] == '2' or myinput['paradigm'][:4] == u"нп 2" : # овать
        if myinput['lexeme'][-3] == u'о' :
            myinput['lexeme'] = myinput['lexeme'][:-3]
        elif myinput['lexeme'][-3] == u'е' :
            if myinput['lexeme'][-4] in u'жшщчц' :
                myinput['lexeme'] = myinput['lexeme'][:-3]
            elif myinput['lexeme'][-4] in u'аэоуыяеёюи' :
                myinput['lexeme'] = myinput['lexeme'][:-3]
                myinput['lexeme'] = myinput['lexeme'] + u'й'
            elif myinput['lexeme'][-4] in u'бвдзлмнпрстф' :
                myinput['lexeme'] = myinput['lexeme'][:-3]
                myinput['lexeme'] = myinput['lexeme'] + u'ь'
        elif myinput['lexeme'][-3] == u'ё' :
            if myinput['lexeme'][-4] in u'жшщчц' :
                myinput['lexeme'] = myinput['lexeme'][:-3]
                myinput['paradigm'] += u'_ёва́'
            elif myinput['lexeme'][-4] in u'аэоуыяеёюи' :
                myinput['lexeme'] = myinput['lexeme'][:-3]
                myinput['lexeme'] = myinput['lexeme'] + u'й'
            elif myinput['lexeme'][-4] in u'бвдзлмнпрстф' :
                myinput['lexeme'] = myinput['lexeme'][:-3]
                myinput['lexeme'] = myinput['lexeme'] + u'ь'
        else : print "WARNING: V_stemmer function is not processing",myinput['lemma'],'correctly.'
        if len(myinput['stress1']) >= 1 :
            if myinput['stress1'][-1] > len(myinput['lexeme']) : # if the suffix is stressed, i.e. ова́ть
                #print myinput['lexeme'],'|',len(myinput['lexeme']),'|',myinput['stress1'][-1]
                if myinput['paradigm'][-5:] != u'_ёва́' and myinput['paradigm'][1] != u'b' :
                    myinput['paradigm'] = myinput['paradigm'] + u'_ова́'
                #print myinput['paradigm']
    elif myinput['paradigm'][:1] == '1' and u'%[x]%' not in myinput['paradigm'] :
        if myinput['pos'][:2] == u'св' :  # If the verb is perfective or biaspectual
            if myinput['stress1'][-1] == len(myinput['lexeme']) :
                myinput = V_add_suffix_to_code(myinput)
                myinput = V_add_stress(myinput)
    myinput = VCodeCleaner (myinput)
    return Vstresser ( myinput )

def VCodeCleaner ( myinput ) :
    for codefields in ['paradigm','paradigm_details'] :
        for old , new in [(u'%tr%',u''),(u'%[x]%',u'?'),(u'%x%',u's'),(u'%1%',u'1'),(u'%2%',u'2'),(u'%3%',u'3'),(u'%4%',u'4'),(u'%5%',u'5'),(u'%6%',u'6'),(u'%7%',u'7'),(u'%8%',u'8'),(u'%9%',u'9'),(u'§ ',u'')] :
            myinput[codefields] = myinput[codefields].replace(old,new)
    return myinput

def AStemCodeStrip ( myinput ) :
    output = re.sub( " [1-7]" , " " , myinput )
    output = re.sub( "\\*" , "" , output )    
    return output

def DeNumber ( lemmaname ) : # remove leading numbers from lemma, e.g. 2есть > есть
    if lemmaname[0] in u'0123456789-' :
        return DeNumber(lemmaname[1:])
    else :
        return lemmaname

def Yoer ( myDict ) :
    if u'ё' in myDict['lexeme'] :
        return myDict['lexeme'] , myDict['paradigm'].replace( u", ё" , u'' )
    elif u'е' in myDict['lexeme'] :
        myList = list (myDict['lexeme'])
        myList.reverse()
        myList[myList.index(u'е')] = u'ё'
        myList.reverse()
        return ''.join(myList) , myDict['paradigm'].replace( u", ё" , u'' )
    else :
        print "WARNING: no 'е' in" , myDict['lexeme'] , "to convert to 'ё'"
        return myDict['lexeme'] , myDict['paradigm']

myFile = codecs.open ( 'gram_studentam_preprocessed.csv' , mode='r' , encoding='utf-8' )
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

myColumns = Zlist.pop(0).split(u"\t")
myColumns = [i.strip() for i in myColumns]
print '\t'.join(myColumns)

for n in range(len(Zlist)) : # Parse each line and the put entries in one of the dictionaries.
    entryDict = {}
    thisLine = Zlist[n].split(u"\t")

    for n in range(len(myColumns)) :
        entryDict[myColumns[n]] = thisLine[n].strip()

    entryDict['VowelPositions'] = [m.start()+1 for m in Vowel.finditer(entryDict['lexeme'])]
    entryDict['stress2'] = [ i for i in entryDict['stress2'].split(u"/") ]
    if entryDict['stress2'] == [''] :
        entryDict['stress2'] = []
    else : entryDict['stress2'] = [ int(i) for i in entryDict['stress2'] ]
    entryDict['stress1'] = [ i for i in entryDict['stress1'].split(u"/") ]
    if entryDict['stress1'] == [''] or entryDict['stress1'] == ['x'] :
        entryDict['stress1'] = []
    else : entryDict['stress1'] = sorted([ int(i) for i in entryDict['stress1'] ])
    entryDict['UnstressedVowelPositions'] = sorted(list(set(entryDict['VowelPositions']) - set(entryDict['stress1']) - set(entryDict['stress2'])))
    if entryDict['lemma'] == "" :
        entryDict['lemma'] = entryDict['lexeme'] # if lemma is empty, copy lexeme
    if entryDict['pos'] == "" :
        entryDict['pos'] = u"UNLABELLED"
    if entryDict['paradigm'] == "" :
        entryDict['paradigm'] = u"UNLABELLED"
    if u'ё' in entryDict['lemma'] and u'ё' not in entryDict['lexeme'] : # if the lemma has a ё and lexeme doesn't, switch them
        if DeNumber(entryDict['lemma']).replace(u'ё',u'е') == entryDict['lexeme'] :
            entryDict['lexeme'] = DeNumber(entryDict['lemma']).replace(u'ё',u'е')
        else :
            print entryDict['lemma'] , entryDict['lexeme']
    entryDict['lemma'] = entryDict['lemma'].replace(u'ё',u'е') # remove ё from all lemmas
    if u', ё' in entryDict['paradigm'] and u'св' not in entryDict['pos'] : # non-verbs with ', ё' in Z's code
        entryDict['lexeme'] , entryDict['paradigm'] = Yoer ( entryDict ) # put ё into lexeme of nominals


    codes = entryDict['pos'] + " " + entryDict['paradigm'] + " " + entryDict['paradigm_details']
    codes = codes.strip()

    if entryDict['pos'].split()[0] in u'м мо мо-жо с со ж жо мн.'.split() :
        if codes in Ndict :
            Ndict[codes].append(entryDict)
        else :
            Ndict[codes] = [entryDict]
    elif entryDict['pos'].split()[0] in u'п' :
        if codes in Adict :
            Adict[codes].append(entryDict)
        else :
            Adict[codes] = [entryDict]
    elif entryDict['pos'].split()[0] in u'нсв св св-нсв нсв, св, св-нсв,'.split() :
        if codes in Vdict :
            Vdict[codes].append(entryDict)
        else :
            Vdict[codes] = [entryDict]
    elif entryDict['pos'][0] in u'н' :
        if codes in Advdict :
            Advdict[codes].append(entryDict)
        else :
            Advdict[codes] = [entryDict]
    elif entryDict['pos'] in u'союз' :
        if codes in Cdict :
            Cdict[codes].append(entryDict)
        else :
            Cdict[codes] = [entryDict]
    elif entryDict['pos'] in u'межд.' :
        if codes in Idict :
            Idict[codes].append(entryDict)
        else :
            Idict[codes] = [entryDict]
    elif entryDict['pos'] in u'числ. числ.-п' :
        if codes in Numdict :
            Numdict[codes].append(entryDict)
        else :
            Numdict[codes] = [entryDict]
    elif entryDict['pos'] in u'предл.' :
        if codes in Pdict :
            Pdict[codes].append(entryDict)
        else :
            Pdict[codes] = [entryDict]
    elif entryDict['pos'] in u'мс мс-п' :
        if codes in Prodict :
            Prodict[codes].append(entryDict)
        else :
            Prodict[codes] = [entryDict]
    elif entryDict['pos'] in u'' :
        if codes in Sdict :
            Sdict[codes].append(entryDict)
        else :
            Sdict[codes] = [entryDict]
    else :
        if codes in Odict :  # leftovers
            Odict[codes].append(entryDict)
        else :
            Odict[codes] = [entryDict]

print len(Zlist),"lines in input."
print len(Ndict)+len(Adict)+len(Vdict)+len(Odict),'categories in output.'
for d , n in [ (Ndict,"noun") , (Adict,"adjective") , (Vdict,"verb") , (Advdict,"adverb") , 
               (Cdict,"conjunction") , (Idict,"interjection") , (Numdict,"numeral") , 
               (Pdict,"preposition") , (Prodict,"pronoun") , (Sdict,"subjunction") , (Odict,"miscellaneous") ] :
    print len(d),'\t',n,'categories in output.'

with codecs.open ( "../stems/verbs.lexc" , mode='w' , encoding='utf-8' ) as Vfile :
    print "Preparing verbs.lexc ...",
    newVdict = {}
    for code in Vdict :
        for entry in Vdict[code] :
            entry = V_stemmer(entry)
            entry['paradigm'] = entry['paradigm'].replace("*","")
            if entry['lemma'][-2] == u"с" :
                entry['paradigm'] += u"_R"
            lexicon = entry['pos'] + " " + entry['paradigm'] + " " + entry['paradigm_details']
            lexicon = lexicon.strip()
            if lexicon in newVdict :
                newVdict[lexicon].append(entry)
            else :
                newVdict[lexicon] = [entry]
    print len(newVdict),'categories in verbs.lexc ...',
    print "writing verbs.lexc ...",
    Vcatslist = []
    Vfile.write( u'LEXICON Verb\n' )
    for each_code in sorted ( newVdict, reverse=False ) : # for each grammar code in the verb dictionary
        Vcatslist.append([len(newVdict[each_code]),each_code,newVdict[each_code][0]['lemma']])
        #print each_code
        code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(newVdict[each_code])) + u'\n!' + u' '*35 + each_code.replace(u" ",u"_") + u'\n'
        #print code_header
        Vfile.write(code_header)
        #Vfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
        for each_lemma in sorted ( newVdict[each_code] , key=lambda x: x['lemma'][::-1]) :
            if each_lemma['skip'] == u'1' :
                skipper = u"! "
            elif len(newVdict[each_code]) < 100 and each_lemma['skip'] != u'-1' : # -1 in the skip column blocks that lemma from being commented out
                skipper = u"! "
            else : skipper = u""
            entry = skipper + each_lemma['lemma'] + u":" + each_lemma['lexeme'] + u" " + each_code.replace(" ","_") + u" ;"
            #entry += u' '*(50-len(entry)) + u"\t! " + each_lemma['pos'] + u' ' + each_lemma['paradigm'] + u' ' + each_lemma['paradigm_details']
            entry += u'\n'
            Vfile.write(entry)
    Vcatsfile = codecs.open ( "verb_cats.txt" , mode='w' , encoding='utf-8' )
    for i,j,k in sorted (Vcatslist,key=lambda x : x[0],reverse=True) :
        Vcatsfile.write(str(i)+'\t\t'+j+'\t\t'+k+"\n")
    Vcatsfile.close()    
    print "verbs.lexc done!"

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
            entry += u' '*(50-len(entry))+u"\t! "+v[4]  # add unmodified code as comment
            if (not u'\u0301' in entry and not u"ё" in entry) and (not u'В' in k2) :
                entry += u'\tWARNING: no stress on stem'
            entry += u'\n'
            Nfile.write(entry)
        Nfile.write( u'\n' )

with codecs.open ( "adjectives.lexc" , mode='w' , encoding='utf-8' ) as Afile :
    print "Writing adjectives.lexc ..."
    Afile.write( u"DON'T FORGET THAT ....\n adjectives 2*a ~Fений have masc short-form in 0, not ь\n! DON'T FORGET!!\n\n")
    Afile.write( u'LEXICON Adjective\n' )
    for k in sorted ( Adict, key=lambda k: len(Adict[k]), reverse=True ) :
        k2 = AStemCodeStrip (k)
        code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(Adict[k])) + u'\n!' + u' '*35 + k.replace(u" ",u"_") + u'\n'
        Afile.write(code_header)
        Afile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
        if len(Adict[k]) < 250 : # if there are less than 250 lemmas, comment out all the entries
            comment = u"! "
        else :
            comment = u""
        for v in sorted ( Adict[k] , key=lambda x: x[0][::-1]) :
            entry = comment + v[0]+u":"+A_stemmer( v[3] , k )+u" "+k2.replace(u" ",u"_")+u" ;"
            entry += u' '*(50-len(entry))+u"\t! "+v[4]+u'\n'
            Afile.write(entry)

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
            entry += u' '*(50-len(entry))+u"\t! "+v[4]+u'\n'
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
                entry += u' '*(50-len(entry))+u"\t! "+v[4]+u'\n'
                Myfile.write(entry)
