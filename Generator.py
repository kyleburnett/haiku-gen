from numpy import random
import json

def getSeed(lookup):
    word = random.choice(lookup.keys())
    return (word, lookup[word]["syllable_count"])

def printHaiku(words, break1, break2):
    print " ".join(words[:break1])
    print " ".join(words[break1:break2])
    print " ".join(words[break2:])

def checkHaiku(lookup, words):
    breaks = []
    counts = [5, 7, 5]
    index = 0
    total = 0
    for count in counts:
        while index < len(words):
            total += lookup[words[index]]["syllable_count"]
            if total == count:
                total = 0
                breaks.append(index + 1)
                index += 1
                break
            elif total > count:
                return []
            index += 1

    return breaks[:2]

def generateCandidate(lookup):
    words = []
    syllable_count = 0

    w, c = getSeed(lookup)
    words.append(w)
    syllable_count += c

    # Get haiku candidate
    tries = 0
    while syllable_count < 17:
        if tries > 10:
            words = []
            syllable_count = 0
            w, c = getSeed(lookup)
            words.append(w)
            syllable_count += c

        chain = lookup[words[-1]]["markov_chain"]
        # dist = [1.0 / p for p in chain["dist"]]
        # s = sum(dist)
        # dist = [p / s for p in dist]
        # choice = random.choice(chain["words"], p=dist).lower()
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
            words = []
            syllable_count = 0
            w, c = getSeed(lookup)
            words.append(w)
            syllable_count += c

    return words


with open("out.json", "r") as ifp:
    lookup = json.load(ifp)

candidate = generateCandidate(lookup)
check = checkHaiku(lookup, candidate)

while True:
    if len(check) == 2:
        printHaiku(candidate, check[0], check[1])
        break
    else:
        candidate = generateCandidate(lookup)
        check = checkHaiku(lookup, candidate)
