import nltk
from nltk.corpus import cmudict
d = cmudict.dict()

def count_syllables(sequence):
    return len([phonemes for phonemes in sequence if phonemes[-1].isdigit()])

def word_to_syllable_counts(word):
    return [count_syllables(variant) for variant in d[word.lower()]]

print word_to_syllable_counts('arithmetic')