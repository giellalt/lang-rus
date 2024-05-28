## Process this file with automake to produce Makefile.in
## Copyright: Sámediggi/Divvun/UiT
## Licence: GPL v3+

SUBDIRS = fst cg3

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

include $(top_srcdir)/../giella-core/am-shared/src-dir-include.am
include $(top_srcdir)/../giella-core/am-shared/devtest-include.am
