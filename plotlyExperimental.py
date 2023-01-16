"""
Plotly / NetworkX Network Graph Generator

DaCapo Brainscience, Inc.

Created by Eli Murphy

January, 2023
"""

import csv
from xml.dom.minicompat import NodeList
import networkx as nx
import matplotlib.pyplot as plt
import os 
G = nx.DiGraph()

os.chdir(r"C:\Users\elija\Documents\GitHub\DaCapo")

file = input("Input CSV Filename (include .csv): ")

with open(file, "r") as csv:
    next(csv)
    data = csv.readlines()
    #data = list(csv.reader(csv, delimiter=","))
    fromnode = []
    tonode = []
    weights = []
    temp = []
    for r in data:
        row = r.split(",")
        fromnode.append(row[0])
        tonode.append(row[1])
        weights.append(float(row[12].replace("\n", "")))

        temp.append((row[0], row[1], float(row[12].replace("\n", ""))))

    #print(fromnode, "\n", tonode, "\n", weights)

for i in range(len(fromnode)):
    G.add_weighted_edges_from(temp)
  
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size = 12)
#nx.draw(G)
plt.show()




