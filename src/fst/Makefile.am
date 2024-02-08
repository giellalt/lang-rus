## Process this file with automake to produce Makefile.in
## Copyright: Sámediggi/Divvun/UiT
## Licence: GPL v3+

# always build . last here, and tagsets have to be built after morphology
SUBDIRS = morphology filters phonetics syllabification orthography transcriptions tagsets .

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

#### Xerox transducers:
if CAN_XFST
GT_ANALYSERS+=
GT_GENERATORS+=

if WANT_CUSTOM_FSTS
CUSTOM_FSTS+=
endif # WANT_CUSTOM_FSTS

endif # CAN_XFST

#### HFST transducers
if CAN_HFST
GT_ANALYSERS+=
GT_GENERATORS+=

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
