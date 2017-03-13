'''
Created on Nov 30, 2016

@author: lbozarth
'''
import os, re, string, csv

import pandas as pd
import numpy as np
from datetime import datetime
import operator

def hashtags(tweet_text):
    pattern = "(?:(?<=\s)|^)#(\w*[a-z_]+\w*)";
    li = re.findall(pattern, tweet_text, 0)
    return li

def writeToCsv(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    return

def processData(filename, hashtagDict):
    print(filename)
    with open(filename, "rU") as  f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            try:
                tweet_text = row[-2].lower()
                hashtagList = hashtags(tweet_text)
                for hashtag in hashtagList:
                    if hashtag in hashtagDict:
                        hashtagDict[hashtag] = hashtagDict[hashtag] + 1
                    else:
                        hashtagDict[hashtag] = 0;
            except IndexError as e:
                print(row)
    return

def genHashtags():
    hashtagDict = {}
    dataDir = "../data/output/"
    for filename in os.listdir(dataDir):
        processData(os.path.join(dataDir,filename), hashtagDict)
    print(len(hashtagDict))
    sorted_data = sorted(hashtagDict.items(), key=operator.itemgetter(1), reverse=True)
    writeToCsv("../data/analysis/hashtags.csv", sorted_data)
        
if __name__ == '__main__':
    genHashtags()