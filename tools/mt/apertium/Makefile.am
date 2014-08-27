## Process this file with automake to produce Makefile.in
## Copyright: Sámediggi/Divvun/UiT
## Licence: GPL v3+

# Process subdirs first:
SUBDIRS = filters tagsets .

##################################################################
#### BEGIN: Add local processing instructions BELOW this line ####
##################################################################

analyser-mt-gt-desc.hfst: analyser-mt-gt-desc.tmp.hfst \
				 $(top_builddir)/src/orthography/destress.hfst
	$(AM_V_RGX2FST)$(PRINTF) "\
				@\"$<\" \
			.o. @\"$(top_builddir)/src/orthography/destress.hfst\" \
			;" \
		| $(HFST_REGEXP2FST) $(HFST_FLAGS) -S --harmonize-flags \
		| $(HFST_INVERT) \
		| $(HFST_FST2FST) $(HFST_FLAGS) -f olw \
		> $@

generator-mt-gt-norm.hfst: generator-mt-gt-norm.tmp.hfst \
				  $(top_builddir)/src/orthography/destress.hfst
	$(AM_V_RGX2FST)$(PRINTF) "\
				@\"$<\" \
			.o. @\"$(top_builddir)/src/orthography/destress.hfst\" \
			;" \
		| $(HFST_REGEXP2FST) $(HFST_FLAGS) -S --harmonize-flags \
		| $(HFST_FST2FST) $(HFST_FLAGS) -f olw \
		> $@

##################################################################
#### END: Add local processing instructions ABOVE this line ######
##################################################################

####### Other targets: ###########

# cleaning
clean-local:
	-rm -f *.hfst *.gz *.cg3 *.bin

include $(top_srcdir)/am-shared/tools-mt-apertium-dir-include.am
