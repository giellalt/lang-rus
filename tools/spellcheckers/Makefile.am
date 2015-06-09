## Process this file with automake to produce Makefile.in
## Copyright: Sámediggi/Divvun/UiT
## Licence: GPL v3+

# The current dir must be built first.
SUBDIRS = . fstbased listbased

#########################################
# BEGIN: Local processing
#
# Target template:
#
# generator-speller-gt-norm.hfst: generator-speller-gt-norm.tmp.hfst
#	build rules
#
# analyser-speller-gt-norm.xfst: analyser-speller-gt-norm.tmp.xfst
#	build rules

# We need to remove accents from the speller fst's:
generator-speller-gt-norm.hfst: generator-speller-gt-norm.tmp.hfst \
				  $(top_builddir)/src/orthography/destress.lookup.hfst
	$(AM_V_RGX2FST)$(PRINTF) "\
				@\"$<\" \
			.o. @\"$(top_builddir)/src/orthography/destress.lookup.hfst\" \
			;" \
		| $(HFST_REGEXP2FST) $(HFST_FLAGS) -S --xerox-composition=ON \
		> $@

analyser-speller-gt-norm.xfst: analyser-speller-gt-norm.tmp.xfst \
				  $(top_builddir)/src/orthography/destress.lookup.xfst
	$(AM_V_XFST)$(PRINTF) "read regex \
				@\"$<\" \
			.o. @\"$(top_builddir)/src/orthography/destress.lookup.xfst\" \
			;\n\
		 save stack $@\n\
		 quit\n" | $(XFST) $(VERBOSITY)

# END: Local processing
#########################################

include $(top_srcdir)/am-shared/tools-spellcheckers-dir-include.am
