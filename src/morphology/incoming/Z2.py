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
import itertools
import copy

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

Masc = [u"м", u"мо"]
MascFcodes = [u"1a", u"1b", u"1e", u"2a", u"2b", u"2e", u"3a", u"3b", u"3d", u"5a", u"5b", u"6a", u"6b"]
Fem = [u"ж", u"жо"]
Fem8codes = [u"8b'", u"8e"]
Pro = [u"мс"]
ProFcodes = [] # [u"1b", u"2b", u"6b"]
MiscM = []
Fgroup1 = combiner(Masc,MascFcodes) + combiner(Fem,Fem8codes) + combiner (Pro,ProFcodes) + MiscM

FemFcodesS = [u"1b", u"1e", u"1f", u"2b", u"2e", u"2f", u"3b", u"3f", u"3f'", u"5b", u"6b"]
Neut = [u"с", u"со"]
NeutFcodesS = [u"1b", u"1c", u"3b", u"3c", u"5b", u"5c", u"5f", u"6b"]
Adj = [u"п"]
AdjFcodesS = [u"1a/b", u"1b"]
MiscS = [u"мн. <м 3b>",u"мн. <м 5b>"] # These aren't working
Fgroup2stressed = combiner(Fem,FemFcodesS) + combiner(Neut,NeutFcodesS) + combiner(Adj,AdjFcodesS) + MiscS

FemFcodesU = [u"1a", u"1d", u"2a", u"2d", u"2d'", u"3a", u"3d", u"5a", u"5d", u"6a", u"6d"]
NeutFcodesU = [u"1a", u"1d", u"3a", u"3d", u"5a", u"5d", u"6a", u"6d"]
AdjFcodesU = [u"1a", u"1a'", u"1a/c", u"1a/c'", u"1a/c''", u"1b/c'", u"1b/c''", u"2a", u"3a", u"3a'", u"3a/c", u"3a/c'", u"3a/c''"]
MiscU = [u"мн. <м 2a>",u"мн. <м 3a>",u"мн. <м 5a>"] # These aren't working
Fgroup2unstressed = combiner(Fem,FemFcodesU) + combiner(Neut,NeutFcodesU) + combiner(Adj,AdjFcodesU) + MiscU

def fleeter ( myinput ) : # decide whether word belongs to Fgroup1 (Mfleeter) or Fgroup2 (Ffleeter, stressed or unstressed)
    # print "Running fleeter...",myinput['lemma'],'(',myinput['lexeme'],')',myinput['pos'],myinput['paradigm']
    if myinput['FV'] != u'' :
        return Ffleeter ( myinput , "stressed" ) # could be "unstressed", bypassed anyway
    if u'мс ' in myinput['pos'] + u' ' + myinput['paradigm'] or myinput['pos'] == u'п' and myinput['lemma'][-1] != u'й' :
        return Mfleeter (myinput)
    for c in Fgroup2stressed :
        if c in myinput['pos'] + u' ' + myinput['paradigm'] :
            return Ffleeter (myinput,"stressed")
    for c in Fgroup2unstressed :
        if c in myinput['pos'] + u' ' + myinput['paradigm'] :
            return Ffleeter (myinput,"unstressed")
    for c in Fgroup1 :
        if c in myinput['pos'] + u' ' + myinput['paradigm'] :
            return Mfleeter (myinput)
    else :
        print "Warning A: Fleeting vowel added with FEM/NEUT/PL UNSTRESSED conventions (FV tag) :",myinput['lemma'],myinput['lexeme'],myinput['pos'],myinput['paradigm']
        return Ffleeter (myinput,"unstressed",confidence=0)

def Mfleeter (myinput) : # add (or don't add) ь or й to "alternate" with fleeting vowel
    # print "Running Mfleeter...",myinput['lemma'],myinput['lexeme'],myinput['paradigm'],">>>>",
    mylexeme = myinput['lexeme']
    Findex = mylexeme.find(u"F")
    if mylexeme[Findex+1] == u'́' : # If stress is on the F symbol, put it on preceding vowel
        mylexeme = mylexeme[:Findex-2] + u'́%^F' + mylexeme[Findex+2:]
    if u"Fо" in mylexeme :
        return myinput
    elif mylexeme[mylexeme.find(u'F')+1] in u"аеёяи" :
        if mylexeme[Findex-3] in u"а э о у ы я е ё ю и ́".split() :
            mylexeme = mylexeme[:Findex]+u"й"+mylexeme[Findex:]
        elif mylexeme[Findex-3] == u"л" :
            mylexeme = mylexeme[:Findex]+u"ь"+mylexeme[Findex:]
        elif mylexeme[Findex-3] in u"бвгдзйкмнпрстфх" and (u"м 3" in myinput['paradigm'] or u"мо 3" in myinput['paradigm']):
            mylexeme = mylexeme[:Findex]+u"ь"+mylexeme[Findex:]
        myinput['lexeme'] = mylexeme
        return myinput
    elif mylexeme[mylexeme.find(u'F')+1] in u"аеёяи" :
        return myinput
    else :
        print "Warning B: Fleeting vowel added with FEM/NEUT/PL UNSTRESSED conventions (FV tag) :",myinput['lemma'],myinput['lexeme'],myinput['pos'],myinput['paradigm'],
        return Ffleeter (myinput,"unstressed",confidence=0)

def Ffleeter (myinput,stress,confidence=1) :
    # print "Running Ffleeter...",myinput,mycode,stress,">>>>",
    Findex = myinput['lexeme'].find(u"F")
    if myinput['FV'] != u'' :
        TheVowel = myinput['FV'].split(u'/')[0]
    elif u"6" in myinput['paradigm'] :
        if stress == "unstressed" :
            TheVowel = u"и"
        elif stress == "stressed" :
            TheVowel = u"е́"
    elif ( myinput['lexeme'][Findex-3] == u"ь" or myinput['lexeme'][Findex-3] == u"й" ) and myinput['lexeme'][Findex+1] == u"ц" :
        if stress == "unstressed" :
            TheVowel = u"е"
        elif stress == "stressed" :
            TheVowel = u"е́"
    elif ( myinput['lexeme'][Findex-3] == u"ь" or myinput['lexeme'][Findex-3] == u"й" ) and myinput['lexeme'][Findex+1] != u"ц" :
        if stress == "unstressed" :
            TheVowel = u"е"
        elif stress == "stressed" :
            TheVowel = u"ё"
    elif myinput['lexeme'][Findex-3] in u"гкх" :
        if stress == "unstressed" :
            TheVowel = u"о"
        elif stress == "stressed" :
            TheVowel = u"о́"
    elif myinput['lexeme'][Findex-3] in u"жшщчц" :
        if stress == "unstressed" :
            TheVowel = u"е"
        elif stress == "stressed" :
            TheVowel = u"о́"
    elif myinput['lexeme'][Findex+1] in u"гкх" :
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
        print "\t>>>>>\t"+myinput['lexeme'][:Findex+1]+TheVowel+myinput['lexeme'][Findex+1:]+u"FV"
        myinput['lexeme'] = myinput['lexeme'][:Findex+1]+TheVowel+myinput['lexeme'][Findex+1:]+u"FV"
    else : 
        myinput['lexeme'] = myinput['lexeme'][:Findex+1]+TheVowel+myinput['lexeme'][Findex+1:]
    return myinput

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

def stresser ( myinput ) : # places primary stress (acute), and secondary stress (grave).
    mystresses = []
    if myinput['stress1'] == [] :
        #print 'Stress index missing for' , myinput['lemma']
        return myinput
    Fposition = myinput['lexeme'].find(u'%^F')
    if Fposition >= 0 :
        myinput['lexeme'] = myinput['lexeme'].replace(u'%^F',u'')
    for i in myinput['stress1'] :
        if i <= len (myinput['lexeme']) and myinput['lexeme'][i-1] != u'ё' :
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
    if Fposition >= 0 and myinput['pos'] not in [u'св',u'св-нсв',u'нсв'] :
        newFposition = Fposition + len([i for i in myinput['stress1']+myinput['stress2'] if i < Fposition])
        newFposition = newFposition - myinput['lexeme'][:newFposition].count(u'ё')
        myinput['lexeme'] = myinput['lexeme'][:newFposition] + u'%^F' + myinput['lexeme'][newFposition:]
        return fleeter (myinput)
    else :
        return myinput

# def CodeCleaner ( myinput ) : # generates the (preliminary) name of the continuation class
#     output = re.sub( "\\<(.*?)\\>" , "[\\1]" , myinput )         # change <  > to [ ]   
#     output = foma_replace( output )
#     output = output.strip()
#     return output.strip()

def NCodeStrip ( myinput ) : # For nouns, remove stem labels and fleeting vowel markers from continuation class name generated by CodeCleaner
    output = re.sub( " [1-7]" , " " , myinput )
    output = re.sub( "\\*" , "" , output )
    return output

def A_stemmer ( myinput ) : # generates lexical stem for adjectives (including substantivized)
    # print "Running A_stemmer...",myinput['lemma'],myinput['paradigm'],myinput['paradigm_details']
    if myinput['lexc_stem'] != u'' :
        myinput['lexeme'] = myinput['lexc_stem']
        return myinput
    elif myinput['lexeme'][-2:] in [u'ый',u'ой'] :
        myinput['lexeme'] = myinput['lexeme'][:-2]
    elif myinput['lexeme'][-2:] in [u'ий'] and u'<мс ' not in myinput['paradigm']:
        myinput['lexeme'] = myinput['lexeme'][:-2]
        if myinput['lexeme'][-1] == u'н' :
            myinput['lexeme'] += u'ь'
    if u'***' in myinput['paradigm'] or ( not  '**' in myinput['paradigm'] and '*' in myinput['paradigm'] ) :    # If the code indicates that there is a fleeting vowel
        AFchecker = 0
        for c in AdjFcodesU : 
            if c in myinput['paradigm'] :
                AFchecker += 1
        if AFchecker > 0 :
            myinput = add_stress (myinput)
        instem = list(myinput['lexeme'])
        if u'<мс ' in myinput['paradigm'] or myinput['lemma'][-1] != u'й' or myinput['lexeme'][-2:] == u'нь':
            instem.insert(len(instem)-2,u"%^F")
        else :
            instem.insert(len(instem)-1,u"%^F")
        instem = ''.join(instem)
        myinput['lexeme'] = instem
    myinput['paradigm'] = re.sub( "\\*" , "" , myinput['paradigm'] )
    return stresser ( myinput )

Cons = re.compile(u"[бвгджзйклмнпрстфхцчшщ]")
SoftSign = re.compile(u"[ь]")
Vowel = re.compile(u"[аэоуыяеёюи]")
VowEnd = re.compile(u"[аяоёеыи]")
StressRE = re.compile(u"[<>]")

def N_stemmer ( myinput ) :
    # print "Running N_stemmer...",instem,code
    # need to add a stress mark for d and f
    if myinput['lexc_stem'] != u'' :
        myinput['lexeme'] = myinput['lexc_stem']
        return myinput
    elif u"<п " not in myinput['paradigm'] :
        if u'***' in myinput['paradigm'] or ( not  '**' in myinput['paradigm'] and '*' in myinput['paradigm'] ) :    # If the code indicates that there is a fleeting vowel
            instem = myinput['lexeme'][::-1]
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
            myinput['lexeme'] = instem
            myinput['paradigm'] = re.sub( "\\*" , "" , myinput['paradigm'] )
        return stresser ( myinput )
    else : # if the word is a substantivized adjective...
        return A_stemmer ( myinput )

def add_yo ( inputString ) : # converts the final 'е' in the string to 'ё'
    inputString = inputString[::-1]
    theIndex = inputString.find(u'е')
    inputString = inputString[:theIndex] + u'ё' + inputString[theIndex+1:]
    return inputString[::-1]

def add_stress ( myinput ) : # adds stress index for the last syllable of the stem
    if len(myinput['PotentialStressPositions']) > 0 :
        if myinput['PotentialStressPositions'][-1] < myinput['stress1'][-1] :
            myinput['stress1'].append(myinput['PotentialStressPositions'][-1])
            myinput['stress1'].sort()
            myinput['PotentialStressPositions'] = myinput['PotentialStressPositions'][:-1]
    return myinput

def add_stress_directly ( myinput ) : # adds stress index for the last syllable of the stem
    if len([i for i in myinput['VowelPositions'] if i < len(myinput['lexeme'])]) > 0 :
        stressPosition = max([i for i in myinput['VowelPositions'] if i < len(myinput['lexeme'])])
        if myinput['lexeme'][stressPosition-1] not in u'бвгджзйклмнпрстфхцчшщ' :
            myinput['lexeme'] = myinput['lexeme'][:stressPosition] + u'\u0301' + myinput['lexeme'][stressPosition:]
        else :
            stressPosition += 1
            if myinput['lexeme'][stressPosition-1] not in u'бвгджзйклмнпрстфхцчшщ' :
                myinput['lexeme'] = myinput['lexeme'][:stressPosition] + u'\u0301' + myinput['lexeme'][stressPosition:]
            else :
                print 'ASD error: stress over cons.',myinput['lemma'],myinput['lexeme']
    else :
        print 'ASD error:',myinput['lemma'],myinput['lexeme']
    return myinput

def V_add_suffix_to_code ( myinput , mylength ) : # adds suffix to paradigm code (e.g. ать, а́ть, еть, е́ть, etc.)
    mylemma = DeNumber ( myinput['lemma'] )
    if mylemma[-2] == u"с" : # remove reflexive suffix
        mylemma = mylemma[:-2]
    if myinput['stress1'][-1] > len(mylemma) - mylength : # if the suffix is stressed
        removed_chars = mylemma[:-mylength]
        mysuffix = mylemma[-mylength:]
        stress_index_for_suffix = myinput['stress1'][-1] - len(removed_chars)
        mysuffix = mysuffix[:stress_index_for_suffix] + u'́' + mysuffix[stress_index_for_suffix:]
    else :
        mysuffix = mylemma[-mylength:]
    myinput['paradigm'] = myinput['paradigm'] + u'_' + mysuffix
    myinput['lexeme'] = myinput['lexeme'][:-mylength+2]
    return myinput

def V_stemmer ( myinput ) : # generates lexical stem for verbs
    # print "Running V_stemmer...",repr(myinput).decode("unicode-escape")
    # Remove infinitive ending (ть, ться, чь, чься, ти, тись)
    if myinput['lexc_stem'] != u'' :
        myinput['lexeme'] = myinput['lexc_stem']
        myinput = CodeCleaner (myinput)
        myinput['paradigm'] += myinput['lexc_suffix'] # for most words, this represents no change
        return myinput
    if myinput['lexeme'][-2:] == u"ся" or myinput['lexeme'][-2:] == u"сь" :
        myinput['lexeme'] = myinput['lexeme'][:-4]
    else :
        myinput['lexeme'] = myinput['lexeme'][:-2]
    # Add "pp" to paradigm of all transitive imperfectives without an aspectual partner
    if myinput['paradigm'][:3] == u'нсв' and myinput['lemma'][-2] != u'с' and myinput['aspect_pair'] == u'' :
        myinput['paradigm'] += u'pp'
    
    # Remove more, depending on inflection class

    # if the source file dictates a lexc_code override, then follow the override (and not the )
    if myinput['lexc_code'] != u'' :
        if myinput['stem_drop'] != u'' : dropper = int(myinput['stem_drop'])
        else : dropper = 0
        if dropper > 0 :
            myinput['lexeme'] = myinput['lexeme'][:-dropper]
        myinput['paradigm_details'] = myinput['lexc_code']

    if u'%1%' in myinput['paradigm'] or u'%4%' in myinput['paradigm'] :  # add stress to verbs with помета 1
        myinput = add_stress( myinput )

    
    elif myinput['paradigm'][:2] == '16' or myinput['paradigm'][:5] == u"нп 16" :
        completely_useless_variable = 0
    
    elif myinput['paradigm'][:2] == '15' or myinput['paradigm'][:5] == u"нп 15" :
        completely_useless_variable = 0
    
    elif myinput['paradigm'][:2] == '14' or myinput['paradigm'][:5] == u"нп 14" :
        myinput = V_add_suffix_to_code(myinput,3)
    
    elif myinput['paradigm'][:2] == '13' or myinput['paradigm'][:5] == u"нп 13" :
        myinput['lexeme'] = myinput['lexeme'][:-2]
    
    elif myinput['paradigm'][:2] == '12' or myinput['paradigm'][:5] == u"нп 12" :
        if myinput['lexeme'][-1] == u'ы' :
            myinput = V_add_suffix_to_code(myinput,3)
    
    elif myinput['paradigm'][:2] == '11' or myinput['paradigm'][:5] == u"нп 11" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
    
    elif myinput['paradigm'][:2] == '10' or myinput['paradigm'][:5] == u"нп 10" :
        if myinput['lexeme'][-2] == u'р' :
            myinput = V_add_suffix_to_code(myinput,4)
        else :
            myinput['lexeme'] = myinput['lexeme'][:-1]
    
    elif myinput['paradigm'][:1] == '9' or myinput['paradigm'][:4] == u"нп 9" :
        myinput['lexeme'] = myinput['lexeme'][:-3]
    
    elif myinput['paradigm'][:1] == '8' or myinput['paradigm'][:4] == u"нп 8" :
        if u'ё' in myinput['paradigm'] and myinput['lexeme'][-1] == u'е' :
            myinput['lexeme'] = myinput['lexeme'][:-1]+u'ё'
            myinput['paradigm'] = myinput['paradigm'].replace(u'ё',u'')
        elif u'ё' in myinput['paradigm'] :
            print "Trouble placing ё in stem of",myinput['lemma']
        if u'(-к-)' in myinput['paradigm'] :
            myinput['lexeme'] = myinput['lexeme']+u'к'
            myinput['paradigm'] = myinput['paradigm'].replace(u'(-к-)',u'')
        elif u'(-г-)' in myinput['paradigm'] :
            myinput['lexeme'] = myinput['lexeme']+u'г'
            myinput['paradigm'] = myinput['paradigm'].replace(u'(-г-)',u'')
        else : print "Trouble placing г/к in stem of",myinput['lemma']
    
    elif myinput['paradigm'][:1] == '7' or myinput['paradigm'][:4] == u"нп 7" :
        while myinput['lexeme'][-1] != u'з' and myinput['lexeme'][-1] != u'с' :
            myinput['lexeme'] = myinput['lexeme'][:-1]
        if myinput['lexeme'][-1] == u'с' :
            myinput['lexeme'] = myinput['lexeme'][:-1]
            if u'(-д-)' in myinput['paradigm'] :
                myinput['lexeme'] += u'д'
            elif u'(-т-)' in myinput['paradigm'] :
                myinput['lexeme'] += u'т'
            elif u'(-с-)' in myinput['paradigm'] :
                myinput['lexeme'] += u'с'
            elif u'(-ст-)' in myinput['paradigm'] :
                myinput['lexeme'] += u'ст'
            elif u'(-б-)' in myinput['paradigm'] :
                myinput['lexeme'] += u'б'
            else : print 'V_stemmer WARNING: trouble finishing stem of',myinput['lemma'],myinput['paradigm'],myinput['lexeme']
            if u'ё' in myinput['paradigm'] :
                while myinput['lexeme'][-1] != u'е' :
                    myinput['lexeme'] = myinput['lexeme'][:-1]
                myinput['lexeme'] = myinput['lexeme'][:-1]
        else :
            if u'ё' in myinput['paradigm'] :
                myinput['lexeme'] = add_yo ( myinput['lexeme'] )
    
    elif myinput['paradigm'][:1] == '6' or myinput['paradigm'][:4] == u"нп 6" :
        if u'ё' in myinput['paradigm'] :
            suffix_length = len(DeNumber(myinput['lemma']))-myinput['PotentialStressPositions'][-1]+1
            myinput = V_add_suffix_to_code(myinput,suffix_length)
        else :
            myinput = V_add_suffix_to_code(myinput,3)
        if u'6b' in myinput['paradigm'] :
            myinput['paradigm'] = myinput['paradigm'].replace(u'6b',u'6°b')
        if u'6°b' in myinput['paradigm'] : 
            if myinput['paradigm'][:2] != u'нп' and myinput['lemma'][-2] != u'с' :
                if myinput['pos'][:2] == u'св' or myinput['pos'][:3] == u'нсв' and myinput['aspect_pair'] == u'' :
                    myinput = add_stress(myinput)
        if u'6c' in myinput['paradigm'] :
            myinput = add_stress(myinput)
        elif myinput['pos'][:2] == u'св' or myinput['pos'][:3] == u'нсв' and myinput['aspect_pair'] == u'' :  # If the verb is transitive perfective/biaspectual or imperfective without an aspectual partner
            if myinput['stress1'][-1] == len(myinput['lexeme']) :
                myinput = add_stress(myinput)
    
    elif myinput['paradigm'][:1] == '5' or myinput['paradigm'][:4] == u"нп 5" :
        myinput = V_add_suffix_to_code(myinput,3)
        if u'5c' in myinput['paradigm'] :
            myinput = add_stress(myinput)
    
    elif myinput['paradigm'][:1] == '4' or myinput['paradigm'][:4] == u"нп 4" :
        myinput['lexeme'] = myinput['lexeme'][:-1]
        if u'%8%' in myinput['paradigm'] :
            myinput = add_stress(myinput)
        if u'-жд-' in myinput['paradigm_details']:
            myinput['lexeme'] = myinput['lexeme'][:-1]
    
    elif myinput['paradigm'][:1] == '3' or myinput['paradigm'][:4] == u"нп 3" : # нуть
        myinput['lexeme'] = myinput['lexeme'][:-2]
        if u'3°a' in myinput['paradigm'] :
            myinput['paradigm'] = myinput['paradigm'].replace(u'3°a',u'3a zero')
        elif u'3b' in myinput['paradigm'] and myinput['lemma'][-2:] != u'ся' and u'нп' not in myinput['paradigm']:
            if u'ё' in myinput['paradigm'] :
                myinput['paradigm'] = myinput['paradigm'].replace(u'ё',u'')
                myinput['lexeme'] = add_yo(myinput['lexeme'])
            else :
                myinput = add_stress(myinput)
        elif u'3c' in myinput['paradigm'] :
            if u'ё' in myinput['paradigm'] :
                suffix_length = len(DeNumber(myinput['lemma']))-myinput['PotentialStressPositions'][-1]+1
                myinput = V_add_suffix_to_code(myinput,suffix_length)
            myinput = add_stress(myinput)
    
    elif myinput['paradigm'][:1] == '2' or myinput['paradigm'][:4] == u"нп 2" : # овать
        if u' о' in myinput['paradigm'] :
            myinput['paradigm'] = myinput['paradigm'].replace(u' о',u'')
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
                myinput['paradigm'] += u' ёва́'
            elif myinput['lexeme'][-4] in u'аэоуыяеёюи' :
                myinput['lexeme'] = myinput['lexeme'][:-3]
                myinput['lexeme'] = myinput['lexeme'] + u'й'
            elif myinput['lexeme'][-4] in u'бвдзлмнпрстф' :
                myinput['lexeme'] = myinput['lexeme'][:-3]
                myinput['lexeme'] = myinput['lexeme'] + u'ь'
        else : print "V_stemmer WARNING: not processing",myinput['lemma'],'correctly.'
        if len(myinput['stress1']) >= 1 :
            if myinput['stress1'][-1] > len(myinput['lexeme']) : # if the suffix is stressed, i.e. ова́ть
                #print myinput['lexeme'],'|',len(myinput['lexeme']),'|',myinput['stress1'][-1]
                if myinput['paradigm'][-5:] != u' ёва́' and myinput['paradigm'][1] != u'b' :
                    myinput['paradigm'] = myinput['paradigm'] + u' ова́'
                #print myinput['paradigm']
    
    elif myinput['paradigm'][:1] == '1' or myinput['paradigm'][:4] == u"нп 1" :
        if u'%[x]%' not in myinput['paradigm'] and myinput['lemma'][-2] != u'с' and myinput['paradigm'][:2] != u"нп" :
            if u'ё' in myinput['paradigm'] :
                suffix_length = len(DeNumber(myinput['lemma']))-myinput['PotentialStressPositions'][-1]+1
                myinput = V_add_suffix_to_code(myinput,suffix_length)
            elif myinput['pos'][:2] == u'св' or u'pp' in myinput['paradigm'] :  # If the verb is transitive perfective/biaspectual or imperfective without an aspectual partner
                if myinput['stress1'][-1] == len(myinput['lexeme']) :
                    myinput = V_add_suffix_to_code(myinput,3)
                    myinput = add_stress(myinput)
    myinput['paradigm'] += myinput['lexc_suffix'] # for most words, this represents no change
#    else : 
#        if u'см. ' not in myinput['paradigm_details'] :
#            print "V_Stemmer WARNING: Code not found for",myinput['lemma'],myinput['paradigm'],'---',myinput['paradigm_details']
    myinput = CodeCleaner (myinput)
    return stresser ( myinput )

fiveO = [u'предо',u'пре́до']
four = [u'пред',u'пре́д']
fourO = u'возо надо низо подо разо возо́ надо́ низо́ подо́ разо́'.split()
three = u'над под воз низ раз на́д по́д во́з ни́з ра́з'.split()
threeS = u'вос нис рас во́с ни́с ра́с'.split()
threeO = u'обо ото взо изо обо́ ото́ взо́ изо́'.split()
two = u'об от вз из о́б о́т и́з'.split()
twoS = u'вс ис и́с'.split()
twoO = u'во со во́ со́'.split()
one = u'в с'.split()
prefixes_with_fleeting_vowels = fiveO + four + fourO + three + threeS + threeO + two + twoS + twoO + one

def V_star ( myinput ) : # add fleeting vowel prefixes with * in paradigm
    myinput['paradigm'] = myinput['paradigm'].replace(u'*',u'')
    for p in prefixes_with_fleeting_vowels :
        if p in myinput['lexeme'] :
            if p[-1] == u'о' :
                myinput['lexeme'] = re.sub(p,p[:-1]+u'%^Fо',myinput['lexeme'],1)
                return myinput
            elif p[-1] == u'с' and len(p) > 1 :
                myinput['lexeme'] = re.sub(p,p[:-1]+u'з%^Fо',myinput['lexeme'],1)
                return myinput
            elif len(p) >= 2 :
                if p[:-2] == u'о́' :
                    myinput['lexeme'] = re.sub(p,p[:-2]+u'%^Fо́',myinput['lexeme'],1)
                    return myinput
                else:
                    myinput['lexeme'] = re.sub(p,p+u'%^Fо',myinput['lexeme'],1)
                    return myinput
            else:
                myinput['lexeme'] = re.sub(p,p+u'%^Fо',myinput['lexeme'],1)
                return myinput
    print "ERROR: cannot add fleeting vowel to prefix in",myinput['lemma'],myinput['lexeme']
    return myinput

def CodeCleaner ( myinput ) :
    for codefields in ['paradigm','paradigm_details'] :
        myinput[codefields] = myinput[codefields].replace(u'_',u' ')
        myinput[codefields] = myinput[codefields].strip()
        for old , new in [(u':',u''),(u';',u''),(u'%tr%',u''),(u'%[x]%',u'?'),(u'%x%',u's'),
                        (u'%1%',u'1'),(u'%2%',u'2'),(u'%3%',u'3'),(u'%4%',u'4'),(u'%5%',u'5'),
                        (u'%6%',u'6'),(u'%7%',u'7'),(u'%8%',u'8'),(u'%9%',u'9'),(u' § 7',u's'),
                        (u'§ 8',u''),(u'§ 9',u''),(u' § 10',u's'),(u' § 11',u's'),(u'§ 12',u''),
                        (u'§ ',u''),(u'  ',u' '),(u'   ',u' '),(u'    ',u' '),
                        (u'<',u'['),(u'>',u']'),(u'(на)',u''),(u'(в)',u'')] :
            myinput[codefields] = myinput[codefields].replace(old,new)
        if myinput[codefields] == u' ' :
            myinput[codefields] = u''
    return myinput

def expand_variation ( myinput ) : # create multiple entries for pos/paradigms with ";" or "//"
    outList = []
    for myPOS in myinput['pos'].split(u';') :
        tempDict = copy.deepcopy(myinput)
        tempDict['pos'] = myPOS
        outList.append(tempDict)
    outList2 = []
    for d in outList : # d is a dict object
        for myPOS in d['pos'].split(u'// ') :
            tempDict2 = copy.deepcopy(d)
            tempDict2['pos'] = myPOS
            outList2.append(tempDict2)
    outList3 = []
    for d in outList2 :
        outList3.extend(expand_variation_paradigm(d))
    return outList3
    
def expand_variation_paradigm ( myinput ) :
    myParadigm = myinput['paradigm']
    outList = []
    if u'//' in myParadigm :
        if myParadigm[0] == u'<' :
            myParadigm = myParadigm[1:-1]
            if u',' in myParadigm :
                scoper = myParadigm.split(u',')
                for i in range(len(scoper)) :
                    scoper[i] = scoper[i].split(u'// ')
                for i in list(itertools.product(*scoper)) :
                    tempDict = copy.deepcopy(myinput)
                    tempDict['paradigm'] = u'<' + u' '.join(m.replace(',','').strip() for m in i) + u'>'
                    outList.append(tempDict)
            else : # if there is no comma
                print myinput['lemma'] , myParadigm , '\t\t\tPROBLEM A'
        else : # if does not begin with <
            if u',' in myParadigm :
                scoper = myParadigm.split(u',')
                for i in range(len(scoper)) :
                    scoper[i] = scoper[i].split(u'// ')
                for i in list(itertools.product(*scoper)) :
                    tempDict = copy.deepcopy(myinput)
                    tempDict['paradigm'] = ' '.join(m.replace(',','').strip() for m in i)
                    outList.append(tempDict)
            else : # if does not begin with < and there is no comma
                for paradigm in myParadigm.split(u'// ') :
                    tempDict = copy.deepcopy(myinput)
                    tempDict['paradigm'] = paradigm.replace(',','')
                    outList.append(tempDict)
    else :
        tempDict = copy.deepcopy(myinput)
        tempDict['paradigm'] = tempDict['paradigm'].replace(',','')
        outList.append(tempDict)
    return outList

def DeNumber ( lemmaname ) : # remove leading numbers from lemma, e.g. 2есть > есть
    if lemmaname[0] in u'0123456789-' :
        return DeNumber(lemmaname[1:])
    else :
        return lemmaname

def ReNumber ( lemmaname ) : # move leading numbers to end of lemma, e.g. 2есть > есть²
    myindex = 0
    while lemmaname[myindex] in u'0123456789-' :
        myindex += 1
    if myindex == 0 :
        return lemmaname
    elif myindex > 0 :
        lemmaname = lemmaname[myindex:] + lemmaname[:myindex].replace(u'1',u'¹').replace(u'2',u'²').replace(u'3',u'³').replace(u'4',u'⁴').replace(u'5',u'⁵').replace(u'6',u'⁶').replace(u'7',u'⁷').replace(u'8',u'⁸').replace(u'9',u'⁹').replace(u'0',u'⁰').replace(u'-',u'⁻')
        return lemmaname
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
        #print "WARNING: no 'е' in" , myDict['lexeme'] , "to convert to 'ё'"
        return myDict['lexeme'] , myDict['paradigm']

def dictionary_sorter ( myEntryDict ) :
    codes = myEntryDict['pos'].strip() + u' ' + myEntryDict['paradigm'].strip() + u' ' + myEntryDict['paradigm_details'].strip()
    while u'  ' in codes :
        codes = codes.replace(u'  ',u' ')

    if myEntryDict['pos'].split() :
        if myEntryDict['pos'].split()[0] in u'м мо мо-жо с со ж жо мн. ф.'.split() or u'соб' in myEntryDict['pos'] :
            if codes in Ndict :
                Ndict[codes].append(myEntryDict)
            else :
                Ndict[codes] = [myEntryDict]
        elif myEntryDict['pos'].split()[0] in u'п' :
            if codes in Adict :
                Adict[codes].append(myEntryDict)
            else :
                Adict[codes] = [myEntryDict]
        elif myEntryDict['pos'].split()[0] in u'нсв св св-нсв нсв, св, св-нсв,'.split() :
            if myEntryDict['lexeme'][-2] == u'с' and myEntryDict['PotentialStressPositions'][-1] == len(DeNumber(myEntryDict['lexeme'])) :
                myEntryDict['PotentialStressPositions'] = myEntryDict['PotentialStressPositions'][:-1]
            if codes in Vdict :
                Vdict[codes].append(myEntryDict)
            else :
                Vdict[codes] = [myEntryDict]
        elif myEntryDict['pos'] == u'н' :
            if codes in Advdict :
                Advdict[codes].append(myEntryDict)
            else :
                Advdict[codes] = [myEntryDict]
        elif myEntryDict['pos'] == u'союз' :
            if codes in Cdict :
                Cdict[codes].append(myEntryDict)
            else :
                Cdict[codes] = [myEntryDict]
        elif myEntryDict['pos'] == u'межд.' :
            if codes in Idict :
                Idict[codes].append(myEntryDict)
            else :
                Idict[codes] = [myEntryDict]
        elif myEntryDict['pos'] == u'числ. числ.-п' :
            print myEntryDict['lemma']
            if codes in Numdict :
                Numdict[codes].append(myEntryDict)
            else :
                Numdict[codes] = [myEntryDict]
        elif myEntryDict['pos'] == u'предл.' :
            if codes in Pdict :
                Pdict[codes].append(myEntryDict)
            else :
                Pdict[codes] = [myEntryDict]
        elif myEntryDict['pos'] in u'мс мс-п'.split() :
            if codes in Prodict :
                Prodict[codes].append(myEntryDict)
            else :
                Prodict[codes] = [myEntryDict]
        else : 
            if codes in Odict :
                Odict[codes].append(myEntryDict)
            else :
                Odict[codes] = [myEntryDict]
    else :
        if codes in Odict :  # leftovers
            Odict[codes].append(myEntryDict)
        else :
            Odict[codes] = [myEntryDict]

myFile = codecs.open ( 'ZalAll.csv' , mode='r' , encoding='utf-8' )
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

    entryDict['OrigZCode'] = entryDict['source'] + u': ' + entryDict['paradigm'] + u' ' + entryDict['paradigm_details']
    entryDict['VowelPositions'] = [m.start()+1 for m in Vowel.finditer(entryDict['lexeme'])]
    entryDict['stress2'] = [ i for i in entryDict['stress2'].split(u"/") ]
    if entryDict['stress2'] == [''] :
        entryDict['stress2'] = []
    else : entryDict['stress2'] = [ int(i) for i in entryDict['stress2'] ]
    entryDict['stress1'] = [ i for i in entryDict['stress1'].split(u"/") ]
    if entryDict['stress1'] == [''] or entryDict['stress1'] == ['x'] :
        entryDict['stress1'] = []
    else : entryDict['stress1'] = sorted([ int(i) for i in entryDict['stress1'] ])
    entryDict['PotentialStressPositions'] = sorted(list(set(entryDict['VowelPositions']) - set(entryDict['stress1']) - set(entryDict['stress2'])))
    if entryDict['lemma'] == "" :
        entryDict['lemma'] = entryDict['lexeme'] # if lemma is empty, copy lexeme
    if entryDict['source'] == u'ZProp' : #capitalize the lexeme
        entryDict['lexeme'] = DeNumber (entryDict['lemma'])
    if u'ё' in entryDict['lemma'] and u'ё' not in entryDict['lexeme'] : # if the lemma has a ё and lexeme doesn't, switch them
        if DeNumber(entryDict['lemma']).replace(u'ё',u'е').lower() == entryDict['lexeme'] :
            entryDict['lexeme'] = DeNumber(entryDict['lemma']).replace(u'ё',u'е').lower()
        else :
            print entryDict['lemma'] , entryDict['lexeme']
    entryDict['lemma'] = entryDict['lemma'].replace(u'ё',u'е') # remove ё from all lemmas
    if u', ё' in entryDict['paradigm'] and u'св' not in entryDict['pos'] : # non-verbs with ', ё' in Z's code
        entryDict['lexeme'] , entryDict['paradigm'] = Yoer ( entryDict ) # put ё into lexeme of nominals
    entryDict['lemma'] = entryDict['lemma'].replace(u' ',u'% ') # escape spaces in lemmas
    entryDict['lexeme'] = entryDict['lexeme'].replace(u' ',u'% ') # escape spaces in lexeme
    if entryDict['FV'] != u'' :
        entryDict['paradigm_details'] = u''

    entryDict = expand_variation(entryDict) # this embeds the entryDict(s) in list

    for e in entryDict :
        dictionary_sorter ( e )

print len(Zlist),"lines in input."
catCounter = 0
for d , n in [ (Ndict,"noun") , (Adict,"adjective") , (Vdict,"verb") , (Advdict,"adverb") , 
               (Cdict,"conjunction") , (Idict,"interjection") , (Numdict,"numeral") , 
               (Pdict,"preposition") , (Prodict,"pronoun") , (Sdict,"subjunction") , (Odict,"miscellaneous") ] :
    print len(d),'\t',n,'categories in input.'
    catCounter += len(d)
print "="*20
print "TOTAL categories:",catCounter

lexc_header = u'! ===================================================================\n'*5 +\
              u'! This lexc file is automatically generated by ../incoming/Z2.py. In \n' +\
              u"! order to permanently change this file, you must change the script's\n" +\
              u"! xslx input. Instructions can be found in the 'README' sheet of the \n" +\
              u"! Excel workbook.\n" +\
              u'! ===================================================================\n'*5 +\
              u'\n\n'

V_lexc_paradigms = codecs.open ( "../affixes/verbs.lexc" , mode='r' , encoding='utf-8' )
V_LEXICA = set([ i.split()[1] for i in V_lexc_paradigms if u'LEXICON' in i ])

A_lexc_paradigms = codecs.open ( "../affixes/adjectives.lexc" , mode='r' , encoding='utf-8' )
A_LEXICA = set([ i.split()[1] for i in A_lexc_paradigms if u'LEXICON' in i ])

N_lexc_paradigms = codecs.open ( "../affixes/nouns.lexc" , mode='r' , encoding='utf-8' )
N_LEXICA = set([ i.split()[1] for i in N_lexc_paradigms if u'LEXICON' in i ])

# with codecs.open ( "verbs.lexc" , mode='w' , encoding='utf-8' ) as Vfile :
#     print "Preparing verbs.lexc ...",
#     newVdict = {}
#     for code in Vdict :
#         for entry in Vdict[code] :
#             entry = V_stemmer(entry)
#             if entry['lexc_stem'] != u'' : 
#                 entry['lexeme'] = entry['lexc_stem']
#             elif u'*' in entry['paradigm'] :
#                 entry = V_star(entry)
#             if entry['lemma'][-2] == u"с" :
#                 entry['paradigm'] += u" R"

#             # Reduce combined length of produced LEXICON name to 56 characters (maximum for xfst compiler)
#             if len(entry['pos'] + u' ' + entry['paradigm'] + u' ' + entry['paradigm_details']) > 56 :
#                 entry['paradigm_details'] = entry['paradigm_details'][:(56-len(entry['pos'] + u' ' + entry['paradigm'] + u' '))]
#             lexicon = entry['pos'] + u' ' + entry['paradigm'] + u' ' + entry['paradigm_details']
#             lexicon = lexicon.strip()
#             while u'  ' in lexicon :
#                 lexicon = lexicon.replace(u'  ',u' ')
#             if lexicon in newVdict :
#                 newVdict[lexicon].append(entry)
#             else :
#                 newVdict[lexicon] = [entry]
#     print len(newVdict),'categories in verbs.lexc ...',
#     print "writing verbs.lexc ...",
#     Vcatslist = []
#     Vfile.write( lexc_header )
#     Vfile.write( u'LEXICON Verb\n' )
#     for each_code in sorted ( newVdict, reverse=False ) : # for each grammar code in the verb dictionary
#         Vcatslist.append([len(newVdict[each_code]),each_code,newVdict[each_code][0]['lemma'],newVdict[each_code][0]['lexeme'],])
#         code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(newVdict[each_code])) + u'\n!' + u' '*35 + each_code.replace(u" ",u"_") + u'\n'
#         Vfile.write(code_header)
#         #Vfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
#         for each_lemma in sorted ( newVdict[each_code] , key=lambda x: x['lemma'][::-1]) :
#             if each_lemma['skip'] == u'1' or each_code.replace(" ","_") not in V_LEXICA :
#                 skipper = u"! "
#             elif len(newVdict[each_code]) < 30 and each_code.replace(" ","_") not in V_LEXICA :
#                 skipper = u"! "
#             else : skipper = u""
#             if each_lemma['do_not_skip'] == u'1' :
#                 skipper = u""
#             entry = skipper + ReNumber(each_lemma['lemma']) + u":" + each_lemma['lexeme'] + u" " + each_code.replace(" ","_") + u" ;"
#             #entry += u' '*(50-len(entry)) + u"\t! " + each_lemma['pos'] + u' ' + each_lemma['paradigm'] + u' ' + each_lemma['paradigm_details']
#             entry += u'\n'
#             Vfile.write(entry)
#     Vcatsfile_freq = codecs.open ( "verb_cats_freq.txt" , mode='w' , encoding='utf-8' )
#     Vcats_counter = 0.0
#     V_total = sum(i for i,j,k,l in Vcatslist)
#     for i,j,k,l in sorted (Vcatslist,key=lambda x : x[0],reverse=True) :
#         if j.replace(" ","_") in V_LEXICA :
#             h = u''
#         else :
#             h = u'**'
#         Vcats_counter += i
#         Vcatsfile_freq.write(h+str(i)+'\t\t'+'{:.2%}'.format(Vcats_counter/V_total)+'\t\t'+j.replace(' ','_')+'\t\t'+k+'\t\t'+l+"\n")
#     Vcatsfile_freq.close()    
#     Vcatsfile_alph = codecs.open ( "verb_cats_alph.txt" , mode='w' , encoding='utf-8' )
#     Vcats_counter = 0.0
#     V_total = sum(i for i,j,k,l in Vcatslist)
#     for i,j,k,l in sorted (Vcatslist,key=lambda x : ' '.join(x[1].split()[1:]).replace(' ','_'),reverse=False) :
#         if j.replace(" ","_") in V_LEXICA :
#             h = u''
#         else :
#             h = u'**'
#         if i > 2 :
#             Vcats_counter += i
#             Vcatsfile_alph.write(h+str(i)+'\t\t'+'{:.2%}'.format(Vcats_counter/V_total)+'\t\t'+j.replace(' ','_')+'\t\t'+k+'\t\t'+l+"\n")
#     Vcatsfile_alph.close()
#     print "verbs.lexc done!"

# for d , f , l in [ (Advdict,"adverbs.lexc",u"Adverb") , (Cdict,"conjunctions.lexc",u"Conjunction") , (Idict,"interjections.lexc",u"Interjection") , 
#                (Pdict,"prepositions.lexc",u"Preposition") , (Prodict,"pronouns.lexc",u"Pronoun") , (Sdict,"subjunctions.lexc",u"Subjunction") , 
#                (Numdict,"numerals.lexc",u"Numeral") , (Odict,"other.lexc",u"THESE LEXICA NEED TO BE CATEGORIZED AND LABELED") ] :
#     print "Writing",f,"...",
#     with codecs.open ( f , mode='w' , encoding='utf-8' ) as Myfile :
#         Myfile.write( u'LEXICON ' + l + u'\n' )
#         for each_code in sorted ( d, reverse=False ) : # for each grammar code in the verb dictionary
#             code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(d[each_code])) + u'\n!' + u' '*35 + each_code.replace(u" ",u"_") + u'\n'
#             Myfile.write(code_header)
#             #Vfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
#             for each_lemma in sorted ( d[each_code] , key=lambda x: x['lemma'][::-1]) :
#                 each_lemma = stresser(each_lemma)
#                 if each_lemma['skip'] == u'1' :
#                     skipper = u"! "
#                 elif len(d[each_code]) < 30 and each_lemma['skip'] != u'-1' : # -1 in the skip column blocks that lemma from being commented out
#                     skipper = u"! "
#                 else : skipper = u""
#                 if each_lemma['do_not_skip'] == u'1' :
#                     skipper = u""
#                 entry = skipper + each_lemma['lemma'] + u":" + each_lemma['lexeme'] + u" " + each_code.replace(" ","_") + u" ;"
#                 #entry += u' '*(50-len(entry)) + u"\t! " + each_lemma['pos'] + u' ' + each_lemma['paradigm'] + u' ' + each_lemma['paradigm_details']
#                 entry += u'\n'
#                 Myfile.write(entry)
#     print "Done!"

# with codecs.open ( "adjectives.lexc" , mode='w' , encoding='utf-8' ) as Afile :
#     print "Preparing adjectives.lexc ...",
#     newAdict = {}
#     for code in Adict :
#         for entry in Adict[code] :
#             entry = A_stemmer(entry)
#             if u'́' not in entry['lexeme'] and u'ё' not in entry['lexeme'] and entry['lexeme'] != u'' :
#                 entry = add_stress_directly( entry )
#             if u'<мс' not in entry['paradigm'] :
#                 entry['paradigm'] = re.sub( "[1-7]" , "" , entry['paradigm'] , count = 1 )
#             else : # if it is a pronoun declension
#                 if entry['lemma'][-2] == u'́' :
#                     entry['paradigm'] += entry['lemma'][-3:]
#                 else :
#                     entry['paradigm'] += entry['lemma'][-2:]
#             entry = CodeCleaner(entry)
#             if entry['lexc_stem'] != u'' :
#                 entry['lexeme'] = entry['lexc_stem']

#             # Reduce combined length of produced LEXICON name to 56 characters (maximum for xfst compiler)
#             if len(entry['pos'] + u' ' + entry['paradigm'] + u' ' + entry['paradigm_details']) > 56 :
#                 entry['paradigm_details'] = entry['paradigm_details'][:(56-len(entry['pos'] + u' ' + entry['paradigm'] + u' '))]
#             lexicon = entry['pos'] + u' ' + entry['paradigm'] + u' ' + entry['paradigm_details']
#             lexicon = lexicon.strip()
#             while u'  ' in lexicon :
#                 lexicon = lexicon.replace(u'  ',u' ')
#             if lexicon in newAdict :
#                 newAdict[lexicon].append(entry)
#             else :
#                 newAdict[lexicon] = [entry]
#     print len(newAdict),'categories in adjectives.lexc ...',
#     print "writing adjectives.lexc ...",
#     Acatslist = []
#     Afile.write( lexc_header )
#     Afile.write( u"! DON'T FORGET THAT ....\n ! adjectives 2*a ~Fений have masc short-form in 0, not ь\n! DON'T FORGET!!\n\n")
#     Afile.write( u'LEXICON Adjective\n' )
#     for each_code in sorted ( newAdict, reverse=False ) : # for each grammar code in the verb dictionary
#         Acatslist.append([len(newAdict[each_code]),each_code,newAdict[each_code][0]['lemma'],newAdict[each_code][0]['lexeme'],])
#         code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(newAdict[each_code])) + u'\n!' + u' '*35 + each_code.replace(u" ",u"_") + u'\n'
#         Afile.write(code_header)
#         #Afile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
#         for each_lemma in sorted ( newAdict[each_code] , key=lambda x: x['lemma'][::-1]) :
#             if each_lemma['skip'] == u'1' or each_code.replace(" ","_") not in A_LEXICA :
#                 skipper = u"! "
#             elif len(newAdict[each_code]) < 30 and each_code.replace(" ","_") not in A_LEXICA :
#                 skipper = u"! "
#             else : skipper = u""
#             if each_lemma['do_not_skip'] == u'1' :
#                 skipper = u""
#             entry = skipper + ReNumber(each_lemma['lemma']) + u":" + each_lemma['lexeme'] + u" " + each_code.replace(" ","_") + u" ;"
#             entry += u' '*(50-len(entry)) + u"\t! " + each_lemma['OrigZCode']
#             entry += u'\n'
#             Afile.write(entry)
#     Acatsfile_freq = codecs.open ( "adj_cats_freq.txt" , mode='w' , encoding='utf-8' )
#     Acats_counter = 0.0
#     A_total = sum(i for i,j,k,l in Acatslist)
#     for i,j,k,l in sorted (Acatslist,key=lambda x : x[0],reverse=True) :
#         if j.replace(" ","_") in A_LEXICA :
#             h = u''
#         else :
#             h = u'**'
#         Acats_counter += i
#         Acatsfile_freq.write(h+str(i)+'\t\t'+'{:.2%}'.format(Acats_counter/A_total)+'\t\t'+j.replace(' ','_')+'\t\t'+k+'\t\t'+l+"\n")
#     Acatsfile_freq.close()    
#     Acatsfile_alph = codecs.open ( "adj_cats_alph.txt" , mode='w' , encoding='utf-8' )
#     Acats_counter = 0.0
#     A_total = sum(i for i,j,k,l in Acatslist)
#     for i,j,k,l in sorted (Acatslist,key=lambda x : ' '.join(x[1].split()[1:]).replace(' ','_'),reverse=False) :
#         if j.replace(" ","_") in A_LEXICA :
#             h = u''
#         else :
#             h = u'**'
#         Acats_counter += i
#         Acatsfile_alph.write(h+str(i)+'\t\t'+'{:.2%}'.format(Acats_counter/A_total)+'\t\t'+j.replace(' ','_')+'\t\t'+k+'\t\t'+l+"\n")
#     Acatsfile_alph.close()
#     print "adjectives.lexc done!"

with codecs.open ( "nouns.lexc" , mode='w' , encoding='utf-8' ) as Nfile :
    print "Preparing nouns.lexc ...",
    newNdict = {}
    for code in Ndict :
        for entry in Ndict[code] :
            entry = N_stemmer(entry)
            entry['paradigm'] = re.sub( "[1-7]" , "" , entry['paradigm'] , count = 1 )
            entry = CodeCleaner(entry)
            if entry['lexc_stem'] != u'' :
                entry['lexeme'] = entry['lexc_stem']

            # Reduce combined length of produced LEXICON name to 56 characters (maximum for xfst compiler)
            if len(entry['pos'] + u' ' + entry['paradigm'] + u' ' + entry['paradigm_details']) > 56 :
                entry['paradigm_details'] = entry['paradigm_details'][:(56-len(entry['pos'] + u' ' + entry['paradigm'] + u' '))]
            lexicon = entry['pos'] + u' ' + entry['paradigm'] + u' ' + entry['paradigm_details']
            lexicon = lexicon.strip()
            while u'  ' in lexicon :
                lexicon = lexicon.replace(u'  ',u' ')
            if lexicon in newNdict :
                newNdict[lexicon].append(entry)
            else :
                newNdict[lexicon] = [entry]
    print len(newNdict),'categories in nouns.lexc ...',
    print "writing nouns.lexc ...",
    Ncatslist = []
    Nfile.write( lexc_header )
    Nfile.write( u'LEXICON Noun\n' )
    for each_code in sorted ( newNdict, reverse=False ) : # for each grammar code in the verb dictionary
        Ncatslist.append([len(newNdict[each_code]),each_code,newNdict[each_code][0]['lemma'],newNdict[each_code][0]['lexeme'],])
        code_header = u'! '+'='*60 + u'  Types in Zaliznjak: ' + str(len(newNdict[each_code])) + u'\n!' + u' '*35 + each_code.replace(u" ",u"_") + u'\n'
        Nfile.write(code_header)
        #Nfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
        for each_lemma in sorted ( newNdict[each_code] , key=lambda x: x['lemma'][::-1]) :
            if each_lemma['skip'] == u'1' or each_code.replace(" ","_") not in N_LEXICA :
                skipper = u"! "
            elif len(newNdict[each_code]) < 15 and each_code.replace(" ","_") not in N_LEXICA :
                skipper = u"! "
            else : skipper = u""
            if each_lemma['do_not_skip'] == u'1' :
                skipper = u""
            entry = skipper + ReNumber(each_lemma['lemma']) + u":" + each_lemma['lexeme'] + u" " + each_code.replace(" ","_") + u" ;"
            #entry += u' '*(50-len(entry)) + u"\t! " + each_lemma['pos'] + u' ' + each_lemma['paradigm'] + u' ' + each_lemma['paradigm_details']
            entry += u'\n'
            Nfile.write(entry)
    Ncatsfile_freq = codecs.open ( "noun_cats_freq.txt" , mode='w' , encoding='utf-8' )
    Ncats_counter = 0.0
    N_total = sum(i for i,j,k,l in Ncatslist)
    for i,j,k,l in sorted (Ncatslist,key=lambda x : x[0],reverse=True) :
        if j.replace(" ","_") in N_LEXICA :
            h = u''
        else :
            h = u'**'
        Ncats_counter += i
        Ncatsfile_freq.write(h+str(i)+'\t\t'+'{:.2%}'.format(Ncats_counter/N_total)+'\t\t'+j.replace(' ','_')+'\t\t'+k+'\t\t'+l+"\n")
    Ncatsfile_freq.close()    
    Ncatsfile_alph = codecs.open ( "noun_cats_alph.txt" , mode='w' , encoding='utf-8' )
    Ncats_counter = 0.0
    N_total = sum(i for i,j,k,l in Ncatslist)
    for i,j,k,l in sorted (Ncatslist,key=lambda x : ' '.join(x[1].split()[1:]).replace(' ','_'),reverse=False) :
        if j.replace(" ","_") in N_LEXICA :
            h = u''
        else :
            h = u'**'
        Ncats_counter += i
        Ncatsfile_alph.write(h+str(i)+'\t\t'+'{:.2%}'.format(Ncats_counter/N_total)+'\t\t'+j.replace(' ','_')+'\t\t'+k+'\t\t'+l+"\n")
    Ncatsfile_alph.close()
    print "nouns.lexc done!"

