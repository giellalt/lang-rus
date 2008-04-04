# This is a makefile that builds the Russian morphological parser
# *****************************************************************
# This is a dummy file. Russian refers to the name of the language, rus to the 
# ISO code of the language, for use in file names.

# This is a preliminary file that builds a Russian parser based upon
# xfst and not twolc.

# Here we build the final generator , an inverted transducer of the analyzer.
# It is dependent upon rus.save

irus.fst: ../bin/irus.fst
../bin/irus.fst: ../bin/rus.fst
	@echo
	@echo "*** Building the inverse irus.fst ***"
	@echo
	@printf "load ../bin/rus.save \n\
	invert net \n\
	save stack ../bin/irus.fst \n\
	quit \n" > ../../tmp/irus-fst-script
	@xfst -utf8 < ../../tmp/irus-fst-script
	@rm -f ../../tmp/irus-fst-script


# This goal is to build the final analyser. It depends on all the files.

rus.fst: ../bin/rus.fst
../bin/rus.fst: ../bin/rus.save ../bin/caseconv.fst
	@echo
	@echo "*** Building rus.fst ***" ;
	@echo
	@printf "read regex [[@\"../bin/rus.save\"] .o. \
	[@\"../bin/caseconv.fst\"]] ; \n\
	save stack ../bin/rus.fst \n\
	quit \n" > ../../tmp/rus-fst-script
	@xfst -utf8 < ../../tmp/rus-fst-script
	@rm -f ../../tmp/rus-fst-script


# The second goal is to build the caseconv.fst file
# This goal depends on case.regex

caseconv.fst: ../bin/caseconv.fst
../bin/caseconv.fst: case.regex
	@echo
	@echo "*** Building caseconv.fst ***" ;
	@echo
	@printf "read regex < case.regex \n\
	save stack ../bin/caseconv.fst \n\
	quit \n" > ../../tmp/caseconv-script
	@xfst -utf8 < ../../tmp/caseconv-script
	@rm -f ../../tmp/caseconv-script


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
	@lexc -utf8 < ../../tmp/rus-lex-save-script
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
	@twolc -utf8 < ../../tmp/twol-rus-script
	@rm -f ../../tmp/twol-rus-script

clean:
	@rm -f ../bin/*.bin ../bin/*.fst ../bin/*.save


