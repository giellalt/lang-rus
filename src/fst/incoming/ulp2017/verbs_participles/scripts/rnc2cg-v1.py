#!/usr/bin/env python3

import argparse, re
import xml.etree.ElementTree as ET

from lxml.html import fromstring, parse, etree

from subprocess import Popen, PIPE

import os

# import cglib
# from rnctags import weeDict as tagDict
# from rnctags import rnc2cg
# from rnclib import which

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

corpus=sys.arg[0]

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
