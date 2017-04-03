'''
Created on Nov 30, 2016

@author: lbozarth
'''
import os, re, string, csv

import pandas as pd
import numpy as np
from datetime import datetime
import operator

def writeToCsv(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    return

def processData(filename, userDict):
    print(filename)
    with open(filename, "rU") as  f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            try:
                user = row[2]
#                 if user == '816289049552027648':
#                     print row;
#                     break
                if user in userDict:
                    userDict[user] = userDict[user] + 1
                else:
                    userDict[user] = 0;
            except IndexError as e:
#                 print(row)
                continue
    return

def genUsers():
    userDict = {}
    dataDir = "../data/output/"
    for filename in os.listdir(dataDir):
        processData(os.path.join(dataDir,filename), userDict)
    print(len(userDict))
    sorted_data = sorted(userDict.items(), key=operator.itemgetter(1), reverse=True)
    writeToCsv("../data/analysis/users_by_screen_name_1000plus.csv", sorted_data)
        
if __name__ == '__main__':
    genUsers()