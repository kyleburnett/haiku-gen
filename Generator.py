from os import listdir
from numpy import random
import json

def getSeed(lookup):
    word = random.choice(lookup.keys())
    return (word, lookup[word]["syllable_count"])

def printHaiku(words, break1, break2):
    print " ".join(words[:break1])
    print " ".join(words[break1:break2])
    print " ".join(words[break2:])

with open("out.json", "r") as ifp:
    lookup = json.load(ifp)

# Initialize word list and syllable_count
words = []
syllable_count = 0

# Get random seed
w, c = getSeed(lookup)
words.append(w)
syllable_count += c

# Line 1
tries = 0
while syllable_count < 5:
    chain = lookup[words[-1]]["markov_chain"]
    choice = random.choice(chain["words"], p=chain["dist"]).lower()
    try:
        count = lookup[choice]["syllable_count"]
        words.append(choice)
        syllable_count += count
        tries = 0
    except KeyError:
        tries += 1
        continue

    if syllable_count > 5 or tries > 10:
        words = []
        syllable_count = 0
        w, c = getSeed(lookup)
        words.append(w)
        syllable_count += c

line1_count = len(words)

# Line 2
tries = 0
while syllable_count < 12:
    chain = lookup[words[-1]]["markov_chain"]
    choice = random.choice(chain["words"], p=chain["dist"]).lower()
    try:
        count = lookup[choice]["syllable_count"]
        words.append(choice)
        syllable_count += count
        tries = 0
    except KeyError:
        tries += 1
        continue

    if syllable_count > 12 or tries > 10:
        words = words[:line1_count]
        syllable_count = 5

line2_count = len(words)

# Line 3
tries = 0
while syllable_count < 17:
    chain = lookup[words[-1]]["markov_chain"]
    choice = random.choice(chain["words"], p=chain["dist"]).lower()
    try:
        count = lookup[choice]["syllable_count"]
        words.append(choice)
        syllable_count += count
        tries = 0
    except KeyError:
        tries += 1
        continue

    if syllable_count > 17 or tries > 10:
        words = words[:line2_count]
        syllable_count = 12

printHaiku(words, line1_count, line2_count)