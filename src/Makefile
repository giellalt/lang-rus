# This is a makefile that builds the Russian morphological parser
# *****************************************************************
# This is a dummy file. Russian refers to the name of the language, rus to the 
# ISO code of the language, for use in file names.

# This is a preliminary file that builds a Russian parser based upon
# xfst and not twolc.

# Here we build the final generator , an inverted transducer of the analyzer.
# It is dependent upon rus.save

ifeq (victorio.uit.no, $(shell hostname))
XFST = /opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/fst -utf8
LEXC = /opt/sami/xerox/bin/lexc -utf8
TWOLC = /opt/sami/xerox/bin/twolc -utf8
endif

XFST = xfst #-utf8
LEXC = lexc #-utf8
TWOLC = twolc #-utf8



LEX = rus-lex.txt \
	  noun-rus-lex.txt \
	  noun-rus-morph.txt \
	  propernoun-rus-lex.txt \
	  propernoun-rus-morph.txt \
	  adj-rus-lex.txt \
	  adj-rus-morph.txt \
	  verb-rus-lex.txt \
	  verb-rus-morph.txt \
	  adv-rus-lex.txt \
#	  abbr-rus-lex.txt \
#	  acro-rus-lex.txt \
	  pron-rus-lex.txt \
	  punct-rus-lex.txt \
	  numeral-rus-lex.txt \
	  pp-rus-lex.txt \
	  cc-rus-lex.txt \
	  cs-rus-lex.txt \
	  interj-rus-lex.txt 



irus.fst: ../bin/irus.fst
../bin/irus.fst: ../bin/rus.fst \
		../bin/cyr2lat_no.fst \
		../bin/lat2cyr_no.fst \
		../bin/idate-rus.fst \
		../bin/iclock-rus.fst \
		../bin/rus-inum.fst
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
../bin/rus.save: ../bin/twol-rus.bin $(LEX)
	@echo
	@echo "*** Building rus-lex.save ***" ;
	@echo
	printf "compile-source $(LEX) \n\
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


# Here are two goals for making cyrillic to latin converters
# and vice versa.

cyr2lat_no.fst: ../bin/cyr2lat_no.fst
../bin/cyr2lat_no.fst: cyr2lat_no.xfst
	@echo
	@echo "*** Building cyr2lat.fst ***" ;
	@echo
	@printf "source $< \n\
	save stack $@ \n\
	quit \n" > ../tmp/cyr2lat-script
	$(XFST) < ../tmp/cyr2lat-script
	@rm -f ../tmp/cyr2lat-script

lat2cyr_no.fst: ../bin/lat2cyr_no.fst
../bin/lat2cyr_no.fst: lat2cyr_no.xfst
	@echo
	@echo "*** Building lat2cyr.fst ***" ;
	@echo
	@printf "source $< \n\
	save stack $@ \n\
	quit \n" > ../tmp/lat2cyr-script
	$(XFST) < ../tmp/lat2cyr-script
	@rm -f ../tmp/lat2cyr-script


idate-rus.fst: ../bin/idate-rus.fst
../bin/idate-rus.fst: ../bin/date-rus.fst
	@echo
	@echo "*** $(@F) ***"
	@echo
	@$(XFST) -e "load < $<" \
			-e "invert net" \
			-e "save stack $@" \
			-stop

date-rus.fst: ../bin/date-rus.fst
../bin/date-rus.fst: date-rus.lexc
	@echo
	@echo "*** $(@F) ***"
	@echo
	$(XFST) -e "read lexc $<" \
			-e "save stack $@" \
			-stop





iclock-rus.fst: ../bin/iclock-rus.fst
../bin/iclock-rus.fst: ../bin/clock-rus.fst
	@echo
	@echo "*** $(@F) ***"
	@echo
	@$(XFST) -e "load < $<" \
			-e "invert net" \
			-e "save stack $@" \
			-stop


clock-rus.fst: ../bin/clock-rus.fst
../bin/clock-rus.fst: clock-rus.lexc
	@echo
	@echo "*** $(@F) ***"
	@echo
	$(XFST) -e "read lexc $<" \
			-e "save stack $@" \
			-stop


rus-inum.fst: ../bin/rus-inum.fst
../bin/rus-inum.fst: ../bin/rus-num.fst
	@echo
	@echo "*** $(@F) ***"
	@echo
	@$(XFST) -e "load < $<" \
			-e "invert net" \
			-e "save stack $@" \
			-stop

rus-num.fst: ../bin/rus-num.fst
../bin/rus-num.fst: rus-num.txt
	@echo
	@echo "*** $(@F) ***"
	@echo
	$(XFST) -e "read lexc $<" \
			-e "save stack $@" \
			-stop



clean:
	@rm -f ../bin/*.bin ../bin/*.fst ../bin/*.save


