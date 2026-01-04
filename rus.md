# Russian language model documentation

All doc-comment documentation in one large file.

---

## src-cg3-functions.cg3.md 



* Sets for POS sub-categories

* Sets for Semantic tags

* Sets for Morphosyntactic properties

* Sets for verbs

- V is all readings with a V tag in them, REAL-V should
be the ones without an N tag following the V.  
The REAL-V set thus awaits a fix to the preprocess V ... N bug.

* The set COPULAS is for predicative constructions

* NP sets defined according to their morphosyntactic features

* The PRE-NP-HEAD family of sets

These sets model noun phrases (NPs). The idea is to first define whatever can
occur in front of the head of the NP, and thereafter negate that with the
expression **WORD - premodifiers**.

The set **NOT-NPMOD** is used to find barriers between NPs.
Typical usage: ... (*1 N BARRIER NPT-NPMOD) ...
meaning: Scan to the first noun, ignoring anything that can be
part of the noun phrase of that noun (i.e., "scan to the next NP head")

* Miscellaneous sets

* Border sets and their complements

* Syntactic sets

These were the set types.

### HABITIVE MAPPING

* **hab1** 

* **hab2** 

* **hab3** (<hab> @ADVL>) for hab-actor and hab-case; if leat to the right, and Nom to the right of leat. Lots of restrictions.

* **habNomLeft** 

* **hab4** 	

* **hab6** 

* **hab7** 

* **hab8** This is not HAB
* **hab5**  This is not HAB

* **habDain** (<hab> @ADVL>) for (Pron Dem Pl Loc) if leat followed by Nom to the right

* **habGen** (<hab> @<ADVL) hab for Gen; if Gen is located in the end of the sentence and Nom is sentence initial

* **spred<obj** (@SPRED<OBJ) for Acc; the object of an SPRPED. Not to be mistaken with OPRED. If SPRED is to the left, and copulas is to the left of it. Nom or Hab are found sentence initially.

* **Hab<spred** (@<SPRED) for Nom; if copulas, goallut or jápmit is FMAINV and habitive or human Loc is found to the left. OR: if Ill or @Pron< followed by HAB are found to the left.

* **Hab>Advlcase<spred** (<ext> @<SUBJ) for Nom; it allows adverbials with Ill/Loc/Com/Ess to be found inbetween HAB and <ext>.

* **Nom>Advlcase<spred** (<ext> @<SUBJ) for Nom; it allows adverbials with Ill/Loc/Com/Ess to be found inbetween Nom and <ext> @<SUBJ.

* **<spred** (<ext> @<SUBJ) for Nom; if copulas to the left, and some kind of adverb, N Loc, time related word or Po to the left of it. OR: if Ill or @Pron< to the left, followed by copulas and the before mentioned to the left of copulas. 

* **<spred** (<ext> @<SUBJ) for Nom, but not for Pers. To the left boahtit or heaŋgát as MAINV, and futher to the left is some kind of place related word, or time related word

* **<spredQst1** (<ext> @<SUBJ) for Nom in a typically question sentence; if A) Hab, some kind of place word, Po or Nom to the left, and Qst followed by copulas to the left. B) same as a, only the Qst-pcle is attached to copulas. C) Qst to the left, with copulas to its left, but not if two Nom:s are found somewhere to the right. D) copulas to the left, and BOS to the left. E) Loc or Ill to the left, and Loc or Hab to the left of this, Qst and copulas to the left. F) Num @>N to the left, Hab, some kind of place word, Po or Nom to the left, and Qst followed by copulas to the left. NOTE) for all these rules; human, Loc or Sem/Plc not allowed to the right.

* **<spredQst2** (@<SPRED) for Nom; in a typically question sentence; differs from <spredQst1 by not beeing as restricted to the right. Though you are not allowed to be Pers or human.

* **Nom<spredQst** (@<SPRED) for Nom; in a typically question sentence. Differs from <spredQst2 by letting Nom be found between SPRED and copulas

* **<spred** (@<SPRED) for A Nom or N Nom if; the subject Nom is on the same side of copulas as you: on the right side of copulas

* **<spredVeara** (@<SPRED) for veara + Nom; if genitive immediately to the right, and intransitive mainverb to the right of genitive

* **leftCop<spred** (@<SPRED) for Nom; if copulas is the main verb to the left, and there is no Ess found to the left of cop (note that Loc is allowed between target and cop). OR: if you are Coll or Sem/Group with copulas to your left. 

* **<spredLocEXPERIMENT** (@<SPRED) for material Loc; if you are to the right of copulas, and the Nom to the left of copulas is not a hab-actor

* **NumTime** (@<SPRED) for A Nom

* **<spredSg** (@<SPRED) for Sg Nom	

* **<spredPg** (@<SPRED) for Pl Nom	

* **<spred** (@<SPRED) for Nom; if copulas to the left, and Nom or sentence boundary to the left of copulas. First one to the right is EOS.

* **<spred** (@<SPRED) for N Ess

* **spredEss>** (@SPRED>) for N Ess; if copulas to the right of you, and if an NP with nom-case first one to your left.

* **HABSpredSg>** (@SPRED>) for Nom; if habitive first one to the left, followed by copulas.

* **GalleSpred>** (@SPRED>) for Num Nom; if sentence initial

* **spredSgMII>** (@SPRED>)

* **r492>** (@SPRED>) for Interr Gen; consisting only of negations. You are not allowed to be MII. You are not allowed to have an adjective or noun to yor right. You are not allowed to have a verb to your right; the exception beeing an aux.

* **AdjSpredSg>** (@SPRED>) for A Sg Nom; if copulas to the right, but not if A or @<SPRED are found to the right of copulas

* **SpredSg>Hab** (@SPRED>) for Nom; if you are sentence initial, copulas is located to the right, and there is a habitive to the right of copulas

* **Spred>SubjInf** (@SPRED>) for Nom; if copulas to the right, and the subject of copulas is an Inf to the right

* **spredCoord** (@<SPRED) coordination for Nom; only if there already is a SPRED to the left of CNP. Not if there is some kind of comparison involved.

* **subj>Sgnr1** (@SUBJ>) for Nom Sg, including Indef Nom if; VFIN + Sg3 or Pl3 to the right (VFIN not allowed to the left) 

* **subj>Du** (@SUBJ>) for dual nominatives, including Coll Nom. VFIN + Du3 to the right. 
* **subj>Pl** (@SUBJ>) for plural nominatives, including Coll and Sem/Group. VFIN + Pl3 to the right.

* **subj>Pl** (@SUBJ>) for plural nominatives

* **subj>Sgnr2** (@SUBJ>) for Nom Sg; if VFIN + Sg3 to the right.

* **<subjSg** (@<SUBJ) for Nom Sg; if VFIN Sg3 or Du2 to the left (no HAB allowed to the left).

* **f<advl** (@-F<ADVL) for infinite adverbials

* **f<advl** (@-F<ADVL) for infinite adverbials

* **s-boundary=advl>** (@ADVL>) for ADVL that resemble s-booundaries. Mainverb to the right.

* **-fobj>** (@-FOBJ>) for Acc 

* **-fobj>** (@-FOBJ>) for Acc

* **advl>mainV** (@ADVL>) if; finite mainverb not found to the left, but the finite mainverb is found to the right.

* **<advl** (@<ADVL) if; finite mainverb found to the left. Not if a comma is found immediately to the left and a finite mainverb is located somewhere to the right of this comma.

* **<advlPoPr** (@<ADVL) if mainverb to the left.
* **advlPoPr>** (@<ADVL) if mainverb to the right.

* **advlEss>** (@<ADVL) for weather and time Ess, if FMAINV to the left.

* **advl>inbetween** (@ADVL>) for Adv; if inbetween two sentenceboundaries where no mainverb is present.

* **comma<advlEOS** (@<ADVL) if; comma found to the left and the finite mainverb to the left of comma. To the right is the end of the sentence.

* **advlBOS>** (@ADVL>) if; you are N Ill and found sentnece initially. First one to your right is a clause.

* **<advlPoEOS** (@<ADVL) for Po; if you are found at the very end of a sentence. A mainverb is needed to the right though.

* **cleanupILL<advl** (@<ADVL) for N Ill if; there are no boundarysymbols to your left, if you arent already @N< OR @APP-N<, and no mainverb is to yor left.

* **<opredAAcc** (@<OPRED) for A Acc; if an other accusative to the left, and a transtive verb to the left of it. OR: if a transitive verb to the left, and an accusative to the left of it.

#### sma object

* **<advlEss** (@<ADVL) for ESS-ADVL if; FMAINV to the left
* **<spredEss** (@<SPRED) for N Ess if; FMAINV to the left is intransitive or bargat

### SUBJ MAPPING - leftovers

### OBJ MAPPING - leftovers

### HNOUN MAPPING

* * *

<small>This (part of) documentation was generated from [src/cg3/functions.cg3](https://github.com/giellalt/lang-rus/blob/main/src/cg3/functions.cg3)</small>

---

## src-fst-morphology-affixes-symbols.lexc.md 


## Symbol affixes

* * *

<small>This (part of) documentation was generated from [src/fst/morphology/affixes/symbols.lexc](https://github.com/giellalt/lang-rus/blob/main/src/fst/morphology/affixes/symbols.lexc)</small>

---

## src-fst-morphology-affixes-verbs.lexc.md 

To do / Problems
================
Tagging transitive and intransitive verbs.
- Difference between св_нп_1a and св_1a?
- нп = intransitive in ALL meanings.(i.e. lack of нп does not always signify transitivity, rather only the possibility of it). Which lemmas are ONLY transitive?
Manually check for consistency on issues such as:
- passive forms for transitive imperfectives
- present passives
- past passives
- impersonal tags

Active Voice
Passive Voice

* * *

<small>This (part of) documentation was generated from [src/fst/morphology/affixes/verbs.lexc](https://github.com/giellalt/lang-rus/blob/main/src/fst/morphology/affixes/verbs.lexc)</small>

---

## src-fst-morphology-phonology.twolc.md 

==> sourced from phonology-rules/twolc_header <==
This file is produced automatically from the script make_twolc.sh
Instead, edit the component file(s) in the 
phonology-rules/ directory and then run `sh make_twolc.sh`.

==> sourced from phonology-rules/000 <==
============================================================================

01_base_rules.twolc
02_stem_palatalization.twolc
03_spellingrule-husher.twolc
04_spellingrule-velar.twolc
05_spellingrule-c.twolc
06_fleeting-vowel-deletion.twolc
07_fleeting-vowel-insertion.twolc
08_nouns_ie-ii.twolc
09_stress.twolc
Genitive plural of nouns
Comparative adjectives
Masculine short-form adjectives
Stem alternations
Vowels in nonpast endings
Imperatives
Verbal prefix fleeting vowels and voicing assimilation

* *рабо́та>у*
* *рабо́т0>у*
* ★*рабо́та>у* (is not standard language)
* ★*рабо́та>0* (is not standard language)

==> sourced from phonology-rules/001 <==
============================================================================
* *сло́во>а́*
* *слов0>а́*
* *у́мн>а́*
* *умн>а́*
* *сёст^Fёра́>ы*
* *сёст00р0>ы*
* *се́м^Fе́йя́>у́*
* *сем00ь0>ю́*
* *прочи́та́<ем*
* *прочита́<ем*

==> sourced from phonology-rules/002 <==
============================================================================
* *Тама́ра>а*
* *Тама́р0>а*
* *мо́ре>о*
* *мо́р0>е*
* *Петр>овна>а*
* *Петр>овн0>а*
* *о́к^Fоно>о́*
* *ок00н0>о́*
* *зе́м^Fе́ля́>е́*
* *зем00л0>е́*
* *б^Fе́й<у́*
* *б00ь<ю́*
* *б^Fе́й<^Sте*
* *б0е́й<0те*
* *ж^Fёг<ла́*
* *ж00г<ла́*

==> sourced from phonology-rules/003 <==
============================================================================
* *ли́х>е́е*
* *ли́ш>е0*

==> sourced from phonology-rules/004 <==
============================================================================
* *люб^Fо́вь>ы́*
* *люб00в0>и́*
* *люб^Fо́вь>ью*
* *люб0о́в0>ью*
* *кни́га>ов*
* *кни́г0>00*
* *чудо́вище>ов*
* *чудо́вищ0>00*
* *пти́ца>ов*
* *пти́ц0>00*
* *пи́ла́>о́в*
* *пи́л0>00*
* *ба́ш^Fеня>ов*
* *ба́ш0ен0>00*
* *се́м^Fе́йя́>ов*
* *сем0е́й0>00*
* *ва́йя>ов*
* *ва́й0>00*

==> sourced from phonology-rules/005 <==
============================================================================
* *с^Oго́н^M<ю́*
* *с0гон0<ю́*

==> sourced from phonology-rules/006 <==
============================================================================

==> sourced from phonology-rules/007 <==
============================================================================
* *раз^oш^Fе́й<у́*
* *разош00ь<ю́*
* *раз^oши́л*
* *рас0ши́л*

==> sourced from phonology-rules/008 <==
============================================================================
* *ко́сть>ь*
* *ко́ст0>ь*
* *ми́лость>ы*
* *ми́лост0>и*
* *во́сь^Fемь>ь*
* *во́с00ем0>ь*

==> sourced from phonology-rules/009 <==
============================================================================
* *музе́й>а*
* *музе́0>я*
* *Гава́йй>ы*
* *Гава́й0>и*
* *копе́й^Fека>ов*
* *копе́00ек0>00*
* *ли́х>е́й*
* *ли́ш>е0*

==> sourced from phonology-rules/010 <==
============================================================================
* *мурав^Fе́й>а́*
* *мурав00ь>я́*
* *бел^Fе́йё>о́*
* *бел00ь0>ё*
* *б^Fе́й<у́*
* *б00ь<ю́*
* *вы́бурав<й*
* *вы́бурав<ь*

==> sourced from phonology-rules/011 <==
============================================================================
* *но́в>^Z*
* *но́в>0*
* *столе́т^Fень>^Z*
* *столе́т0ен0>0*

==> sourced from phonology-rules/012 <==
============================================================================
* *си́нь>^Z*
* *си́н0>ь*

==> sourced from phonology-rules/013 <==
============================================================================
* *длинноше́й>^Z*
* *длинноше́0>й*

==> sourced from phonology-rules/014 <==
============================================================================
* *хоро́ш>ому*
* *хоро́ш>ему*
* *па́ль^Fец>ом*
* *па́ль00ц>ем*
* *музе́й>ом*
* *музе́0>ем*
* *си́нь>ой*
* *си́н0>ей*
* *сча́ст^Fий>ом*
* *сча́ст00ь>ем*
* *ва́йя>ой*
* *ва́й0>ей*
* *Гава́йй>ов*
* *Гава́й0>ев*

==> sourced from phonology-rules/015 <==
============================================================================
* *кни́га>ы*
* *кни́г0>и*
* *хоро́ш>ый*
* *хоро́ш>ий*
* *музе́й>ы*
* *музе́0>и*

==> sourced from phonology-rules/016 <==
============================================================================
* *слы́ш<ю*
* *слы́ш<у*
* *и́ск^M<я́*
* *и0щ0<а́*

==> sourced from phonology-rules/017 <==
============================================================================

==> sourced from phonology-rules/018 <==
============================================================================

==> sourced from phonology-rules/019 <==
============================================================================

==> sourced from phonology-rules/020 <==
============================================================================

==> sourced from phonology-rules/021 <==
============================================================================

==> sourced from phonology-rules/022 <==
============================================================================

==> sourced from phonology-rules/023 <==
============================================================================

==> sourced from phonology-rules/024 <==
============================================================================

==> sourced from phonology-rules/025 <==
============================================================================

==> sourced from phonology-rules/026 <==
============================================================================

==> sourced from phonology-rules/027 <==
============================================================================

==> sourced from phonology-rules/028 <==
============================================================================

==> sourced from phonology-rules/029 <==
============================================================================

==> sourced from phonology-rules/030 <==
============================================================================

==> sourced from phonology-rules/031 <==
============================================================================

==> sourced from phonology-rules/032 <==
============================================================================

==> sourced from phonology-rules/033 <==
============================================================================

==> sourced from phonology-rules/034 <==
============================================================================

==> sourced from phonology-rules/035 <==
============================================================================

==> sourced from phonology-rules/036 <==
============================================================================

==> sourced from phonology-rules/037 <==
============================================================================

==> sourced from phonology-rules/038 <==
============================================================================

==> sourced from phonology-rules/039 <==
============================================================================

==> sourced from phonology-rules/040 <==
============================================================================

==> sourced from phonology-rules/041 <==
============================================================================

==> sourced from phonology-rules/042 <==
============================================================================

==> sourced from phonology-rules/043 <==
============================================================================

==> sourced from phonology-rules/044 <==
============================================================================

==> sourced from phonology-rules/045 <==
============================================================================

==> sourced from phonology-rules/046 <==
============================================================================

==> sourced from phonology-rules/047 <==
============================================================================

==> sourced from phonology-rules/048 <==
============================================================================

==> sourced from phonology-rules/049 <==
============================================================================

* * *

<small>This (part of) documentation was generated from [src/fst/morphology/phonology.twolc](https://github.com/giellalt/lang-rus/blob/main/src/fst/morphology/phonology.twolc)</small>

---

## src-fst-morphology-root.lexc.md 



## Russian tags

### Stressed vowels

* а́ е́ ё́ и́ о́ у́ ы́ э́ ю́ я́      Primary stress (lower)
* а̀ ѐ ё̀ ѝ о̀ у̀ ы̀ э̀ ю̀ я̀      Secondary stress (lower)

* А́ Е́ Ё́ И́ О́ У́ Ы́ Э́ Ю́ Я́     Primary stress (upper)
* А̀ Ѐ Ё̀ Ѝ О̀ У̀ Ы̀ Э̀ Ю̀ Я̀     Secondary stress (upper)

### Symbols that need to be escaped on the lower side (towards twolc): (copied from sme)

### Markers

* ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁰  = Used to enumerate homonymous lemmas
* %>    = End-of-stem marker (nominals)
* %<    = End-of-stem marker (verbs)
* %^F   = Fleeting vowel marker
* %^o %^O  = Verbal prefix fleeting vowel
* %^G   = Irregular GenPl marker (to keep ов/ев on n stems, e.g. ов%^G
* %^Z   = Zero ending (resolves to 0/й/ь)
* %^M   = Verb stem mutation
* %^D   = archiphoneme for д~жд alternation in past passive participles
* %^T   = archiphoneme for т~щ alternation in verbs
* %^d   = archiphoneme for verb stems with -дший past active participles (-сти 7 (-д-) )
* %^t   = archiphoneme for verb stems with -тший past active participles (-сти 7 (-т-) )
* %^R   = archiphoneme for бороть and пороть
* %^U   = Imperative ending (unstressed)
* %^S  = Imperative ending (stressed)
* %^P  = Attenuative comparative prefix: по~
* %^A  = Attenuative comparative prefix: по~
* %^Y  = Verbal prefix вы́-

### POS
* +A       = Adjective
* +Abbr    = Abbreviation
* +Adv     = Adverb
* +CC      = Coordinating conjunction
* +CS      = Subordinating conjunction
* +Det     = Determiner
* +Interj  = Interjection
* +N       = Noun
* +Num     = Numeral
* +Paren   = Parenthetical вводное слово
* +Pcle    = Particle
* +Po      = Postposition (ради is the only postposition)
* +Pr      = Preposition
* +Pron    = Pronoun
* +V       = Verb

### Sub-POS
* +All     = All: весь
* +Coll    = Collective numerals
* +Def     = Definite
* +Dem     = Demonstrative
* +Indef   = Indefinite: кто-то, кто-нибудь, кто-либо, кое-кто, etc.
* +Interr  = Interrogative: кто, что, какой, ли, etc.
* +Neg     = Negative: никто, некого, etc.
* +Pers    = Personal
* +Pos     = Possessive, e.g. его, наш
* +Prcnt   = Percent
* +Prop    = Proper
* +Recip   = Reciprocal: друг друга
* +Refl    = Pronoun себя, possessive свой
* +Rel     = Relativizer, e.g. который, где, как, куда, сколько, etc.
* +Symbol = independent symbols in the text stream, like £, €, ©

### Verbal MSP
* +Impf +Perf        = Imperfective, perfective
* +IV +TV            = Intransitive, transitive (Zaliznjak does not mark trans-only, so transitive verbs all have both TV and IV)
* +Inf +Imp          = Imperatives: 2nd person = читай, 1st person = прочитаем
* +Pst +Prs +Fut     = Past, present, future
* +Sg1 +Sg2 +Sg3     = person sg
* +Pl1 +Pl2 +Pl3     = person pl
* +PrsAct +PrsPss    = Participles (+PrsAct+Adv and +PstAct+Adv are used for the verbal adverbs)
* +PstAct +PstPss    = Participles
* +Pass              = Passive
* +Imprs             = Impersonal (cannot have explicit subject)
* +Lxc             = Lexicalized (for participial forms)

* +Der             = Derived (for participial forms)
* +Der/PrsAct             = Derived (for participial forms)
* +Der/PrsPss             = Derived (for participial forms)
* +Der/PstAct             = Derived (for participial forms)
* +Der/PstPss             = Derived (for participial forms)

### Nominal MSP
* +Msc +Fem +Neu +MFN   = grammatical gender,  +MFN = gender unspecifiable (pl tantum)
* +Inan +Anim +AnIn     = animacy (+AnIn = ambivalent animacy for non-accusative modifiers)
* +Sem/Sur +Sem/Pat     = Surname (фамилия), Patronymic
* +Sem/Ant +Sem/Alt     = Anthroponym/Given name, Other
* +Sg +Pl               = number
* +Nom +Acc +Gen       
* +Loc +Dat +Ins       
* +Loc2 +Gen2 +Voc     
* +Count                = Count (for человек/людей or лет/годов, etc. also шага́/шара́/часа́/etc.)
* +Ord      = Ordinal
* +Cmpar    = Comparative
* +Sint     = Synthetic comparative is possible, e.g. старее
* +Pred     = "Predicate", also used for short-form adjectives
* +Cmpnd    = "Compound", used for compounding adjectives, such as русско-английский
* +Att      = Attenuative comparatives like получше, поновее, etc.

### Punctuation
* +PUNCT    = Punctuation
* +CLB    = Clause boundary  ! TODO SENT vs CLB which is which?
* +SENT    = Clause boundary
* +COMMA   = Comma
* +DASH    = Dash
* +LQUOT    = Left quotation
* +RQUOT    = Right quotation
* +QUOT    = "Ambidextrous" quotation
* +LPAR     = Left parenthesis/bracket
* +RPAR     = Right parenthesis/bracket
* +LEFT     = Left parenthesis/bracket/quote/etc.
* +RIGHT +MIDDLE  = Right parenthesis/bracket/quote/etc.

### Other tags
* +Prb      = +Prb(lematic): затруднительно - предположительно - нет
* +Fac      = Facultative
* +PObj     = Object of preposition (prothetic н: него нее них)
* +Epenth   = epenthesis on prepositions (о~об~обо or в~во)
* +Leng     = Lengthened доброй~доброю (marks less-canonical wordform that has more syllables)
* +Elid     = Elided (Иванович~Иваныч, новее~новей, чтобы~чтоб, или~иль, коли~коль)
* +Use/NG   = Do not generate (used for apertium, etc.)
* +Use/Obs  = Obsolete
* +Use/Ant  = Antiquated "устаревшее"
* +Err/Orth  = Substandard
* +Err/L2_a2o      = L2 error: Misspelling (о should be а)
* +Err/L2_e2je     = L2 error: Misspelling (е should be э)
* +Err/L2_FV       = L2 error: Presence of fleeting vowel where it should be deleted, e.g. отеца (compare отца). +Err/L2_FV only occurs in lexemes that have a fleeting vowel in at least one form.
* +Err/L2_H2S      = L2 error: Misspelling (ь should be ъ)
* +Err/L2_i2j      = L2 error: Misspelling (й should be и)
* +Err/L2_i2y      = L2 error: Misspelling (ы should be и)
* +Err/L2_ii       = L2 error: Failure to change ending ие to ии in +Sg+Loc or +Sg+Dat, e.g. к Марие, о кафетерие, о знание. +Err/L2_ii is only possible on nouns with a stem in и
* +Err/L2_Ikn      = L2 error: Ikanje (и should be е or я)
* +Err/L2_j2i      = L2 error: Misspelling (и should be й)
* +Err/L2_je2e     = L2 error: Misspelling (э should be е)
* +Err/L2_NoFV     = L2 error: Lack of fleeting vowel where it should be inserted, e.g. окн (compare окон). +Err/L2_NoFV only occurs in lexemes that have a fleeting vowel in at least one form.
* +Err/L2_NoGem    = L2 error: Geminate letter is missing
* +Err/L2_NoSS     = L2 error: Misspelling (ь is missing)
* +Err/L2_o2a      = L2 error: Akanje (а should be о)
* +Err/L2_Pal      = L2 error: Palatalization: failure to place soft-indicating symbol after soft stem, e.g. земла (compare земля). +Err/L2_Pal only occurs on 1) nouns and modifiers that have a soft stem, or 2) verbs in евать, e.g. малует (compare малюет)
* +Err/L2_prijti   = L2 error: Misspelling the stem of прийти, especially the й
* +Err/L2_revIkn   = L2 error: Reversed ikanje, i.e. spelling и as е/я/а to reflect supposed vowel reduction
* +Err/L2_sh2shch  = L2 error: Misspelling (щ should be ш)
* +Err/L2_shch2sh  = L2 error: Misspelling (ш should be щ)
* +Err/L2_ski      = L2 error: по-~ский instead of по-~ски
* +Err/L2_SRc      = L2 error: L2 error: replace и with ы or vice versa after ц
* +Err/L2_SRo      = L2 error: Failure to change о to е after hushers and ц, e.g. Сашой (compare Сашей). +Err/L2+SRo only occurs in 1) nouns and modifiers with stems in hushers or ц, or 2) verbs in евать, e.g. танцовать (compare танцевать)
* +Err/L2_SRy      = L2 error: Failure to change ы to и after hushers and velars, e.g. книгы (compare книги). +Err/L2+SRo only occurs in nouns and modifiers with stems in hushers or velars
* +Err/L2_y2i      = L2 error: Misspelling (и should be ы)

## Key lexicon

* LEXICON Root    

* Abbreviation ;	
* :%^P%^A Adjective ;	    
* Adverb ;	    
* Comparative ;   
* Conjunction ;   
* Interjection ;  
* Noun ;		    
* Numeral ;       
* Parenthetical ; 
* Particle ;      
* Predicative ;   
* Preposition ;   
* Pronoun ;	    
* Verb ;		    
* Propernoun ;    
* Punctuation ;   
* Symbols     ;   
* LexicalizedParticiple ;   

* * *

<small>This (part of) documentation was generated from [src/fst/morphology/root.lexc](https://github.com/giellalt/lang-rus/blob/main/src/fst/morphology/root.lexc)</small>

---

## src-fst-morphology-stems-adjectives.lexc.md 



* * *

<small>This (part of) documentation was generated from [src/fst/morphology/stems/adjectives.lexc](https://github.com/giellalt/lang-rus/blob/main/src/fst/morphology/stems/adjectives.lexc)</small>

---

## src-fst-morphology-stems-numerals.lexc.md 



* * *

<small>This (part of) documentation was generated from [src/fst/morphology/stems/numerals.lexc](https://github.com/giellalt/lang-rus/blob/main/src/fst/morphology/stems/numerals.lexc)</small>

---

## src-fst-phonetics-txt2ipa.xfscript.md 



retroflex plosive, voiceless			t`  ʈ	    0288, 648 (` = ASCII 096)
retroflex plosive, voiced			d`	ɖ		0256, 598
labiodental nasal					F 	ɱ		0271, 625
retroflex nasal						n` 	ɳ		0273, 627
palatal nasal						J 	ɲ		0272, 626
velar nasal							N 	ŋ		014B, 331
uvular nasal							N\	ɴ		0274, 628
	
bilabial trill						B\ 	ʙ		0299, 665
uvular trill							R\ 	ʀ		0280, 640
alveolar tap							4	ɾ		027E, 638
retroflex flap						r` 	ɽ		027D, 637
bilabial fricative, voiceless		p\ 	ɸ		0278, 632
bilabial fricative, voiced			B 	β		03B2, 946
dental fricative, voiceless			T 	θ		03B8, 952
dental fricative, voiced				D 	ð		00F0, 240
postalveolar fricative, voiceless	S	ʃ		0283, 643
postalveolar fricative, voiced		Z 	ʒ		0292, 658
retroflex fricative, voiceless		s` 	ʂ		0282, 642
retroflex fricative, voiced			z` 	ʐ		0290, 656
palatal fricative, voiceless			C 	ç		00E7, 231
palatal fricative, voiced			j\ 	ʝ		029D, 669
velar fricative, voiced	        	G 	ɣ		0263, 611
uvular fricative, voiceless			X	χ		03C7, 967
uvular fricative, voiced				R 	ʁ		0281, 641
pharyngeal fricative, voiceless		X\ 	ħ		0127, 295
pharyngeal fricative, voiced			?\ 	ʕ		0295, 661
glottal fricative, voiced			h\	ɦ		0266, 614

alveolar lateral fricative, vl.		K 
alveolar lateral fricative, vd.		K\

labiodental approximant				P (or v\) 
alveolar approximant					r\ 
retroflex approximant				r\` 
velar approximant					M\

retroflex lateral approximant		l` 
palatal lateral approximant			L 
velar lateral approximant			L\
Clicks

bilabial								O\	(O = capital letter) 
dental								|\
(post)alveolar						!\ 
palatoalveolar						=\ 
alveolar lateral						|\|\
Ejectives, implosives

ejective								_>	e.g. ejective p		p_>
implosive							_<	e.g. implosive b	b_<
Vowels

close back unrounded					M
close central unrounded 				1 
close central rounded				} 
lax i								I 
lax y								Y 
lax u								U

close-mid front rounded				2 
close-mid central unrounded			@\ 
close-mid central rounded			8 
close-mid back unrounded				7

schwa	ə							@

open-mid front unrounded				E 
open-mid front rounded				9
open-mid central unrounded			3 
open-mid central rounded				3\ 
open-mid back unrounded				V 
open-mid back rounded				O

ash (ae digraph)						{ 
open schwa (turned a)				6

open front rounded					& 
open back unrounded	        		A 
open back rounded					Q
Other symbols

voiceless labial-velar fricative		W 
voiced labial-palatal approx.		H 
voiceless epiglottal fricative		H\ 
voiced epiglottal fricative			<\ 
epiglottal plosive					>\

alveolo-palatal fricative, vl. 		s\ 
alveolo-palatal fricative, voiced	z\ 
alveolar lateral flap				l\ 
simultaneous S and x					x\ 
tie bar								_
Suprasegmentals

primary stress						" 
secondary stress						% 
long									: 
half-long							:\ 
extra-short							_X 
linking mark							-\
Tones and word accents

level extra high						_T 
level high							_H
level mid							_M 
level low							_L 
level extra low						_B
downstep								! 
upstep								^	(caret, circumflex)

contour, rising						 
contour, falling						_F 
contour, high rising					_H_T 
contour, low rising					_B_L 

contour, rising-falling				_R_F 
(NB Instead of being written as diacritics with _, all prosodic 
marks can alternatively be placed in a separate tier, set off 
by < >, as recommended for the next two symbols.)
global rise						<R> 
global fall						<F>
Diacritics						
									
voiceless						_0	(0 = figure), e.g. n_0
voiced							_v 
aspirated						_h 
more rounded						_O	(O = letter) 
less rounded						_c 
advanced							_+
retracted						_-
centralized						_" 
syllabic							=	(or _=) e.g. n= (or n_=) 
non-syllabic						_^ 
rhoticity						`
									
breathy voiced					_t 
creaky voiced					_k
linguolabial						_N 
labialized						_w 
palatalized						'	(or _j) e.g. t' (or t_j) 
velarized						_G 
pharyngealized					_?\
									
dental							_d 
apical							_a 
laminal							_m
nasalized						~	(or _~) e.g. A~ (or A_~) 
nasal release					_n
lateral release					_l 
no audible release				_}

velarized or pharyngealized		_e 
velarized l, alternatively		5 
raised							_r 
lowered							_o 
advanced tongue root				_A 
retracted tongue root			_q

* * *

<small>This (part of) documentation was generated from [src/fst/phonetics/txt2ipa.xfscript](https://github.com/giellalt/lang-rus/blob/main/src/fst/phonetics/txt2ipa.xfscript)</small>

---

## src-fst-transcriptions-transcriptor-abbrevs2text.lexc.md 



We describe here how abbreviations are in Russian are read out, e.g.
for text-to-speech systems.

For example:

* s.:syntynyt # ;  
* os.:omaa% sukua # ;  
* v.:vuosi # ;  
* v.:vuonna # ;  
* esim.:esimerkki # ; 
* esim.:esimerkiksi # ; 

* * *

<small>This (part of) documentation was generated from [src/fst/transcriptions/transcriptor-abbrevs2text.lexc](https://github.com/giellalt/lang-rus/blob/main/src/fst/transcriptions/transcriptor-abbrevs2text.lexc)</small>

---

## src-fst-transcriptions-transcriptor-numbers-digit2text.lexc.md 



* * *

<small>This (part of) documentation was generated from [src/fst/transcriptions/transcriptor-numbers-digit2text.lexc](https://github.com/giellalt/lang-rus/blob/main/src/fst/transcriptions/transcriptor-numbers-digit2text.lexc)</small>

---

## src-fst-transcriptions-transcriptor-symbols2text.lexc.md 



This file contains mappings from abbreviations and some acronyms to full
forms for text-to-speech purposes. This is a supplement to the analyser;
the analyser must tag the strings as +ABBR or similar for the transcriptions
to work. The resulting full form must be lemmas known to the analyser,
for further processing.

We describe here how abbreviations in Russian are read out,
for text-to-speech systems.

The file contains:

- miscellaneous symbols

- smileys

- Clause boundary symbols

- Single punctuation marks

- Paired punctuation marks

* * *

<small>This (part of) documentation was generated from [src/fst/transcriptions/transcriptor-symbols2text.lexc](https://github.com/giellalt/lang-rus/blob/main/src/fst/transcriptions/transcriptor-symbols2text.lexc)</small>

---

## tools-grammarcheckers-grammarchecker.cg3.md 


R U S S I A N   G R A M M A R   C H E C K E R

## DELIMITERS

## TAGS AND SETS

### Tags

This section lists all the tags inherited from the fst, and used as tags
in the syntactic analysis. The next section, **Sets**, contains sets defined
on the basis of the tags listed here, those set names are not visible in the output.

Grammarchecker rules begin here 

### Grammarchecker sets

### Grammarchecker rules

* * *

<small>This (part of) documentation was generated from [tools/grammarcheckers/grammarchecker.cg3](https://github.com/giellalt/lang-rus/blob/main/tools/grammarcheckers/grammarchecker.cg3)</small>

---

## tools-tokenisers-tokeniser-disamb-gt-desc.pmscript.md 

## Tokeniser for rus

Usage:
```
$ make
$ echo "ja, ja" | hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
$ echo "Juos gorreválggain lea (dárbbašlaš) deavdit gáibádusa boasttu olmmoš, man mielde lahtuid." | hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
$ echo "(gáfe) 'ja' ja 3. ja? ц jaja ukjend \"ukjend\"" | hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
$ echo "márffibiillagáffe" | hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
```

Pmatch documentation:
<https://github.com/hfst/hfst/wiki/HfstPmatch>

Characters which have analyses in the lexicon, but can appear without spaces
before/after, that is, with no context conditions, and adjacent to words:
* Punct contains ASCII punctuation marks
* The symbol after m-dash is soft-hyphen `U+00AD`
* The symbol following {•} is byte-order-mark / zero-width no-break space
`U+FEFF`.

Whitespace contains ASCII white space and
the List contains some unicode white space characters
* En Quad U+2000 to Zero-Width Joiner U+200d'
* Narrow No-Break Space U+202F
* Medium Mathematical Space U+205F
* Word joiner U+2060

Apart from what's in our morphology, there are
1. unknown word-like forms, and
2. unmatched strings
We want to give 1) a match, but let 2) be treated specially by
`hfst-tokenise -a`
Unknowns are made of:
* lower-case ASCII
* upper-case ASCII
* Cyrillic block (U+0400 - U+04FF)
ASCII digits
* select symbols
* Combining diacritics as individual symbols,
* various symbols from Private area (probably Microsoft),
so far:
* U+F0B7 for "x in box"

### Unknown handling
Unknowns are tagged ?? and treated specially with `hfst-tokenise`
hfst-tokenise --giella-cg will treat such empty analyses as unknowns, and
remove empty analyses from other readings. Empty readings are also
legal in CG, they get a default baseform equal to the wordform, but
no tag to check, so it's safer to let hfst-tokenise handle them.

Finally we mark as a token any sequence making up a:
* known word in context
* unknown (OOV) token in context
* sequence of word and punctuation
* URL in context

* * *

<small>This (part of) documentation was generated from [tools/tokenisers/tokeniser-disamb-gt-desc.pmscript](https://github.com/giellalt/lang-rus/blob/main/tools/tokenisers/tokeniser-disamb-gt-desc.pmscript)</small>

---

## tools-tokenisers-tokeniser-gramcheck-gt-desc.pmscript.md 

## Grammar checker tokenisation for rus

Requires a recent version of HFST (3.10.0 / git revision>=3aecdbc)
Then just:
```
$ make
$ echo "ja, ja" | hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
```

More usage examples:
```
$ echo "Juos gorreválggain lea (dárbbašlaš) deavdit gáibádusa boasttu olmmoš, man mielde lahtuid." | hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
$ echo "(gáfe) 'ja' ja 3. ja? ц jaja ukjend \"ukjend\"" | hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
$ echo "márffibiillagáffe" | hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
```

Pmatch documentation:
<https://github.com/hfst/hfst/wiki/HfstPmatch>

Characters which have analyses in the lexicon, but can appear without spaces
before/after, that is, with no context conditions, and adjacent to words:
* Punct contains ASCII punctuation marks
* The symbol after m-dash is soft-hyphen `U+00AD`
* The symbol following {•} is byte-order-mark / zero-width no-break space
`U+FEFF`.

Whitespace contains ASCII white space and
the List contains some unicode white space characters
* En Quad U+2000 to Zero-Width Joiner U+200d'
* Narrow No-Break Space U+202F
* Medium Mathematical Space U+205F
* Word joiner U+2060

Apart from what's in our morphology, there are
1) unknown word-like forms, and
2) unmatched strings
We want to give 1) a match, but let 2) be treated specially by hfst-tokenise -a
* select extended latin symbols
* select symbols
* various symbols from Private area (probably Microsoft),
so far:
* U+F0B7 for "x in box"

TODO: Could use something like this, but built-in's don't include šžđčŋ:

Simply give an empty reading when something is unknown:
hfst-tokenise --giella-cg will treat such empty analyses as unknowns, and
remove empty analyses from other readings. Empty readings are also
legal in CG, they get a default baseform equal to the wordform, but
no tag to check, so it's safer to let hfst-tokenise handle them.

Finally we mark as a token any sequence making up a:
* known word in context
* unknown (OOV) token in context
* sequence of word and punctuation
* URL in context

* * *

<small>This (part of) documentation was generated from [tools/tokenisers/tokeniser-gramcheck-gt-desc.pmscript](https://github.com/giellalt/lang-rus/blob/main/tools/tokenisers/tokeniser-gramcheck-gt-desc.pmscript)</small>

---

## tools-tokenisers-tokeniser-tts-cggt-desc.pmscript.md 

## TTS tokenisation for smj

Requires a recent version of HFST (3.10.0 / git revision>=3aecdbc)
Then just:
```sh
make
echo "ja, ja" \
| hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
```

More usage examples:
```sh
echo "Juos gorreválggain lea (dárbbašlaš) deavdit gáibádusa \
boasttu olmmoš, man mielde lahtuid." \
| hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
echo "(gáfe) 'ja' ja 3. ja? ц jaja ukjend \"ukjend\"" \
| hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
echo "márffibiillagáffe" \
| hfst-tokenise --giella-cg tokeniser-disamb-gt-desc.pmhfst
```

Pmatch documentation:
<https://kitwiki.csc.fi/twiki/bin/view/KitWiki/HfstPmatch>

Characters which have analyses in the lexicon, but can appear without spaces
before/after, that is, with no context conditions, and adjacent to words:
* Punct contains ASCII punctuation marks
* The symbol after m-dash is soft-hyphen `U+00AD`
* The symbol following {•} is byte-order-mark / zero-width no-break space
`U+FEFF`.

Whitespace contains ASCII white space and
the List contains some unicode white space characters
* En Quad U+2000 to Zero-Width Joiner U+200d'
* Narrow No-Break Space U+202F
* Medium Mathematical Space U+205F
* Word joiner U+2060

Apart from what's in our morphology, there are
1) unknown word-like forms, and
2) unmatched strings
We want to give 1) a match, but let 2) be treated specially by hfst-tokenise -a
* select extended latin symbols
* select symbols
* various symbols from Private area (probably Microsoft),
so far:
* U+F0B7 for "x in box"

TODO: Could use something like this, but built-in's don't include šžđčŋ:

Simply give an empty reading when something is unknown:
hfst-tokenise --giella-cg will treat such empty analyses as unknowns, and
remove empty analyses from other readings. Empty readings are also
legal in CG, they get a default baseform equal to the wordform, but
no tag to check, so it's safer to let hfst-tokenise handle them.

Needs hfst-tokenise to output things differently depending on the tag they get

* * *

<small>This (part of) documentation was generated from [tools/tokenisers/tokeniser-tts-cggt-desc.pmscript](https://github.com/giellalt/lang-rus/blob/main/tools/tokenisers/tokeniser-tts-cggt-desc.pmscript)</small>
