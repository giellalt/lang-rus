# /// script
# dependencies = [
#   "tqdm",
# ]
# ///

"""Attempt to map lexemes to Zaliznyak stress patterns based on orthography.
(Most lexemes will be unsuccessful.)
"""

import re

from tqdm import tqdm


def add_stress_to_wordforms(lexeme_wordforms):
    """Spelling rules disallow unstressed 'o' after hushers (ж, ш, щ, ч).
    Therefore, if we see 'o' after a husher, we can deduce that it must be stressed.
    """
    stressed_forms = [re.sub(r'(?<=[ЖШЩЧ])О', 'О\u0301', form) for form in lexeme_wordforms]
    stressed_matches = [list(re.finditer(r'\u0301|Ë', form)) for form in stressed_forms]
    assert all(len(m) <= 1 for m in stressed_matches), f"Multiple stresses found in a single form: {stressed_forms}"
    if all(stressed_matches):
        return stressed_forms
    elif any(stressed_matches):
        return None  # TODO rethink
    if not any(stressed_matches):
        return lexeme_wordforms


def transform_to_shapes(stressed_forms):
    """Translate wordforms to cVcvc... shapes, taking into account
    the possibility of fleeting vowels.
    c = consonant (cluster)
    v = unstressed vowel
    V = stressed vowel
    o = unstressed fleeting vowel
    O = stressed fleeting vowel
    """
    # Work left to right aligning consonants and vowels of all forms.
    # If all some forms have a vowel between two consonants, while others
    # have either nothing or a soft sign, then it is a fleeting vowel.
    shapes = []
    for form in lexeme_wordforms:
        # this approach is too simplistic; needs to account for fleeting vowels
        shape = re.sub(r'[АЕИОУЫЭЮЯ]\u0301|Ё', 'V', form)
        shape = re.sub(r'[АЕИОУЫЭЮЯ]', 'v', shape)
        shape = re.sub(r'[^АЕИОУЫЭЮЯVv]', 'c', shape)
        shapes.append(shape)


    # get "stem"
    shortest_len = min(len(form) for form in lexeme_wordforms)
    stem_end = 0
    for i in range(shortest_len):
        chars = {form[i] for form in lexeme_wordforms}
        if len(chars) == 1:
            stem_end += 1
        else:
            break
    stem = lexeme_wordforms[0][:stem_end]

    for form in lexeme_wordforms:
        assert form.isupper(), "All forms must be uppercase"
        if 'Ë' in form:
            stressed_forms.append(form.replace('Ë', 'Ё́'))
        # Simple heuristic: add stress on the first vowel
        stressed_form = re.sub(r'([аеёиоуыэюя])', r'\1́', form, count=1)
        stressed_forms.append(stressed_form)
    return stressed_forms


with open('dict.opcorpora.txt') as f:
    lexeme_wordforms = []
    lexemes_found = 0
    wordforms_found = 0
    lexeme_count = 0
    wordform_count = 0
    for line in tqdm(f, total=5924998):  # 5924998 lines
        line = line.strip()
        if re.match(r'\d+$', line):  # new lexeme block
            lex_enum = line
        elif reading := re.match(r'(\w+)\t([A-Z]+),([a-z,]+) ([a-z,]+)', line):  # reading
            wordform, pos, lex_tags, infl_tags = reading.groups()
            lexeme_wordforms.append(wordform)
            wordform_count += 1
        elif not line.strip():  # end of lexeme block
            found = False
            # Determine stress, if possible
            for form in lexeme_wordforms:
                if re.search(r'[ЖШЩЧ]О', form):
                    wordforms_found += 1
                    found = True
            lexemes_found += int(found)
            lexeme_count += 1
            lexeme_wordforms = []

            # stressed_forms = add_stress_to_wordforms(lexeme_wordforms)

print(f"Lexemes with deduced stress: {lexemes_found} ({100 * lexemes_found/int(lex_enum):.2f}%)")
print(f"Wordforms with deduced stress: {wordforms_found} ({100 * wordforms_found/wordform_count:.2f}%)")
