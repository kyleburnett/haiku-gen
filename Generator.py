from os import listdir
from numpy import random
import json

import nltk
from nltk.corpus import cmudict
d = cmudict.dict()

ifp = open("out.json", "r")

data = json.load(ifp)
