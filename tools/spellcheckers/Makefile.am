## Process this file with automake to produce Makefile.in
## Copyright: Sámediggi/Divvun/UiT
## Licence: GPL v3+

# The current dir must be built first.
SUBDIRS = filters . fstbased

#########################################
# BEGIN: Local processing
#
# Target template:
#
# analyser-speller-gt-norm.%: analyser-speller-gt-norm.tmp.%
#	build rules

# We need to remove accents from the speller fst's:
generator-speller-gt-norm.%: analyser-speller-gt-norm.tmp.% \
				  $(top_builddir)/src/orthography/destressOptional.lookup.% \
				  filters/expand-multichars.%
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex                                    \
				@\"$<\" \
			.o. @\"$(top_builddir)/src/orthography/destressOptional.lookup.$*\" \
			.o. @\"filters/expand-multichars.$*\" \
		; \n\
		save stack $@\n\
		quit\n" | $(XFST_TOOL)

analyser-speller-gt-norm.%: analyser-speller-gt-norm.tmp.% \
				$(top_builddir)/src/orthography/destressOptional.lookup.% \
				$(top_builddir)/src/filters/remove-hyphenation-marks.% \
				$(top_builddir)/src/filters/remove-infl_deriv-borders.% \
				filters/expand-multichars.%
	$(AM_V_XFST_TOOL)$(PRINTF) "read regex                                    \
				@\"$<\" \
		.o. @\"$(top_builddir)/src/orthography/destressOptional.lookup.$*\" \
		.o. @\"filters/expand-multichars.$*\" \
		.o. @\"$(top_builddir)/src/filters/remove-hyphenation-marks.$*\"    \
		.o. @\"$(top_builddir)/src/filters/remove-infl_deriv-borders.$*\"   \
		; \n\
		$(INVERT_HFST)\
		save stack $@\n\
		quit\n" | $(XFST_TOOL)

# END: Local processing
#########################################

include $(top_srcdir)/am-shared/tools-spellcheckers-dir-include.am
