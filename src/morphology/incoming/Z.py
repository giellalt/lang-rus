#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Noun codes

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
# 
# 
# 
# 
# 
# 
# 
# Delimiters: , ; : TRIANGLE DIAMOND HATCHED-CIRCLE 

import codecs
import re

def stresser2 ( myinput ) : # places secondary stress (grave accent)
    position = myinput.find('>')
    if position == -1 :
        return myinput
    if position > -1 :
        inputList = list(myinput)
        inputList[position] = inputList[position+1]
        inputList[position+1] = u'\u0300'
        return stresser2 (''.join(inputList))

def stresser ( myinput ) : # places primary stress (acute accent), then calls stresser2 to place 2ndary stress.
    position = myinput.find('<')
    if position == -1 :
        return stresser2 (myinput)
    if position > -1 :
        inputList = list(myinput)
        if inputList[position+1] == u'ё' :
            del inputList[position]
        else :
            inputList[position] = inputList[position+1]
            inputList[position+1] = u'\u0301'
        return stresser (''.join(inputList))

def CodeCleaner ( myinput ) : 
    output = re.sub( "\(_.*?_\)" , "" , myinput )                 # remove irrelevant semantic labels
    output = re.sub( "\\[\\/\\/.*?\\]" , "" , output )            # remove variant labels
    output = re.sub( "\\<(.*?)\\>" , "[\\1]" , output )         # change <  > to [ ]   
    output = output.replace( '"' , "=" )                          # change " to =    
    output = output.replace( '<' , "'" )                          # change < to '    
    return output.strip()

def NStemCodeStrip ( myinput ) : # remove stem labels and fleeting vowel markers
    output = re.sub( " [1-7]" , " " , myinput )
    output = re.sub( "\\*" , "" , output )
    return output

Cons = re.compile(u"[бвгджзйклмнпрстфхцчшщ]")
Vow = re.compile(u"[аяоёеыи]")
StressRE = re.compile(u"[<>]")

def A_stemmer ( instem , code ) :
    instem = instem[:-2]
    if instem[-1:] == u"<" :
        instem = instem[:-1]
    if u'***' in code or ( not  '**' in code and '*' in code ) :    # If the code indicates that there is a fleeting vowel
        instem = list(instem)
        instem.insert(len(instem)-1,u"F")
        instem = ''.join(instem)
    return stresser ( instem )

def N_stemmer ( instem , code ) :
    if u"<П " not in code :
        if u'***' in code or ( not  '**' in code and '*' in code ) :    # If the code indicates that there is a fleeting vowel
            instem = instem[::-1]
            Cindex = Cons.search(instem)
            Vindex = Vow.search(instem)
            Sindex = StressRE.search(instem)
            if Cindex.start() > Vindex.start() : # if the stem ends in a vowel...
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
        return stresser ( instem )
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
        #print k + '\t' + str(len(Ndict[k]))
        Nfile.write(code_header)
        Nfile.write(u'! THIS CATEGORY UNVERIFIED (delete this line when the computer-generated code has been verified by hand)\n')
        for v in sorted ( Ndict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+N_stemmer ( v[3] , k )+u" "+k2.replace(u" ",u"_")+u" ;"
            entry += u' '*(50-len(entry))+u"\t! "+v[2]+u'\t'+v[4]+u'\n'
            if not u'\u0301' in entry :
                entry += u'WARNING: no stress on stem\n'
            Nfile.write(entry)
        Nfile.write( u'\n' )

with codecs.open ( "adjectives.lexc" , mode='w' , encoding='utf-8' ) as Afile :
    print "Writing adjectives.lexc ..."
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
            entry = v[0]+u":"+stresser(v[3])+u" "+k2.replace(u" ",u"_")+u" ;"
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
            entry = v[0]+u":"+stresser(v[3])+u" "+k2.replace(u" ",u"_")+u" ;"
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
                entry = v[0]+u":"+stresser(v[3])+u" "+k2.replace(u" ",u"_")+u" ;"
                entry += u' '*(50-len(entry))+u"\t! "+v[2]+u'\t'+v[4]+u'\n'
                Myfile.write(entry)
