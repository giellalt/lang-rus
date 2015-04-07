import sys

# USAGE:
# $ cat inputfile | python3 lemmaStager.py { noun , propernoun , adjective , verb }

POS = sys.argv[1]
if POS == 'noun' :
	myTagSeqs = []
	for gender in ['+Msc','+Neu','+Fem'] :
		for animacy in ['+Inan','+Anim'] :
			for number in ['+Sg','+Pl'] :
				myTagSeqs.append('+N'+gender+animacy+number+'+Nom')
	for animacy in ['+Inan','+Anim','+AnIn'] :
		myTagSeqs.append('+N+MFN'+animacy+'+Pl+Nom')
	myTagSeqs.append('+N+MFN+Inan+Pl+Gen')
if POS == 'propernoun' :
	myTagSeqs = []
	for gender in ['+Msc','+Neu','+Fem'] :
		for animacy in ['+Inan','+Anim'] :
			for number in ['+Sg','+Pl'] :
				myTagSeqs.append('+N+Prop'+gender+animacy+number+'+Nom')
	for animacy in ['+Inan','+Anim','+AnIn'] :
		myTagSeqs.append('+N+Prop+MFN'+animacy+'+Pl+Nom')
elif POS == 'adjective' :
	myTagSeqs = ['+A+Msc+AnIn+Sg+Nom','+A+Msc+AnIn+Sg+Nom+Fac','+A+Msc+Sg+Pred','+A+Cmpnd']
elif POS == 'verb' :
	myTagSeqs = ['+V+Impf+IV+Inf','+V+Impf+TV+Inf','+V+Perf+IV+Inf','+V+Perf+TV+Inf']

for lemma in sys.stdin :
	for tags in myTagSeqs :
		sys.stdout.write(lemma.strip()+tags+'\n')
	sys.stdout.write('myDelimiter\n')

sys.stdout.flush()
