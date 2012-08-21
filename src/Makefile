# This is a makefile that builds the Russian morphological parser
# *****************************************************************
# This is a dummy file. Russian refers to the name of the language, rus to the
# ISO code of the language, for use in file names.

# This is a preliminary file that builds a Russian parser based upon
# xfst and not twolc.

# Here we build the final generator , an inverted transducer of the analyzer.
# It is dependent upon rus.save

XFST = xfst
LEXC = lexc
TWOLC = twolc

GTLANG=rus

ifeq (victorio.uit.no, $(shell hostname))
XFST = /opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/fst -utf8
LEXC = /opt/sami/xerox/bin/lexc -utf8
TWOLC = /opt/sami/xerox/bin/twolc -utf8
endif

ifeq (gramadeg, $(shell hostname))
XFST = /home/pasha/bin/xfst -utf8
LEXC = /home/pasha/bin/lexc -utf8
TWOLC = /home/pasha/bin/twolc -utf8
endif


LEX = $(GTLANG)-lex.txt \
	  noun-$(GTLANG)-lex.txt \
	  noun-$(GTLANG)-morph.txt \
	  propernoun-$(GTLANG)-lex.txt \
	  propernoun-$(GTLANG)-morph.txt \
	  adj-$(GTLANG)-lex.txt \
	  adj-$(GTLANG)-morph.txt \
	  verb-$(GTLANG)-lex.txt \
	  verb-$(GTLANG)-morph.txt \
	  adv-$(GTLANG)-lex.txt \
#	  abbr-$(GTLANG)-lex.txt \
#	  acro-$(GTLANG)-lex.txt \
	  pron-$(GTLANG)-lex.txt \
	  punct-$(GTLANG)-lex.txt \
	  numeral-$(GTLANG)-lex.txt \
	  pp-$(GTLANG)-lex.txt \
	  cc-$(GTLANG)-lex.txt \
	  cs-$(GTLANG)-lex.txt \
	  interj-$(GTLANG)-lex.txt

all: \
	$(GTLANG).fst        \
	i$(GTLANG).fst       \
	iclock-$(GTLANG).fst \
	idate-$(GTLANG).fst  \
	$(GTLANG)-inum.fst   \
	cyr2lat_no.fst


i$(GTLANG).fst: ../bin/i$(GTLANG).fst
../bin/i$(GTLANG).fst: ../bin/$(GTLANG).save
	@echo
	@echo "*** Building the inverse $(@F) ***"
	@echo
	$(XFST) -e "load < $<" \
			-e "invert net" \
			-e "save stack $@" \
			-stop


# This goal is to build the final analyser. It depends on all the files.

$(GTLANG).fst: ../bin/$(GTLANG).fst
../bin/$(GTLANG).fst: ../bin/$(GTLANG).save ../bin/inituppercase.fst
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "read regex [[@\"$<\"] .o. [@\"../bin/inituppercase.fst\"]] ;" \
			-e "save stack $@" \
			-stop


# The second goal is to build the inituppercase.fst file
# This goal depends on inituppercase.regex

inituppercase.fst: ../bin/inituppercase.fst
../bin/inituppercase.fst: inituppercase.regex
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "read regex < $<" \
			-e "save stack $@" \
			-stop


# The first goal is to build $(GTLANG)-lex.save
# This goal depends on a bunch of lexicon files

$(GTLANG).save: ../bin/$(GTLANG).save
../bin/$(GTLANG).save: ../bin/twol-$(GTLANG).bin $(LEX)
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	printf "compile-source $(LEX) \n\
	read-rules $< \n\
	compose-result \n\
	save-result $@ \n\
	quit \n" > ../../tmp/$(GTLANG)-lex-save-script
	$(LEXC) <  ../../tmp/$(GTLANG)-lex-save-script
	rm -f      ../../tmp/$(GTLANG)-lex-save-script

# The second goal is to build xfst-$(GTLANG).bin
# This goal depends on xfst-$(GTLANG).txt

twol-$(GTLANG).bin: ../bin/two-$(GTLANG).bin
../bin/twol-$(GTLANG).bin: twol-$(GTLANG).txt
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	@printf "read-grammar $< \n\
	compile \n\
	save-binary $@ \n\
	quit \n" > ../../tmp/twol-$(GTLANG)-script
	$(TWOLC) < ../../tmp/twol-$(GTLANG)-script
	@rm -f     ../../tmp/twol-$(GTLANG)-script


# Here are two goals for making cyrillic to latin converters
# and vice versa.

cyr2lat_no.fst: ../bin/cyr2lat_no.fst
../bin/cyr2lat_no.fst: cyr2lat_no.xfst
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "source $<" \
			-e "save stack $@" \
			-stop

lat2cyr_no.fst: ../bin/lat2cyr_no.fst
../bin/lat2cyr_no.fst: lat2cyr_no.xfst
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "source $<" \
			-e "save stack $@" \
			-stop


idate-$(GTLANG).fst: ../bin/idate-$(GTLANG).fst
../bin/idate-$(GTLANG).fst: ../bin/date-$(GTLANG).fst
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "load < $<" \
			-e "invert net" \
			-e "save stack $@" \
			-stop

date-$(GTLANG).fst: ../bin/date-$(GTLANG).fst
../bin/date-$(GTLANG).fst: date-$(GTLANG).lexc
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "read lexc $<" \
			-e "save stack $@" \
			-stop



iclock-$(GTLANG).fst: ../bin/iclock-$(GTLANG).fst
../bin/iclock-$(GTLANG).fst: ../bin/clock-$(GTLANG).fst
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "load < $<" \
			-e "invert net" \
			-e "save stack $@" \
			-stop


clock-$(GTLANG).fst: ../bin/clock-$(GTLANG).fst
../bin/clock-$(GTLANG).fst: clock-$(GTLANG).lexc
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "read lexc $<" \
			-e "save stack $@" \
			-stop


$(GTLANG)-inum.fst: ../bin/$(GTLANG)-inum.fst
../bin/$(GTLANG)-inum.fst: ../bin/$(GTLANG)-num.fst
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "load < $<" \
			-e "invert net" \
			-e "save stack $@" \
			-stop

$(GTLANG)-num.fst: ../bin/$(GTLANG)-num.fst
../bin/$(GTLANG)-num.fst: $(GTLANG)-num.txt
	@echo
	@echo "*** Building $(@F) ***" ;
	@echo
	$(XFST) -e "read lexc $<" \
			-e "save stack $@" \
			-stop



clean:
	@rm -f ../bin/*.bin ../bin/*.fst ../bin/*.save
