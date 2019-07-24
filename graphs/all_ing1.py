######################################################################################################
# All the ingredients on one graph with connection to the most similar item.
######################################################################################################
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import json
from matplotlib import cm


f = open('ingredients.json')
ALL_FOOD_DICT = json.load(f)

id2name = {}
for key, val in ALL_FOOD_DICT.items():
    id2name[val[0]] = key

def plot_weighted_graph(items, sizes, edges, pos, colors):
    "Plot a weighted graph"
    # 1. Add nodes
    G = nx.Graph()  # Create a graph object called G
    node_list = items
    for node in node_list:
        G.add_node(node)

    for i, n in enumerate(node_list):
        col = colors[i]
        nx.draw_networkx_nodes(G, pos, nodelist=[n], node_color=col, node_size=sizes[i])

    # 2. add labels to the nodes
    labels = {}
    for node_name in node_list:
        labels[str(node_name)] = str(node_name)
    nx.draw_networkx_labels(G, pos, labels, font_size=7)

    # 3. Add the edges (4C2 = 6 combinations)
    for i in range(len(node_list)):
        G.add_edge(node_list[i], id2name[edges[i]])

    nx.draw_networkx_edges(G, pos, edge_color='gray')

    # Plot the graph
    plt.axis('off')
    # plt.legend(loc=3, fontsize='xx-small')
    plt.title('Ingredients similarity')
    plt.savefig("similarity.png")

    plt.show()


# ----START OF SCRIPT
if __name__ == '__main__':
    all_data = pd.read_csv("rep_foods.csv", encoding='latin-1')
    items = list((all_data.values[:, 2]))

    cat = list((all_data.values[:, 3]))
    c_set = set(cat)
    d_cat = {}
    j = 1
    for c in c_set:
        d_cat[c] = j
        j += 20
    colors = []
    for c in cat:
        colors.append(d_cat[c])
    colors = cm.gist_rainbow(colors)

    sim_mat = np.load('sim_matrix.npy')
    db_2d = np.load('compdb_2D.npy')
    sizes = np.zeros(len(items))
    edges = np.zeros(len(items))
    pos = {}
    for i, item in enumerate(items):
        sizes[i] = (ALL_FOOD_DICT[item][2])
        edges[i] = np.argmin(sim_mat[ALL_FOOD_DICT[item][0]])
        pos[item] = db_2d[ALL_FOOD_DICT[item][0]]

    sizes = ((sizes/np.sum(sizes))*10000).astype(np.int)
    edges = edges.astype(np.int)
    plot_weighted_graph(items, sizes.tolist(), edges.tolist(), pos, colors)
