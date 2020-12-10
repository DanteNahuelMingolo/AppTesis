from nltk import TweetTokenizer
import pandas as pd
import itertools, re
import sys

def __parsearQuery(word):
    #word = word.split(';')
    words = [w.strip() for w in word.split(';')]
    return words

query = 'aborto; #AbortoLegal2020; salvemos las dos vidas'
print (__parsearQuery(query))