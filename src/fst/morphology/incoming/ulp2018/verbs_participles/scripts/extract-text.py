#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
import re
import string

#mypath="../test/"
mypath="../snjatnik_decoded"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

print(onlyfiles)
#reading the list of files and their content

def constructTextSavetoFile(tokensList, file):
    tokenized = [str for str in tokensList if str]
    extractedText=untokenize(tokenized)
    with open("../snjatnik_texts/"+file.replace(".utf8.xhtml",".txt"), "w") as outfile:
        outfile.write(extractedText)
    outfile.close()

def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()

for f in onlyfiles:
    tokensList=[]
    print(f)
    infile = open("../snjatnik_decoded/"+f, "r")
    lines=infile.read()
    #regex=r"</ana>(.*?)</w>(\s?string.punctuation)(?:\n<w>|</se></p>|</se>\n<se>)"#searching for blocks in file content
    #(?:\n?|</se>)
    #regex:</ana>(.*)</w>(?:\s)?([!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]|--|[.,])?(?:\n?|</se>)
    #regex=r"</ana>(.+?)</w>(.*?)(?:</se>(?:\n?</?p>| \n<se>)|\n)"
    regex=r"(?:(?:</ana>(.*?)</w>(?:.*?)(?:(.*?)</se>|\s?\n))|<se>(.*?)\n)"
    matches = re.findall(regex, lines, re.MULTILINE)
    # Example of the output:
    # [('М', '.,'), ('2002', '.'), ('19', '.'), ('Правила', ''), ('регистрации', ''), ('граждан', ''), ('по', ''), ('месту', ''), ('жительства', ''), ('и', ''), ('пребывания', ' .'), ('Паспортный', ''), ('режим', ' .'), ('М', '.,'), ('2000', '.')]
    #print(matches)
    for match in matches:
        for el in match:
            el1=el.replace(" ", "")#remove whitespace from characters, e.g. ' .' => '.'
            tokensList.append(el1)
    print(constructTextSavetoFile(tokensList, f))
    infile.close()

    # tokenized = [str for str in tokensList if str]
    # extractedText=untokenize(tokenized)
    # print(extractedText)
    # outfile.write(extractedText)
    # outfile.close()
    # infile.close()



    #FROM:
    # ['М', '.,', '2002', '.', '19', '.', 'Правила', 'регистрации', 'граждан', 'по', 'месту', 'жительства', 'и', 'пребывания', '.', 'Паспортный', 'режим', '.', 'М', '.,', '2000', '.']
    #TO:
    #М., 2002. 19. Правила регистрации граждан по месту жительства и пребывания. Паспортный режим. М., 2000.





# #tokenized=list(filter(None, tokensList))
#tokenized = [str for str in tokensList if str]#remove empty lines from list
#print(tokenized)

#print(untokenize(tokenized))
#FROM:
# ['М', '.,', '2002', '.', '19', '.', 'Правила', 'регистрации', 'граждан', 'по', 'месту', 'жительства', 'и', 'пребывания', '.', 'Паспортный', 'режим', '.', 'М', '.,', '2000', '.']
#TO:
#М., 2002. 19. Правила регистрации граждан по месту жительства и пребывания. Паспортный режим. М., 2000.
#</ana>(.+?)</w>(.*?)(?:</se>(?:</p>| \n<se>)|\n)
#</se> \n<se>

#</ana>(.+?)</w>(.*?)(?:</se>(?:\n?</?p>| \n<se>)|\n)
