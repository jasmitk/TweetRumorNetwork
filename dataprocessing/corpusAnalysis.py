'''
Created on Nov 30, 2016

@author: lbozarth
'''
import os, re, string, csv, codecs, random

from nltk import PorterStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO

cache_english_stopwords = set(stopwords.words('english'))
cache_punctuation = """!"$%&'()*+,-./:;<=>?[\]^_`{|}~"""  # Not including # and @
cache_stemmer = PorterStemmer()
cache_lemmatizer = WordNetLemmatizer()
cache_tknzr = TweetTokenizer(preserve_case=False, reduce_len=False, strip_handles=False)
def remove_hex(tweet_text):
    tweet_text_re = re.sub(r'\\x[0-9a-fA-F]+', r'', tweet_text, flags=re.MULTILINE)
    return tweet_text_re

def remove_nonascii(tweet_text):
    tweet_text_re = re.sub(r'[^\x00-\x7f]+', r'', tweet_text, flags=re.MULTILINE)
    return tweet_text_re, tweet_text_re != tweet_text

def remove_urls (tweet_text):
    tweet_text_re = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', r'', tweet_text, flags=re.MULTILINE)
    return tweet_text_re, tweet_text_re != tweet_text

def tokenize(tweet_text):
    tweet_text = tweet_text[1:] # remove b'
    tweet_text,hasUrl = remove_urls(tweet_text)
    tweet_text,hasNonascii = remove_nonascii(tweet_text)
    tweet_text = remove_hex(tweet_text)
#     print("after ul, nonascii, hex", tweet_text)
    tokens = cache_tknzr.tokenize(tweet_text)
    tokens = [i for i in tokens if i not in cache_punctuation]
    tokens = [i for i in tokens if i not in cache_english_stopwords]
#     tokens = [cache_stemmer.stem(i) for i in tokens]
    tokens = [cache_lemmatizer.lemmatize(i) for i in tokens]
    tokens = [i.strip() for i in tokens]
    return tokens,hasUrl,hasNonascii

def preprocessingRow(row):
    tweet_text= row[3]
    tokens,hasUrl,hasNonascii = tokenize(tweet_text)
    tweet_text = ' '.join(tokens)
    row[3] = tweet_text
#     row[3].append(hasUrl)
#     row[4].append(hasNonascii)
    return not tweet_text.strip()

def writeToCsv(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    return

# cutoff date
def preprocessingData(data):
    fData = []
    for index,row in data.iterrows():
        empty_text = preprocessingRow(row)
        if not empty_text:
            fData.append([row[0],row[3]])
    return fData    

def readFromCsv(filename):
    data = []
    with open(filename, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            data.append(row)
    return data

if __name__ == '__main__':
    pass