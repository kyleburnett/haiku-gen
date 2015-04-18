from os import listdir
from numpy import random
import json

import nltk
from nltk.corpus import cmudict

d = cmudict.dict()
puncutation = ["\"", "'", ",", "?", ":", ";", ".", "-", "..."]

def count_syllables(sequence):
    return len([phonemes for phonemes in sequence if phonemes[-1].isdigit()])

def word_to_syllable_counts(word):
    return [count_syllables(variant) for variant in d[word.lower()]]

def compile_files(path):
    files = [f for f in listdir(path)]

    data = ""
    for f in files:
        if f == '.DS_Store':
            continue
        with open(path + "/" + f, "r") as ifp:
            data += ifp.read().decode("utf-8").replace(u"\u2022", "*").encode("utf-8") + " "
    data = unicode(data, "utf-8")

    return data

def extend_markov_chain(cfd, word):
    samples = []
    counts = []
    for w, c in cfd[word].most_common(1000):
        if w not in puncutation:
            samples.append(w)
            counts.append(c)
        if len(samples) >= 10:
            break
    total = sum(counts)

    result = {}
    result["words"] = samples
    result["dist"] = [float(count) / total for count in counts]

    return result

def write_output(f, obj):
    with open(f, "w") as ofp:
        json.dump(obj, ofp)

tokens = nltk.word_tokenize(compile_files("./poems"))
bigrams = nltk.bigrams(tokens)
cfd = nltk.ConditionalFreqDist(bigrams)

lookup = {}
for word in d.keys():
    markov = extend_markov_chain(cfd, word)
    if len(markov["words"]) > 0:
        lookup[word] = {}
        lookup[word]["syllable_count"] = word_to_syllable_counts(word)[0]
        lookup[word]["markov_chain"] = markov

write_output("out.json", lookup)
