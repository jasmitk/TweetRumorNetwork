'''
Created on Apr 2, 2017

@author: lbozarth
'''
import csv, math, os
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydot, graphviz, pygraphviz
from networkx.drawing.nx_agraph import write_dot

def graphNetwork(G, topNodes):
    pos = nx.spring_layout(G, k=0.175, iterations=100)
    nx.draw_networkx_nodes(G, pos, node_color='g', node_size=10)
    nx.draw_networkx_nodes(G, pos, nodelist=topNodes, node_color='r', node_size=300)
#     nx.draw_networkx_labels(G, pos, font_size=12)
    nx.draw_networkx_edges(G, pos)
    plt.show()
    return

def getTop100():
    fn = "../data/analysis/top100"
    data = readFile(fn)
    top100 = set()
    for row in data:
        top100.add(row[0])
    return top100

def getSizes():
    fn = "../data/analysis/users_by_screen_name_1000plus.csv"
    data = readFile(fn)
    weights = {}
    for row in data:
        if(int(row[1]) == 0):
            continue
        weights[row[0]] = math.floor(math.log10(int(row[1])))
    return weights

def readFile(fn):
    data = []
    with open(fn, "rU") as  f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            data.append(row)
    return data

if __name__ == '__main__':
    fn = "../data/analysis/followers_directed_fakenews_only.csv"
    dat = readFile(fn)
    sizes = getSizes()
    top100 = getTop100()
    
    G = nx.DiGraph()
    for row in dat:
        G.add_edge(row[0], row[1])
        
    print("top100")
    top100_attr = {}
    for n in G.nodes():
        if n in top100:
            top100_attr[n] = True
        else:
            top100_attr[n] = False
         
#     print(size_attr)
    nx.set_node_attributes(G, "top100", top100_attr)
    
    print("fake")
    fake_attr = {}
    for n in G.nodes():
        if n in sizes:
            fake_attr[n] = True
        else:
            fake_attr[n] = False
         
#     print(size_attr)
    nx.set_node_attributes(G, "fakenews", fake_attr)
    
    print("frequent fake")
    freq_fake_attr = {}
    for n in G.nodes():
        if n in sizes and sizes[n] >= 1:
            freq_fake_attr[n] = True
        else:
            freq_fake_attr[n] = False
            
    print("posts fake")
    freq_fake_attr = {}
    for n in G.nodes():
        if n in sizes:
            freq_fake_attr[n] = sizes[n]
        else:
            freq_fake_attr[n] = 0
         
#     print(size_attr)
    nx.set_node_attributes(G, "postnum", freq_fake_attr)
    
    print("writing gml")
#     nx.write_pajek(G, "../data/graph/testing.net")
    write_dot(G, "../data/graph/followers_directed_fakenews_only.dot")
#     nx.write_gml(G, "../data/graph/friends_directed_fakenews_only.gml")
    
    print("ploting")
#     graphNetwork(G, topNodes)
    pass
