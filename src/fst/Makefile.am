## Process this file with automake to produce Makefile.in
## Copyright: Sámediggi/Divvun/UiT
## Licence: GPL v3+

# always build . last here, and tagsets have to be built after morphology
SUBDIRS = morphology filters phonetics syllabification orthography transcriptions tagsets . test

####### Automake targets: ########

# Define target variables first, before assigning to them:
GT_ANALYSERS=
GT_GENERATORS=
CUSTOM_FSTS=

#### Local modifications in *fst processing: ####
####
#### Copy the fallback targets, and rename them to the desired targets. Then:
#### Replace the 'cp' command (Xerox) / Prepend the hfst-invert command (Hfst -
#### remember to move the $<) with whatever you need to complete
#### the processing to get the final target transducer.
#### Remember to add the dependencies as well.
#### Also make sure that HFST and Xerox processing are the same.
####
#### If you add new transducers to be built, you need to add them to the
#### relevant variable, e.g.:
####
#### if CAN_HFST
#### GT_GENERATORS+=generator-oahpa-gt-norm.hfst
#### endif
####
#### NB!!!! The HFST targets should get a hyphen after 'analyser'/'generator'
#### respectively, to make the local targets minimally different from and
#### slightly more specific than the fallback targets. This is to avoid warnings
#### about duplicate targets. That is, the local targets should looke like:
####
#### analyser-%.hfst: analyser-%.tmp.hfst
#### generator-%.hfst: generator-%.tmp.hfst

##################################################################
#### BEGIN: Add local processing instructions BELOW this line ####
##################################################################

########################################################
#### Add language-specific transducer targets here: ####

#### HFST transducers
if CAN_HFST
GT_ANALYSERS+=
GT_GENERATORS+=

if WANT_L2
GT_ANALYSERS+=analyser-gt-desc-L2.hfst

# L2 Phonology rules
RULES_MAIN := phonology-rules/twolc_header  \
    phonology-rules/000  phonology-rules/001  phonology-rules/002  \
    phonology-rules/003  phonology-rules/004  phonology-rules/005  \
    phonology-rules/006  phonology-rules/007  phonology-rules/008  \
    phonology-rules/009  phonology-rules/010  phonology-rules/011  \
    phonology-rules/012  phonology-rules/013  phonology-rules/014  \
    phonology-rules/015  phonology-rules/016  phonology-rules/017  \
    phonology-rules/018  phonology-rules/019  phonology-rules/020  \
    phonology-rules/021  phonology-rules/022  phonology-rules/023  \
    phonology-rules/024  phonology-rules/025  phonology-rules/026  \
    phonology-rules/027  phonology-rules/028  phonology-rules/029  \
    phonology-rules/030  phonology-rules/031  phonology-rules/032  \
    phonology-rules/033  phonology-rules/034  phonology-rules/035  \
    phonology-rules/036  phonology-rules/037  phonology-rules/038  \
    phonology-rules/039  phonology-rules/040  phonology-rules/041  \
    phonology-rules/042  phonology-rules/043  phonology-rules/044  \
    phonology-rules/045  phonology-rules/046  phonology-rules/047  \
    phonology-rules/048  phonology-rules/049

RULES_L2_FV := phonology-rules/twolc_header  \
    phonology-rules/000  phonology-rules/001  phonology-rules/002b \
    phonology-rules/003b phonology-rules/004b phonology-rules/005  \
    phonology-rules/006  phonology-rules/007  phonology-rules/008  \
    phonology-rules/009  phonology-rules/010  phonology-rules/011  \
    phonology-rules/012  phonology-rules/013  phonology-rules/014  \
    phonology-rules/015  phonology-rules/016  phonology-rules/017  \
    phonology-rules/018  phonology-rules/019  phonology-rules/020  \
    phonology-rules/021  phonology-rules/022  phonology-rules/023  \
    phonology-rules/024  phonology-rules/025  phonology-rules/026  \
    phonology-rules/027  phonology-rules/028  phonology-rules/029  \
    phonology-rules/030  phonology-rules/031  phonology-rules/032  \
    phonology-rules/033  phonology-rules/034  phonology-rules/035  \
    phonology-rules/036  phonology-rules/037  phonology-rules/038  \
    phonology-rules/039  phonology-rules/040  phonology-rules/041  \
    phonology-rules/042  phonology-rules/043  phonology-rules/044  \
    phonology-rules/045  phonology-rules/046  phonology-rules/047  \
    phonology-rules/048  phonology-rules/049

RULES_L2_NoFV := phonology-rules/twolc_header  \
    phonology-rules/000  phonology-rules/001  phonology-rules/002a \
    phonology-rules/003a phonology-rules/004a phonology-rules/005  \
    phonology-rules/006  phonology-rules/007  phonology-rules/008a \
    phonology-rules/009a phonology-rules/010a phonology-rules/011  \
    phonology-rules/012  phonology-rules/013  phonology-rules/014  \
    phonology-rules/015  phonology-rules/016  phonology-rules/017  \
    phonology-rules/018  phonology-rules/019  phonology-rules/020  \
    phonology-rules/021  phonology-rules/022  phonology-rules/023  \
    phonology-rules/024  phonology-rules/025  phonology-rules/026  \
    phonology-rules/027  phonology-rules/028  phonology-rules/029  \
    phonology-rules/030  phonology-rules/031  phonology-rules/032  \
    phonology-rules/033  phonology-rules/034  phonology-rules/035  \
    phonology-rules/036  phonology-rules/037  phonology-rules/038  \
    phonology-rules/039  phonology-rules/040  phonology-rules/041  \
    phonology-rules/042  phonology-rules/043  phonology-rules/044  \
    phonology-rules/045  phonology-rules/046  phonology-rules/047  \
    phonology-rules/048  phonology-rules/049

RULES_L2_ii := phonology-rules/twolc_header  \
    phonology-rules/000  phonology-rules/001  phonology-rules/002  \
    phonology-rules/003  phonology-rules/004  phonology-rules/005  \
    phonology-rules/006  phonology-rules/007  phonology-rules/008  \
    phonology-rules/009  phonology-rules/010  phonology-rules/011  \
    phonology-rules/012  phonology-rules/013  phonology-rules/014  \
    phonology-rules/015  phonology-rules/016  phonology-rules/017  \
    phonology-rules/018  phonology-rules/019a phonology-rules/020  \
    phonology-rules/021  phonology-rules/022  phonology-rules/023  \
    phonology-rules/024  phonology-rules/025  phonology-rules/026  \
    phonology-rules/027  phonology-rules/028  phonology-rules/029  \
    phonology-rules/030  phonology-rules/031  phonology-rules/032  \
    phonology-rules/033  phonology-rules/034  phonology-rules/035  \
    phonology-rules/036  phonology-rules/037  phonology-rules/038  \
    phonology-rules/039  phonology-rules/040  phonology-rules/041  \
    phonology-rules/042  phonology-rules/043  phonology-rules/044  \
    phonology-rules/045  phonology-rules/046  phonology-rules/047  \
    phonology-rules/048  phonology-rules/049

RULES_L2_Pal := phonology-rules/twolc_header  \
    phonology-rules/000  phonology-rules/001  phonology-rules/002  \
    phonology-rules/003  phonology-rules/004  phonology-rules/005  \
    phonology-rules/006  phonology-rules/007  phonology-rules/008  \
    phonology-rules/009  phonology-rules/010  phonology-rules/011  \
    phonology-rules/012a phonology-rules/013  phonology-rules/014a \
    phonology-rules/015a phonology-rules/016  phonology-rules/017a \
    phonology-rules/018a phonology-rules/019  phonology-rules/020  \
    phonology-rules/021  phonology-rules/022  phonology-rules/023a \
    phonology-rules/024  phonology-rules/025  phonology-rules/026  \
    phonology-rules/027  phonology-rules/028  phonology-rules/029  \
    phonology-rules/030  phonology-rules/031  phonology-rules/032  \
    phonology-rules/033  phonology-rules/034  phonology-rules/035  \
    phonology-rules/036  phonology-rules/037  phonology-rules/038  \
    phonology-rules/039  phonology-rules/040  phonology-rules/041  \
    phonology-rules/042  phonology-rules/043  phonology-rules/044  \
    phonology-rules/045  phonology-rules/046  phonology-rules/047  \
    phonology-rules/048  phonology-rules/049

RULES_L2_SRo := phonology-rules/twolc_header  \
    phonology-rules/000  phonology-rules/001  phonology-rules/002  \
    phonology-rules/003  phonology-rules/004  phonology-rules/005  \
    phonology-rules/006  phonology-rules/007  phonology-rules/008  \
    phonology-rules/009  phonology-rules/010  phonology-rules/011  \
    phonology-rules/012  phonology-rules/013  phonology-rules/014b \
    phonology-rules/015  phonology-rules/016  phonology-rules/017  \
    phonology-rules/018  phonology-rules/019  phonology-rules/020  \
    phonology-rules/021  phonology-rules/022  phonology-rules/023  \
    phonology-rules/024  phonology-rules/025  phonology-rules/026  \
    phonology-rules/027  phonology-rules/028  phonology-rules/029  \
    phonology-rules/030  phonology-rules/031  phonology-rules/032  \
    phonology-rules/033  phonology-rules/034  phonology-rules/035  \
    phonology-rules/036  phonology-rules/037  phonology-rules/038  \
    phonology-rules/039  phonology-rules/040  phonology-rules/041  \
    phonology-rules/042  phonology-rules/043  phonology-rules/044  \
    phonology-rules/045  phonology-rules/046  phonology-rules/047  \
    phonology-rules/048  phonology-rules/049

phonology-err-L2_ii.twolc: $(RULES_L2_ii)
	tail -n +1 $(RULES_L2_ii)  \
		| sed "s/^==>/!! ==> sourced from/g"  \
		> $@

phonology-err-L2_FV.twolc: $(RULES_L2_FV)
	tail -n +1 $(RULES_L2_FV)  \
		| sed "s/^==>/!! ==> sourced from/g"  \
		> $@

phonology-err-L2_NoFV.twolc: $(RULES_L2_NoFV)
	tail -n +1 $(RULES_L2_NoFV)  \
		| sed "s/^==>/!! ==> sourced from/g"  \
		> $@

phonology-err-L2_Pal.twolc: $(RULES_L2_Pal)
	tail -n +1 $(RULES_L2_Pal)  \
		| sed "s/^==>/!! ==> sourced from/g"  \
		> $@

phonology-err-L2_SRo.twolc: $(RULES_L2_SRo)
	tail -n +1 $(RULES_L2_SRo)  \
		| sed "s/^==>/!! ==> sourced from/g"  \
		> $@

phonology-err-L2_%.hfst: phonology-err-L2_%.twolc
	$(AM_V_TWOLC)$(HFST_TWOLC) $(HFST_FORMAT) -i $< -o $@

# L2 Generator/Analyser rules

# 1. Compose lexicon with L2 phonology
generator-raw-gt-desc-err-L2_%.tmp1.hfst: morphology/lexicon.hfst phonology-err-L2_%.hfst
	$(AM_V_HCOMPOSE)hfst-compose -1 morphology/lexicon.hfst -2 phonology-err-L2_$*.hfst | $(HFST_MINIMIZE) > $@

# 2. Subtract standard generator
generator-raw-gt-desc-err-L2_%.tmp2.hfst: generator-raw-gt-desc-err-L2_%.tmp1.hfst generator-raw-gt-desc.hfst
	$(AM_V_GEN)hfst-subtract generator-raw-gt-desc-err-L2_$*.tmp1.hfst \
	    generator-raw-gt-desc.hfst \
	    > $@

# 3. Compose with filters
generator-raw-gt-desc-err-L2_%.tmp.hfst: generator-raw-gt-desc-err-L2_%.tmp2.hfst \
					 filters/reorder-subpos-tags.hfst \
					 filters/reorder-semantic-tags.hfst \
					 filters/remove-mwe-tags.hfst
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex \
	            @\"filters/reorder-subpos-tags.hfst\"   \
	        .o. @\"filters/reorder-semantic-tags.hfst\" \
	        .o. @\"filters/remove-mwe-tags.hfst\"       \
	        .o. @\"$<\" \
	        ;\n\
	     save stack $@\n\
	     quit\n" | $(XFST_TOOL)

# 4. Copy to .hfst
generator-raw-gt-desc-err-L2_%.hfst: generator-raw-gt-desc-err-L2_%.tmp.hfst
	cp -f $< $@

# 5. Copy to analyser raw
analyser-raw-gt-desc-err-L2_%.hfst: generator-raw-gt-desc-err-L2_%.hfst
	cp $< $@

# 6. Create analyser tmp (invert and filter)
analyser-gt-desc-err-L2_%.tmp.hfst: analyser-raw-gt-desc-err-L2_%.hfst \
					 filters/remove-area-tags.hfst \
					 filters/remove-dialect-tags.hfst \
					 filters/remove-number-string-tags.hfst \
					 filters/remove-usage-tags.hfst \
					 filters/remove-semantic-tags.hfst \
					 filters/remove-orig_lang-tags.hfst \
					 filters/remove-orthography-tags.hfst \
					 filters/remove-Orth_IPA-strings.hfst \
					 orthography/downcase-derived_proper-strings.compose.hfst \
					 filters/remove-hyphenation-marks.hfst \
					 filters/remove-infl_deriv-borders.hfst \
					 filters/remove-word-boundary.hfst \
					 orthography/inituppercase.compose.hfst \
					 orthography/spellrelax.compose.hfst
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex \
	            @\"filters/remove-area-tags.hfst\"                \
	        .o. @\"filters/remove-dialect-tags.hfst\"             \
	        .o. @\"filters/remove-number-string-tags.hfst\"       \
	        .o. @\"filters/remove-usage-tags.hfst\"               \
	        .o. @\"filters/remove-semantic-tags.hfst\"            \
	        .o. @\"filters/remove-orig_lang-tags.hfst\"           \
	        .o. @\"filters/remove-orthography-tags.hfst\"         \
	        .o. @\"filters/remove-Orth_IPA-strings.hfst\"         \
	        .o. @\"$<\" \
	        .o. @\"orthography/downcase-derived_proper-strings.compose.hfst\" \
	        .o. @\"filters/remove-hyphenation-marks.hfst\"        \
	        .o. @\"filters/remove-infl_deriv-borders.hfst\"       \
	        .o. @\"filters/remove-word-boundary.hfst\"            \
	        ; \n\
	        define fst \n\
	        set flag-is-epsilon ON\n\
	        read regex fst \
	        .o. @\"orthography/inituppercase.compose.hfst\"       \
	        .o. @\"orthography/spellrelax.compose.hfst\"          \
	        ;\n\
	     save stack $@\n\
	     quit\n" | $(XFST_TOOL)

# 7. Destress optional
analyser-gt-desc-err-L2_%.tmp1.hfst: analyser-gt-desc-err-L2_%.tmp.hfst \
					 orthography/destressOptional.compose.hfst
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex @\"$<\" \
	        .o. @\"orthography/destressOptional.compose.hfst\" \
	        ;\n \
	        invert net\n \
	        save stack $@\n \
	        quit\n" | $(XFST_TOOL)

# 8. Add +Err tag
analyser-gt-desc-err-L2_%.tmp2.hfst: analyser-gt-desc-err-L2_%.tmp1.hfst
	$(AM_V_GEN)echo "[ ? -> ... \"\+Err\/L2_$*\" || _ .#. ]" \
		| hfst-regexp2fst $(HFST_FORMAT) --xerox-composition=ON -S \
		| hfst-compose-intersect \
			-1 $< -2 - \
	                -o $@

# 9. Final L2 analyser
analyser-gt-desc-L2.hfst: analyser-gt-desc.hfst \
			  analyser-gt-desc-err-L2_ii.tmp2.hfst \
			  analyser-gt-desc-err-L2_FV.tmp2.hfst \
			  analyser-gt-desc-err-L2_NoFV.tmp2.hfst \
			  analyser-gt-desc-err-L2_Pal.tmp2.hfst \
			  analyser-gt-desc-err-L2_SRo.tmp2.hfst
	cp analyser-gt-desc.hfst $@
	for tag in ii FV NoFV Pal SRo ; \
	do \
		hfst-disjunct -1 $@ \
			      -2 analyser-gt-desc-err-L2_$${tag}.tmp2.hfst \
			      > $${tag}.tmp.hfst ; \
		mv $${tag}.tmp.hfst $@ ; \
	done
	$(top_srcdir)/src/add_L2_orth_err.sh $@ prijti
	$(top_srcdir)/src/add_L2_orth_err.sh $@ e2je je2e
	$(top_srcdir)/src/add_L2_orth_err.sh $@ H2S
	$(top_srcdir)/src/add_L2_orth_err.sh $@ i2j i2y Ikn j2i y2i revIkn SRc SRy
	$(top_srcdir)/src/add_L2_orth_err.sh $@ NoGem
	$(top_srcdir)/src/add_L2_orth_err.sh $@ NoSS
	$(top_srcdir)/src/add_L2_orth_err.sh $@ o2a a2o
	$(top_srcdir)/src/add_L2_orth_err.sh $@ sh2shch shch2sh
	$(top_srcdir)/src/add_L2_orth_err.sh $@ ski

endif # WANT_L2

if WANT_CUSTOM_FSTS
CUSTOM_FSTS+=
endif # WANT_CUSTOM_FSTS

endif # CAN_HFST

#### FOMA transducers
if CAN_FOMA
GT_ANALYSERS+=
GT_GENERATORS+=

if WANT_CUSTOM_FSTS
CUSTOM_FSTS+=
endif # WANT_CUSTOM_FSTS

endif # CAN_FOMA

#################################################
#### Add language-specific build rules here: ####

# We need to add processing of language-specific tags in the analysers:
define giella_fsts
# We also need language-specific processing in the accented analysers:
analyser-gt-%.accented.$(1): analyser-gt-%.accented.tmp.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "load stack $$<\n\
		 $$(INVERT_HFST)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)

# We also need language-specific processing in the accented generators:
generator-gt-%.accented.$(1): generator-gt-%.accented.tmp.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "load stack $$<\n\
		 $$(INVERT_XFST)$$(INVERT_FOMA)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)

analyser-gt%.$(1): analyser-gt%.tmp.$(1) \
					 orthography/destressOptional.compose.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"$$<\"                                      \
			.o. @\"orthography/destressOptional.compose.$(1)\" \
			;\n\
		 $$(INVERT_HFST)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)

analyser-disamb-gt%.$(1): analyser-disamb-gt%.tmp.$(1) \
					 orthography/destressOptional.compose.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"$$<\"                                      \
			.o. @\"orthography/destressOptional.compose.$(1)\" \
			;\n\
		 $$(INVERT_HFST)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)

# The hfst specific tokeniser disamb fst also needs to be destressed:
analyser-pmatchdisamb-gt%.$(1): analyser-pmatchdisamb-gt%.tmp.$(1) \
					 orthography/destressOptional.compose.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"$$<\"                                      \
			.o. @\"orthography/destressOptional.compose.$(1)\" \
			;\n\
		 $$(INVERT_HFST)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)

analyser-gramcheck-gt%.$(1): analyser-gramcheck-gt%.tmp.$(1) \
					 orthography/destressOptional.compose.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"$$<\"                                      \
			.o. @\"orthography/destressOptional.compose.$(1)\" \
			;\n\
		 $$(INVERT_HFST)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)

# We need to add processing of language-specific tags in the generators:
generator-gt%.$(1): generator-gt%.tmp.$(1) \
					 orthography/destress.compose.$(1) \
					 filters/make-optional-cyrillic-jo.$(1) \
					 filters/make-ambiguous-AnIn.$(1) \
					 filters/make-ambiguous-MFN.$(1)
	$$(AM_V_XFST_TOOL)$$(PRINTF) "read regex \
				@\"filters/make-optional-cyrillic-jo.$(1)\" \
		        .o. @\"filters/make-ambiguous-AnIn.$(1)\" \
		        .o. @\"filters/make-ambiguous-MFN.$(1)\" \
			.o. @\"$$<\"                                    \
			.o. @\"orthography/destress.compose.$(1)\"      \
			;\n\
		 $$(INVERT_XFST)$$(INVERT_FOMA)\
		 save stack $$@\n\
		 quit\n" | $$(XFST_TOOL)

endef
$(foreach fst,hfst xfst foma,$(eval $(call giella_fsts,$(fst))))

##################################################################
#### END: Add local processing instructions ABOVE this line ######
##################################################################

include $(top_srcdir)/../giella-core/am-shared/src-fst-dir-include.am
include $(top_srcdir)/../giella-core/am-shared/devtest-include.am

if CAN_HFST
if WANT_L2
CLEANFILES += phonology-err-L2_*.twolc phonology-err-L2_*.hfst \
              generator-raw-gt-desc-err-L2_*.hfst \
              analyser-raw-gt-desc-err-L2_*.hfst \
              analyser-gt-desc-err-L2_*.hfst \
              analyser-gt-desc-L2.hfst \
              *.tmp.hfst *.tmp1.hfst *.tmp2.hfst
endif
endif
