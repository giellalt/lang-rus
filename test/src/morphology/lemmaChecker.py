import sys
import re

# USAGE:
# $ cat inputfile | python3.4 lemmachecker.py

enumerators = re.compile('[¹²³⁴⁵⁶⁷⁸⁹⁰⁻]*')

def lemmaChecker( groupList ) : #returns lemma if it fails
	myLemma = groupList[0].split('+')[0]
	mySurface = enumerators.sub('',myLemma)
	for i in groupList :
		if i.split()[1].replace('\u0300','').replace('\u0301','') == mySurface :
			return False
	return myLemma

lemmagroup = []
for line in sys.stdin :
	if 'myDelimiter' not in line :
		if line != '\n' :
			lemmagroup.append( line.strip() )
	else :
		result = lemmaChecker( lemmagroup )
		if result :
			sys.stdout.write( result + '\n' )
		lemmagroup = []

sys.stdout.flush()