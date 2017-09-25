#!/usr/bin/env python3

import argparse, re
import xml.etree.ElementTree as ET

from lxml.html import fromstring, parse, etree

from subprocess import Popen, PIPE

import os

import cglib
from rnctags import weeDict as tagDict
from rnctags import rnc2cg
from rnclib import which

stressMark = '`'
cacheDir = ""
posMappings = {
		'V': 'vblex', # ipf:impf, pf:perf, tran:tv, intr:iv
		'ADV': 'adv',
		'A': 'adj',
		'S': 'n', # f, m, n, inan:nn
		#'S': 'np.al',
		'S.persn': 'np.ant', # f, m
		'A-PRO': 'prn.pos', # det.pos?
		'S-PRO': 'prn.pers',
		'PR': 'pr',
		'CONJ': 'cnjcoo', # etc.
		'INTJ': 'ij'
		# ADV-PRO ?
	}

def parseRnc(fn):
	global stressMark
	with open(fn, 'r', encoding="windows-1251") as corpusFile:
		content = corpusFile.read()
	corpusTree = ET.fromstring(content)

	return corpusTree

def printRnc(corpus, stress=False):
	for sent in corpus.iter('se'):
		words = []
		for word in sent.itertext():
			if word.strip()!='':
				if not stress:
					word = re.sub(stressMark, "", word)
				words.append(word.strip())

		print(' '.join(words))

def printRncAsCg(corpus, stress=False, tags=False, uniq=False):
	global stressMark
	for word in corpus.findall('.//se/w'):
		wd = ''.join(word.itertext())
		if not stress:
			wd = re.sub(stressMark, "", wd)
		anas = word.findall('ana')
		#if len(anas)==1:
		#	ana = anas[0].attrib
		#else: print("FIXME: more than one analysis!!!  Keeping only first for the moment")
		##for ana in word.findall('ana'):
		##	print(ana.attrib)
		for thisAna in anas: #word.findall('ana'):
			ana = thisAna.attrib
			if uniq:
				print('.'.join(ana['gr'].replace('=', ',').split(',')))
			elif tags:
				print(ana['gr'])
			else:
				print(wd, ana)

def getRncWords(se, stress=False):
	global stressMark
	words = []
	for word in se.findall('.//w'):
		analyses = []
		token = ''.join(word.itertext())
		if not stress:
			token = re.sub(stressMark, "", token)
		anas = word.findall('ana')
		for ana in anas:
			lemma = ana.attrib['lex']
			tags = ana.attrib['gr']
			thisAna = {lemma: tags}
			analyses.append(thisAna)
		words.append({token: analyses})
	return words


def getRncSentences(corpus, stress=False):
	global stressMark
	for se in corpus.findall('.//se'):
		sentence = textContents(se, stress=stress)
		words = getRncWords(se, stress=stress)
		yield (sentence, words)


def textContents(elem, stress=False):
	htmlTree = fromstring(ET.tostring(elem))
	output = re.sub('[\n \r]+', ' ', htmlTree.text_content()).strip()
	if not stress:
		output = re.sub(stressMark, "", output)

	return(output)


def getSentences(corpus, stress=False):
	global stressMark
	for se in corpus.findall('.//se'):
		sentence = textContents(se, stress=stress)
		yield sentence

def analyseCg(corpus, stress=False, verbosity=0):
	if verbosity>0:
		if which("rusmorph.sh"):
			print("rusmorph.sh found")
		else:
			print("SHARKS: rusmorph.sh NOT FOUND")
	for sentence in getSentences(corpus, stress=False):
		p1 = Popen(["echo", sentence], stdout=PIPE)
		p2 = Popen(["rusmorph.sh"], stdin=p1.stdout, stdout=PIPE, shell=True)
		p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
		output = p2.communicate()[0]
		yield output.decode()

def getCorpusCg(corpus, filename, stress=False, force=False, verbosity=0):
	global cacheDir

	# get the cache directory
	dirname = os.path.dirname(filename)
	cacheDir = os.path.join(dirname, '.cache')
	if(not os.path.exists(cacheDir)):
		os.mkdir(cacheDir)

	# make the filename for the cg file
	(base, ext) = os.path.splitext(os.path.basename(filename))
	cgBase = base + '.cg'
	cgFn = os.path.join(cacheDir, cgBase)

	# if no cache file, or if being forced to recache, create and fill cache
	if (not os.path.exists(cgFn)) or force:
		with open(cgFn, 'w') as cgFile:
			for sentence in analyseCg(corpus, stress, verbosity=verbosity):
				cgFile.write(sentence)

	# return contents of cache file as Sentences object
	with open(cgFn, 'r') as cgFile:
		content = cgFile.read()
	return cglib.Sentences(content, verbosity = verbosity)

def writeFiltered(filename, sentences):

	# make the filename for the output file
	(base, ext) = os.path.splitext(os.path.basename(filename))
	output = base + '.filtered'

	# write it
	with open(output, 'w') as outFile:
		add = ""
		for sent in sentences:
			outFile.write(add+str(sent))
			add = "\n\n"


def tagsMatch(tags, search):
	# takes tags as list of tags, search as tag string (e.g. "n.pl")
	#print(tags, search)
	if tags is not None and search is not None:
		for idx, searchTag in enumerate(search.split('.')):
			#print(idx)
			if searchTag != tags[idx]:
				return False

		return True
	else:
		return False

#def addInRNCTags(corpusRnc, corpusCg):

def guessAlxworezm(sentenceRnc, parsesCg, curW, token, lemma):
	rnctags = list(sentenceRnc[1][curW][token.token][0].items())[0][1]
	rnclemma = list(sentenceRnc[1][curW][token.token][0].items())[0][0]
	rncParse = {rnclemma: rnctags}
	#print(rncParse)
	parseRnc = rnc2cg(rncParse)
	#"<Кинзмараул>"
	#print(rncParse)
	#print(parsesCg)
	remainingParses = {}
	exactMatched = False
	for parse in parsesCg:
		cglemma = parse.lemma
		if cglemma != None and "*" not in cglemma and len(parsesCg) > 1:
			#print(cglemma.strip("¹").strip("²").strip("³").strip("⁴"))
			if cglemma.strip("¹").strip("²").strip("³").strip("⁴") != rnclemma:
				parse.comment("REMOVE:LemmaNot_"+rnclemma)
			else:
				#print(parse.tags, parseRnc[lemma])
				#if len(parseRnc[lemma])==1:
				toAppend = []
				for singleTag in parseRnc[lemma]:
					#print(singleTag)
					if not isinstance(singleTag, str):
						#print("LIST")
						toAppend += singleTag
						parseRnc[lemma].remove(singleTag)
				for listTag in toAppend:
					parseRnc[lemma].append(listTag)
				#print(parseRnc[lemma])
						#parseRnc[lemma].del(singleTag)
				#print(parse.tags, parseRnc[lemma])

				intersection = set(parse.tags).intersection(parseRnc[lemma])
				numMatchingTags = len(intersection)
				if numMatchingTags == len(parse.tags):
					parse.addDecision("SELECT:ExactMatch")
					exactMatched = True
				else:
					#thisRemainingParse = [parse, numMatchingTags]
					if numMatchingTags not in remainingParses:
						remainingParses[numMatchingTags] = []
					remainingParses[numMatchingTags].append(parse)
	if exactMatched:
		for parse in parsesCg:
			if not parse.isSelected():
				parse.comment("REMOVE:NotExactMatch")
	else:
		if remainingParses != {}:
			#print(remainingParses)
			maxKey = max(remainingParses.keys())
			#print(maxKey)
			if maxKey > 0:
				for num in remainingParses:
					for remainingParse in remainingParses[num]:
						#print(remainingParse, parseRnc, num)
							if num < maxKey:
								#print(remainingParse)
								remainingParse.comment("REMOVE:LessThanMaxTags")
							elif num == maxKey:
								remainingParse.addDecision("SELECT:MaxMatchingTags")



def compareRncCg(corpusRnc, corpusCg, stress=False, algorithm="POS", orig=False, info=False, verbosity=0):
	global cacheDir
	global posMappings
	#print(corpusCg)

	outSents = []
	dragons = 0
	for (sentenceRnc, sentenceCg) in zip(getRncSentences(corpusRnc, stress=stress), corpusCg.all()):
		#sentlen = len(sentenceCg)
		#print(len(sentenceCg), len(sentenceRnc[1]))
		#print(sentenceCg, sentenceRnc[1])
		curW = 0
		for token in sentenceCg.tokens:
			if not token.punctInParses():
				if curW >= len(sentenceRnc[1]):
					if verbosity>1:
						print("DRAGONS", sentenceRnc[1])
					dragons += 1
				else:
					#print(token.token, sentenceRnc[1][cur])

					if token.token in sentenceRnc[1][curW]:

						# split Rnc tags
						parsesRnc = sentenceRnc[1][curW][token.token]
						parsesCg = token.parses
						#print(token.token, parsesCg, parsesRnc)
						curParse = 0
						for parse in parsesRnc:
							for lemma in parse:
								splitTags = parse[lemma].replace('=', ',').split(',')
								sentenceRnc[1][curW][token.token][curParse][lemma] = splitTags
								#print(splitTags)
							curParse += 1
							#print(token.token, parsesCg, sentenceRnc[1][curW][token.token])


						if len(sentenceRnc[1][curW][token.token]) > 1:
							if verbosity > 1:
								print("SKIPPING: more than one filter ({}), undefined behaviour".format(len(sentenceRnc[1][curW][token.token])), sentenceRnc[1][curW][token.token])
						else:

							# check if Rnc parse in Cg parses
							# for now just check first tag
							if algorithm=="POS":
								firstTag = list(sentenceRnc[1][curW][token.token][0].items())[0][1][0]
								if firstTag in posMappings:
									for parse in parsesCg:
										#print(parse.tags)
										found = tagsMatch(parse.tags, posMappings[firstTag])
										if not found:
											parse.comment("REMOVE:"+firstTag)
										else:
											parse.addDecision("SELECT:"+firstTag)
								else:
									print(firstTag, "not in POS list!")

							# check if Rnc parse in Cg parses
							# REMOVE analyses with no matching tags
							# SELECT analyses where all convertible tags match
							# otherwise SELECT analysis with most matches
							elif algorithm=="guess":
								guessAlxworezm(sentenceRnc, parsesCg, curW, token, lemma)
						if orig:
							for RNCParse in parsesRnc:
								lem = list(RNCParse.keys())[0]
								tagz = RNCParse[lem]
								tagz.append("@RNC")
								textTagz = " ".join(tagz)
								stuffs = (lem, textTagz)
								#print(stuffs)
								parseToAdd = ";  \"{}\" {}".format(stuffs[0], stuffs[1])
								#print(parseToAdd)
								token.addParse(parseToAdd,where=0)



				curW += 1
		#print(str(sentenceCg))
		outSents.append(sentenceCg)
	if info:
		print("Number of sentences: {}".format(len(outSents)))
		print("Number of sentences with tokenisation errors: {}".format(dragons))
	return outSents


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='rnc 2 cg mangler')
	parser.add_argument('corpus', help="uri to a corpus file")
	parser.add_argument('-s', '--stress', help="preserve stress marks", action='store_true', default=False)
	parser.add_argument('-c', '--clean', help="print clean output", action='store_true', default=False)
	parser.add_argument('-d', '--debug', help="print raw corpus for debugging", action='store_true', default=False)
	parser.add_argument('-t', '--tags', help="tags only", action='store_true', default=False)
	parser.add_argument('-u', '--uniq', help="unique tags only", action='store_true', default=False)
	parser.add_argument('-a', '--analyse', help="analyse all sentences with rusmorph.sh and cache the analyses", action='store_true', default=False)
	parser.add_argument('-m', '--algorithm', help="algorithm to use for comparison: pos or guess", action='store', default='pos')
	parser.add_argument('-f', '--force', help="force cached cg to be regenerated", action='store_true', default=False)
	#parser.add_argument('-o', '--output', help="output CG file", action='store')
	parser.add_argument('-O', '--original', help="add in original RNC tags with @RNC tag", action='store_true', default=False)
	parser.add_argument('-i', '--info', help="print additional information", action='store_true', default=False)
	parser.add_argument('-v', '--verbosity', help="level of verbosity (0 = none, 1 = critial warnings only, 2-5 = all warnings)", action='store', type=int, default=0)

	args = parser.parse_args()

	corpus = parseRnc(args.corpus)

	if(args.clean):
		printRnc(corpus, stress=args.stress)
	elif(args.debug):
		printRncAsCg(corpus, stress=args.stress, tags=args.tags, uniq=args.uniq)
	elif(args.analyse):
		analyseCg(corpus, stress=args.stress)
	else:
		corpusCg = getCorpusCg(corpus, args.corpus, force=args.force, stress=args.stress, verbosity=args.verbosity)
		#print(corpusCg)
		sentencesCg = compareRncCg(corpus, corpusCg, stress=args.stress, algorithm=args.algorithm, orig=args.original, info=args.info, verbosity=args.verbosity)
		writeFiltered(args.corpus, sentencesCg)
