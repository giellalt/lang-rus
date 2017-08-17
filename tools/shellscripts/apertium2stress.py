"""With given HFST generator, convert apertium-tagged text to stressed text."""
import pexpect
# import random
import re
# import subprocess
import sys


# INPUT:
#  ^Все/весь¹<det><mfn><nn><pl><acc>/весь¹<det><nt><sg><acc>/весь¹<det><nt><sg><nom>/весь¹<det><pl><nom>/все<prn><pl><nom>/всё<prn><nt><sg><acc>/всё<prn><nt><sg><nom>$ ^счастливые/счастливый<adj><mfn><an><pl><nom>/счастливый<adj><mfn><nn><pl><acc>$ ^семьи/семья<n><f><nn><pl><acc>/семья<n><f><nn><pl><nom>/семья<n><f><nn><sg><gen>$ ^похожи/похожий<adj><short><mfn><pl>$ ^друг на друга/на<pr>+друг друга<prn><recip><acc>$^,/,<cm>$ ^каждая/каждая<prn><f><sg><nom>/каждый<det><f><sg><nom>$ ^несчастливая/несчастливый<adj><f><an><sg><nom>$ ^семья/семья<n><f><nn><sg><nom>$ ^несчастлива/несчастливый<adj><short><f><sg>$ ^по-своему/по-своему<adv>$^./.<sent>$^./.<sent>$[][
#
#]
#
# OUTPUT:
#  Все счастли́вые семьи похо́жи дру̀г на дру́га, ка́ждая несчастли́вая семья́ несча́стлива по-сво́ему..[][
#
#]
#
#
# USAGE:
#  $ cat inputfile | python3 apertium2stress.py <path/to/apertium-generator>

Vowel = re.compile('[аэоуыяеёюи]')
# Capital = re.compile('[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯА́Э́О́У́Ы́Я́Е́Ё́Ю́И́А̀Э̀О̀У̀Ы̀Я̀ЀЁ̀Ю̀Ѝ]')
Roman = re.compile('[IVXLCDMivxlcdm]*')  # Latin characters, roman numerals


def capitalizer(inputStr, inputList):
    myList = []
    for i in reversed(inputList):
        myList = [inputStr[i:]] + myList
        inputStr = inputStr[:i]
    return ''.join([i.capitalize() for i in myList])


class Token:
    def __init__(self, surface):
        self.surface = surface
        # list of indices of letters in the original token that are capitalized
        self.capIndexList = [i for i in range(len(surface))
                             if surface[i].isupper()]
        self.readingsdict = {}
        self.wordformsdict = {}

    def add(self, reading, wordform):
        # sys.stderr.write('add() input:' + reading + ' || ' + wordform + '\n')
        if len(self.capIndexList) > 0:
            wordform = capitalizer(wordform, self.capIndexList)
        # sys.stderr.write('add() input after capitalizer: ' + reading
        #                  + ' || ' + wordform + '\n')
        if wordform.lower().replace('\u0301', '').replace('\u0300', '').replace('ё', 'е') != self.surface.lower().replace('\u0301', '').replace('ё', 'е'):
            sys.stderr.write("\t\tWARNING B: Wordform does not match original token! Not included. " + self.surface + ' > ' + wordform + ' || ' + reading + '\n')
        elif reading not in self.readingsdict:
            self.readingsdict[reading] = [wordform]
        elif wordform not in self.readingsdict[reading]:
            self.readingsdict[reading].append(wordform)
            sys.stderr.write("\t\tWARNING A: Too many wordforms associated "
                             "with " + reading + ': ' +
                             '/'.join(self.readingsdict[reading]) + '\n')

        if wordform not in self.wordformsdict:
            self.wordformsdict[wordform] = [reading]
        elif reading not in self.wordformsdict[wordform]:
            self.wordformsdict[wordform].append(reading)

    def isInsane(self):
        """Return True if token is unknown or if any of the readings return the
        same spelling as the surface form.
        """
        if '*' in ''.join(self.readingsdict):  # unknown token
            return True

        for r in self.readingsdict:
            for newSurface in self.readingsdict[r]:
                if newSurface.lower().replace('\u0301', '').replace('\u0300', '').replace('ё', 'е') == self.surface.lower().replace('\u0301', '').replace('\u0300', '').replace('ё', 'е'):
                    return False
        sys.stderr.write('\t\tINSANE: None of the suggested forms match the '
                         'original! Returning original surface form: (' +
                         self.surface + ') with readings:' +
                         '/'.join(list(self.wordformsdict)) + '\n')
        return True

    # def bare(self):
    #     # if self.isInsane():
    #     #     return self.surface
    #     if len(self.readingsdict) == 1:
    #         return self.readingsdict[list(self.readingsdict)[0]][0]
    #     else:
    #         return self.surface

    def safe(self, guesser=''):
        # if self.isInsane():
        #     return self.surface
        if len(self.wordformsdict) == 1:
            return list(self.wordformsdict)[0]
        else:
            if guesser == 'guessSyll':
                return self.guessSyll()
            else:
                return self.surface

    # def guess(self, backoff='none'):
    #     # if self.isInsane():
    #     #     if backoff == 'none':
    #     #         return self.surface
    #     #     if backoff == 'guessSyll':
    #     #         return self.guessSyll()
    #     # sys.stderr.write('DEBUG C:(guess) '+filename+"|"+self.surface+"||"+str(len(self.readingsdict))+"|||"+"_".join(list(self.readingsdict))+"\n")
    #     if len(self.readingsdict) > 0:
    #         randomchoice = random.choice(list(self.readingsdict))
    #         return self.readingsdict[randomchoice][0]
    #     else:
    #         # sys.stderr.write('\t\tBACKOFF to guessSyll: '+self.surface+' || '+"/".join(list(self.readingsdict))+"\n")
    #         return self.guessSyll()

    # def guessFreq(self, backoff='none'):
    #     # if self.isInsane():
    #     #     if backoff == 'none':
    #     #         return self.surface
    #     #     if backoff == 'guessSyll':
    #     #         return self.guessSyll()
    #     myReading = (0, '')
    #     myTag = (0, '')
    #     for r in self.readingsdict:
    #         if '<' in r:
    #             tagSeq = r[r.index('<'):]
    #         else:
    #             tagSeq = ' ' * 16  # forces tag backoff to fail if no '<'
    #
    #         if tagSeq in tagFreqDict:
    #             if tagFreqDict[tagSeq] > myTag[0]:
    #                 myTag = (tagFreqDict[tagSeq], r)
    #
    #         if r in lemtagFreqDict:
    #             if lemtagFreqDict[r] > myReading[0]:
    #                 myReading = (lemtagFreqDict[r], r)
    #
    #     if myReading[0] > 0:
    #         # sys.stderr.write('\t\tGUESSFREQ by reading: '+self.surface+' || '+"/".join(list(self.readingsdict))+"\n")
    #         return self.readingsdict[myReading[1]][0]
    #     elif myTag[0] > 0:
    #         # sys.stderr.write('\t\tGF BACKOFF to tagSeq: '+self.surface+' || '+"/".join(list(self.readingsdict))+"\n")
    #         return self.readingsdict[myTag[1]][0]
    #     else:
    #         # sys.stderr.write('\t\tGF BACKOFF to guess: '+self.surface+' || '+"/".join(list(self.readingsdict))+"\n")
    #         if backoff == 'none':
    #             return self.surface
    #         if backoff == 'guessSyll':
    #             return self.guessSyll()

    # def guessSyll(self):
    #     """Place stress on the last vowel followed by a consonant."""
    #     # This is a (bad) approximation of the last syllable of the stem.
    #     # Not reliable at all, especially for forms with a consonant in the
    #     # grammatical ending.
    #     if 'ё' in self.surface or '\u0301' in self.surface:
    #         # sys.stderr.write('\t\tDEBUG A: guessSyll returning surface:'+self.surface+' || '+"/".join(list(self.readingsdict))+"\n")
    #         return self.surface
    #     surfaceRev = self.surface[::-1]
    #     # sys.stderr.write('Reversed surface: (' + surfaceRev + ')\n')
    #     while surfaceRev != '' and surfaceRev[0] in 'аэоуыяеёюи':
    #         surfaceRev = surfaceRev[1:]
    #     tempSurfaceLen = len(surfaceRev)
    #     VowelMatches = [i.start() for i in Vowel.finditer(self.surface)
    #                     if i.start() < tempSurfaceLen]
    #     if len(VowelMatches) > 0:
    #         stressIndex = VowelMatches[-1] + 1
    #         # sys.stderr.write('\t\tDEBUG B: GuessSyll called. Returning ' + self.surface[:stressIndex] + '\u0301' + self.surface[stressIndex:] + '.  (surface = ' + self.surface + ')\n')
    #         return self.surface[:stressIndex] + '\u0301' + self.surface[stressIndex:]
    #     else:
    #         # sys.stderr.write('\t\tWARNING C: GuessSyll failed; no vowels detected. Returning ' + self.surface + '.\n')
    #         return self.surface

    # def recall(self):
    #     return 'V'.join([w for w in self.wordformsdict])


c = sys.stdin.read(1)

generatorLoc = sys.argv[1]

myGenerator = pexpect.spawnu('hfst-lookup ' + generatorLoc)
myGenerator.expect('> ')

# barefile = open(filename + 'bare.preretxt.tmp', 'w')
# safefile = open(filename + 'safe.preretxt.tmp', 'w')
# guessfile = open(filename + 'guess.preretxt.tmp', 'w')
# guessFreqfile = open(filename + 'guessFreq.preretxt.tmp', 'w')
# guessSyllfile = open(filename + 'guessSyll.preretxt.tmp', 'w')
# guessFreqSyllfile = open(filename + 'guessFreqSyll.preretxt.tmp', 'w')

# recallfile = open(filename + 'recall.preretxt.tmp', 'w')

# tagFreqFile = open('../corpora/wordlists/apertium-tag-freq-list.txt', 'r')
# tagFreqDict = {}
# for line in tagFreqFile:
#     f, t = line.split(' ', maxsplit=1)
#     tagFreqDict[t.strip()] = int(f)
# lemtagFreqFile = open('../corpora/wordlists/apertium-lemtag-freq-list.txt', 'r')
# lemtagFreqDict = {}
# for line in lemtagFreqFile:
#     f, r = line.split(' ', maxsplit=1)
#     lemtagFreqDict[r.strip()] = int(f)

cache = {}
state = 0
surface = ''
analyses = []
analysis = ''
while c != '':
    if not c:
        break
    if c == '^':
        state = 1
        c = sys.stdin.read(1)
        continue
    elif c == '/':
        if analysis != '':
            analyses.append(analysis.strip('/'))
        analysis = ''
        state = 2
    elif c == '$':
        if analysis != '':
            analyses.append(analysis.strip('/'))
        uniq_list_analyses = [i for i in set(analyses) if '+?' not in i]
        # generate forms here.
        results = Token(surface)
        for analysis in uniq_list_analyses:
            # sys.stderr.write('analysis is: ' + analysis + '\n')
            # analysis = analysis.replace('"', '\\"');
            if analysis[0].isupper() and '<np>' not in analysis:
                analysis = analysis.lower()
                # sys.stderr.write('\tnow analysis is: ' + analysis + '\n')
            result = ''
            if analysis not in cache:
                myGenerator.sendline(analysis)
                myGenerator.expect('> ')
                result = myGenerator.before.strip()
                # print([result])

                # result = subprocess.check_output('echo ' + '"^'+analysis+'$"' + ' | hfst-proc -n ' + generatorLoc + ' 2>/dev/null' , shell=True)
                # result = result.decode('utf-8').strip();
                cache[analysis] = result
                # sys.stderr.write('generator output: ' + analysis + ' ||| ' + result + '\n')
            else:
                result = cache[analysis]
            if result.count('\n') > 0:
                for res in result.split('\n')[1:]:
                    res = res.strip('\/').split('\t')[1]
                    if res != '':
                        results.add(analysis, res)
            else:
                res = result.split('\t')[1]
                results.add(analysis, res)
        if not results.isInsane():
            # barefile.write(results.bare())
            # safefile.write(results.safe())
            sys.stdout.write(results.safe())
            # guessfile.write(results.guess())
            # guessFreqfile.write(results.guessFreq())
            # guessSyllfile.write(results.guess(backoff='guessSyll'))
            # guessFreqSyllfile.write(results.guessFreq(backoff='guessSyll'))
            # recallfile.write(results.recall())
        else:
            # barefile.write(results.surface)
            # safefile.write(results.surface)
            sys.stdout.write(results.surface)
            # guessfile.write(results.surface)
            # guessFreqfile.write(results.surface)
            # guessSyllfile.write(results.guessSyll())
            # guessFreqSyllfile.write(results.guessSyll())
            # recallfile.write(results.recall())
        sys.stdout.flush()
        state = 0
        analysis = ''
        analyses = []
        surface = ''
        c = sys.stdin.read(1)
        continue

    if state == 0:  # if just started, or just wrote out result to stdout
        # barefile.write(c)
        # safefile.write(c)
        sys.stdout.write(c)
        # guessfile.write(c)
        # guessFreqfile.write(c)
        # guessSyllfile.write(c)
        # guessFreqSyllfile.write(c)
        # recallfile.write(c)

    elif state == 1:  # if just saw a ^ (collecting surface form)
        surface = surface + c
    elif state == 2:  # if just saw a / (collecting analyses)
        analysis = analysis + c

    c = sys.stdin.read(1)
