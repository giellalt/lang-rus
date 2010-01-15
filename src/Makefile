# This is a makefile that builds the Russian morphological parser
# *****************************************************************
# This is a dummy file. Russian refers to the name of the language, rus to the 
# ISO code of the language, for use in file names.

# This is a preliminary file that builds a Russian parser based upon
# xfst and not twolc.

# Here we build the final generator , an inverted transducer of the analyzer.
# It is dependent upon rus.save

XFST = xfst #-utf8
LEXC = lexc #-utf8
TWOLC = twolc #-utf8

ifeq (victorio.uit.no, $(shell hostname))
XFST = /opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/fst -utf8
LEXC = /opt/sami/xerox/bin/lexc -utf8
TWOLC = /opt/sami/xerox/bin/twolc -utf8
endif



irus.fst: ../bin/irus.fst
../bin/irus.fst: ../bin/rus.fst
	@echo
	@echo "*** Building the inverse irus.fst ***"
	@echo
	@printf "load ../bin/rus.save \n\
	invert net \n\
	save stack ../bin/irus.fst \n\
	quit \n" > ../../tmp/irus-fst-script
	$(XFST) < ../../tmp/irus-fst-script
	@rm -f ../../tmp/irus-fst-script


# This goal is to build the final analyser. It depends on all the files.

rus.fst: ../bin/rus.fst
../bin/rus.fst: ../bin/rus.save ../bin/inituppercase.fst
	@echo
	@echo "*** Building rus.fst ***" ;
	@echo
	@printf "read regex [[@\"../bin/rus.save\"] .o. \
	[@\"../bin/inituppercase.fst\"]] ; \n\
	save stack ../bin/rus.fst \n\
	quit \n" > ../../tmp/rus-fst-script
	$(XFST) < ../../tmp/rus-fst-script
	@rm -f ../../tmp/rus-fst-script


# The second goal is to build the inituppercase.fst file
# This goal depends on inituppercase.regex

inituppercase.fst: ../bin/inituppercase.fst
../bin/inituppercase.fst: inituppercase.regex
	@echo
	@echo "*** Building inituppercase.fst ***" ;
	@echo
	@printf "read regex < inituppercase.regex \n\
	save stack ../bin/inituppercase.fst \n\
	quit \n" > ../../tmp/inituppercase-script
	$(XFST) < ../../tmp/inituppercase-script
	@rm -f ../../tmp/inituppercase-script


# The first goal is to build rus-lex.save
# This goal depends on a bunch of lexicon files

rus.save: ../bin/rus.save
../bin/rus.save: ../bin/twol-rus.bin rus-lex.txt noun-rus-lex.txt noun-rus-morph.txt \
	adj-rus-lex.txt adj-rus-morph.txt verb-rus-lex.txt verb-rus-morph.txt \
	adv-rus-lex.txt pron-rus-lex.txt punct-rus-lex.txt cc-rus-lex.txt \
	cs-rus-lex.txt pp-rus-lex.txt numeral-rus-lex.txt interj-rus-lex.txt
	@echo
	@echo "*** Building rus-lex.save ***" ;
	@echo
	printf "compile-source rus-lex.txt noun-rus-lex.txt noun-rus-morph.txt \
	adj-rus-lex.txt verb-rus-lex.txt verb-rus-morph.txt pron-rus-lex.txt \
	adj-rus-morph.txt adv-rus-lex.txt pp-rus-lex.txt punct-rus-lex.txt \
	cc-rus-lex.txt cs-rus-lex.txt numeral-rus-lex.txt interj-rus-lex.txt \n\
	read-rules ../bin/twol-rus.bin \n\
	compose-result \n\
	save-result ../bin/rus.save \n\
	quit \n" > ../../tmp/rus-lex-save-script
	$(LEXC) < ../../tmp/rus-lex-save-script
	rm -f ../../tmp/rus-lex-save-script

# The second goal is to build xfst-rus.bin
# This goal depends on xfst-rus.txt

twol-rus.bin: ../bin/two-rus.bin
../bin/twol-rus.bin: twol-rus.txt
	@echo
	@echo "*** Building twol-rus.bin ***" ;
	@echo
	@printf "read-grammar twol-rus.txt \n\
	compile \n\
	save-binary ../bin/twol-rus.bin \n\
	quit \n" > ../../tmp/twol-rus-script
	$(TWOLC) < ../../tmp/twol-rus-script
	@rm -f ../../tmp/twol-rus-script

clean:
	@rm -f ../bin/*.bin ../bin/*.fst ../bin/*.save


