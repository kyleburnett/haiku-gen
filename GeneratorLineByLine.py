from numpy import random
import json

import nltk
from nltk.corpus import stopwords
sw = set(stopwords.words('english'))

def getSeed(lookup):
    word = random.choice(lookup.keys())
    return (word, lookup[word]["syllable_count"])

def printHaiku(words, break1, break2):
    print " ".join(words[:break1])
    print " ".join(words[break1:break2])
    print " ".join(words[break2:])

def generateLine(lookup, length):
    words = []
    syllable_count = 0

    w, c = getSeed(lookup)
    words.append(w)
    syllable_count += c

    # Get haiku candidate
    tries = 0
    while syllable_count < length:
        if tries > 10:
            words = []
            syllable_count = 0
            w, c = getSeed(lookup)
            words.append(w)
            syllable_count += c

        chain = lookup[words[-1]]["markov_chain"]
        dist = [1.0 / p for p in chain["dist"]]
        s = sum(dist)
        dist = [p / s for p in dist]
        choice = random.choice(chain["words"], p=dist).lower()
        try:
            count = lookup[choice]["syllable_count"]
            words.append(choice)
            syllable_count += count
            tries = 0
        except KeyError:
            tries += 1
            continue

        if syllable_count > length or tries > 10:
            words = []
            syllable_count = 0
            w, c = getSeed(lookup)
            words.append(w)
            syllable_count += c

        if syllable_count == length and words[-1] in sw:
            words = []
            syllable_count = 0
            w, c = getSeed(lookup)
            words.append(w)
            syllable_count += c

    return words


with open("out.json", "r") as ifp:
    lookup = json.load(ifp)

line1 = generateLine(lookup, 5)
line2 = generateLine(lookup, 7)
line3 = generateLine(lookup, 5)

poem = line1 + line2 + line3

printHaiku(poem, len(line1), len(line1) + len(line2))
