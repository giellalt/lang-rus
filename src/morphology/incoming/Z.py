#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

def stresser2 ( input ) : # places secondary stress (grave accent)
    position = input.find('>')
    if position == -1 :
        return input
    if position > -1 :
        inputList = list(input)
        inputList[position] = inputList[position+1]
        inputList[position+1] = u'\u0300'
        return stresser2 (''.join(inputList))

def stresser ( input ) : # places primary stress (acute accent), then calls stresser2 to place 2ndary stress
    position = input.find('<')
    if position == -1 :
        return stresser2 (input)
    if position > -1 :
        inputList = list(input)
        inputList[position] = inputList[position+1]
        inputList[position+1] = u'\u0301'
        return stresser (''.join(inputList))

def Nstemmer ( input ) : # strips final vowel
    if input[-1:] in u'аоыяеёи' :
        input = input[:-1]
    if input[-1:] == u'<' :
        input = input[:-1]
    return stresser ( input )

myFile = codecs.open ( 'Zaliznjak_IlolaMustajoki_UTF8_orig.txt' , mode='r' , encoding='utf-8' )
Zlist = myFile.readlines()
Ndict = {} # Nouns
Adict = {} # Adjectives
Vdict = {} # Verbs
Odict = {} # miscellaneous
Hdict = {} # for now, exclude lemmas with homonym notation at position 30
for n in range(len(Zlist)) :
    lemma = Zlist[n][:24].strip().lower()
    number = Zlist[n][25:29]
    homonymy = Zlist[n][29:30]
    lexeme = Zlist[n][30:].split()[0].lower()
    codesList = Zlist[n][30:].split()[1:]
    codes = ' '.join(Zlist[n][30:].split()[1:])
    #print lemma,number,homonymy,lexeme,codes
    if homonymy != u" " :
        if codes in Hdict :
            Hdict[codes].append([lemma,number,homonymy,lexeme])
        else :
            Hdict[codes] = [[lemma,number,homonymy,lexeme]]
    elif codesList[0] in u'м мо мо-жо с со ж жо'.upper().split() :
        if codes in Ndict :
            Ndict[codes].append([lemma,number,homonymy,lexeme])
        else :
            Ndict[codes] = [[lemma,number,homonymy,lexeme]]
    elif codesList[0] == u'П' :
        if codes in Adict :
            Adict[codes].append([lemma,number,homonymy,lexeme])
        else :
            Adict[codes] = [[lemma,number,homonymy,lexeme]]
    elif codesList[0] in u'нсв св св-нсв'.upper().split() :
        if codes in Vdict :
            Vdict[codes].append([lemma,number,homonymy,lexeme])
        else :
            Vdict[codes] = [[lemma,number,homonymy,lexeme]]
    else :
        if codes in Odict :
            Odict[codes].append([lemma,number,homonymy,lexeme])
        else :
            Odict[codes] = [[lemma,number,homonymy,lexeme]]

print len(Zlist),"lines in input."
print len(Ndict)+len(Adict)+len(Vdict)+len(Odict)+len(Hdict),'categories in output.'
print len(Ndict),'\tnoun categories in output.'
print len(Adict),'\tadjective categories in output.'
print len(Vdict),'\tverb categories in output.'
print len(Odict),'\tother word categories in output.'
print len(Hdict),'\thomonymous word categories in output.'

with codecs.open ( "Noutput.txt" , mode='w' , encoding='utf-8' ) as Nfile :
    for k in sorted ( Ndict, key=lambda k: len(Ndict[k]), reverse=True ) :
        code_header = u'!' + u'===  '*5 + k + u'  ==='*5 + u'\n' + u'!' + u'===  '*5 + str(len(Ndict[k])) + u'  ==='*5 + u'\n'
        print k + '\t' + str(len(Ndict[k]))
        Nfile.write(code_header)
        for v in sorted ( Ndict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+stresser(v[3])+u" "+k.replace(" ","_")+u" ;\n"
            Nfile.write(entry)

with codecs.open ( "Aoutput.txt" , mode='w' , encoding='utf-8' ) as Afile :
    for k in sorted ( Adict, key=lambda k: len(Adict[k]), reverse=True ) :
        code_header = u'===  '*5+k+u'  ==='*5+u'\n'+u'===  '*5+str(len(Adict[k]))+u'  ==='*5+u'\n'
        Afile.write(code_header)
        for v in sorted ( Adict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+v[3]+u" "+k.replace(" ","_")+u" ;\n"
            Afile.write(entry)

with codecs.open ( "Voutput.txt" , mode='w' , encoding='utf-8' ) as Vfile :
    for k in sorted ( Vdict, key=lambda k: len(Vdict[k]), reverse=True ) :
        code_header = u'===  '*5+k+u'  ==='*5+u'\n'+u'===  '*5+str(len(Vdict[k]))+u'  ==='*5+u'\n'
        Vfile.write(code_header)
        for v in sorted ( Vdict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+v[3]+u" "+k.replace(" ","_")+u" ;\n"
            Vfile.write(entry)

with codecs.open ( "Ooutput.txt" , mode='w' , encoding='utf-8' ) as Ofile :
    for k in sorted ( Odict, key=lambda k: len(Odict[k]), reverse=True ) :
        code_header = u'===  '*5+k+u'  ==='*5+u'\n'+u'===  '*5+str(len(Odict[k]))+u'  ==='*5+u'\n'
        Ofile.write(code_header)
        for v in sorted ( Odict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+v[3]+u" "+k.replace(" ","_")+u" ;\n"
            Ofile.write(entry)

with codecs.open ( "Houtput.txt" , mode='w' , encoding='utf-8' ) as Hfile :
    for k in sorted ( Hdict, key=lambda k: len(Hdict[k]), reverse=True ) :
        code_header = u'===  '*5+k+u'  ==='*5+u'\n'+u'===  '*5+str(len(Hdict[k]))+u'  ==='*5+u'\n'
        Hfile.write(code_header)
        for v in sorted ( Hdict[k] , key=lambda x: x[0][::-1]) :
            entry = v[0]+u":"+v[3]+u" "+k.replace(" ","_")+u" ;\n"
            Hfile.write(entry)
