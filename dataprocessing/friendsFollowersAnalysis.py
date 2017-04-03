'''
Created on Apr 2, 2017

@author: lbozarth
'''
import os, re, string, csv, math
import pandas as pd
import numpy as np
from datetime import datetime
import operator
import snap

def writeToCsv(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    return

def processData(filename, stem, sizes, userEdges):
    print(filename)
    with open(filename, "rU") as  f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            try:
                userHandle = row[1]
                if userHandle in sizes:
                    userEdges.append([userHandle, stem])
            except IndexError as e:
#                 print(row)
                continue
    return

def getSizes():
    fn = "../data/analysis/users_by_screen_name_1000plus.csv"
    data = readFile(fn)
    weights = {}
    for row in data:
        if(int(row[1]) == 0):
            continue
        weights[row[0]] = math.log10(int(row[1]))
    return weights

def readFile(fn):
    data = []
    with open(fn, "rU") as  f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            data.append(row)
    return data

def genUsers():
    sizes = getSizes()
    userEdges = []
    dataDir = "../data/followers"
    for filename in os.listdir(dataDir):
        stem = filename.split(".cs")[0]
        print(stem)
        processData(os.path.join(dataDir, filename), stem, sizes, userEdges)

    print(len(userEdges))
    writeToCsv("../data/analysis/followers_directed_fakenews_only.csv", userEdges)
        
if __name__ == '__main__':
    genUsers()
