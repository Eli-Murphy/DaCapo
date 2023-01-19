'''
Betweenness Centrality Graph Generator

DaCapo Brainscience

Created by Eli Murphy

January, 2023
'''

import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

G = nx.Graph()

csvpath = r"C:\Users\elija\Documents\GitHub\dcb-network\datasets\ppi_0.3_subset.csv" #DEAD PATH

filename = Path(csvpath).stem

edgelist = []

with open(csvpath, "r") as csv:
    next(csv)
    for row in csv:
        splitRow = row.split(",")
        splitRow[2] = splitRow[2].replace("\n", "")
        edgelist.append((splitRow[0], splitRow[1], float(splitRow[2])))
G.add_weighted_edges_from(edgelist)

# largest connected component
components = nx.connected_components(G)
largest_component = max(components, key=len)
H = G.subgraph(largest_component)

# compute centrality
centrality = nx.betweenness_centrality(H, k=10, endpoints=True)

print(centrality)

# compute community structure
lpc = nx.community.label_propagation_communities(H)
community_index = {n: i for i, com in enumerate(lpc) for n in com}

#### draw graph ####
fig, ax = plt.subplots(figsize=(20, 15))
pos = nx.spring_layout(H, k=0.15, seed=4572321)
node_color = [community_index[n] for n in H]
node_size = [v * 20000 for v in centrality.values()]
nx.draw_networkx(
    H,
    pos=pos,
    with_labels=True,
    node_color=node_color,
    node_size=node_size,
    edge_color="gainsboro",
    alpha=0.4,
    font_size=1
)

# Title/legend
font = {"color": "k", "fontweight": "bold", "fontsize": 20}
ax.set_title(filename, font)
# Change font color for legend
font["color"] = "r"

ax.text(
    0.80,
    0.10,
    "node color = community structure",
    horizontalalignment="center",
    transform=ax.transAxes,
    fontdict=font,
)
ax.text(
    0.80,
    0.06,
    "node size = betweenness centrality",
    horizontalalignment="center",
    transform=ax.transAxes,
    fontdict=font,
)

# Resize figure for label readability
ax.margins(0.1, 0.05)
fig.tight_layout()
plt.axis("off")
plt.savefig('ppi_0.3_subset.pdf')  
plt.show()
