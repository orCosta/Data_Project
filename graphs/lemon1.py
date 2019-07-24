###################################################################################
# Graph of lemon similarity to 25 others fruits.
###################################################################################
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg as LA
import networkx as nx



def PCA(data, dims_rescaled_data=2):
    """
    returns: data transformed in 2 dims/columns + regenerated original data
    pass in: data as 2D NumPy array
    """
    m, n = data.shape
    # mean center the data
    data -= data.mean(axis=0)
    # calculate the covariance matrix
    R = np.cov(data, rowvar=False)
    # calculate eigenvectors & eigenvalues of the covariance matrix
    # use 'eigh' rather than 'eig' since R is symmetric,
    # the performance gain is substantial
    evals, evecs = LA.eigh(R)
    # sort eigenvalue in decreasing order
    idx = np.argsort(evals)[::-1]
    evecs = evecs[:,idx]
    # sort eigenvectors according to same index
    evals = evals[idx]
    # select the first n eigenvectors (n is desired dimension
    # of rescaled data array, or dims_rescaled_data)
    evecs = evecs[:, :dims_rescaled_data]
    # carry out the transformation on the data using eigenvectors
    # and return the re-scaled data, eigenvalues, and eigenvectors
    return np.dot(evecs.T, data.T).T, evals, evecs




v = np.load("compdb_fruit.npy")
items = ["Coconut", "Grapefruit", "Banana", "Grape", "Blackberry", "Guava", "Peach", "Sweet cherry", "Date", "Passion fruit", "Kiwi", "Pineapple", "Custard apple",
         "Star fruit", "Papaya", "Lime", "Lemon", "Pummelo", "Mandarin", "Orange", "Quince", "Black crowberry", "Apple", "Strawberry", "Lichee", "Mango"]

lemon_w = [ 67, 76,  61,  85,  45,  84,  76,  49,  68,  31,  65,  69,  25,  50,  89, 104, 293,  42, 158, 181,  31,   1, 0,  60,  29,  71]

def plot_weighted_graph(pos):
    "Plot a weighted graph"

    # 2. Add nodes
    G = nx.Graph()  # Create a graph object called G
    node_list = ["Coconut", "Grapefruit", "Banana", "Grape", "Blackberry", "Guava", "Peach", "Sweet cherry", "Date", "Passion fruit", "Kiwi", "Pineapple", "Custard apple"
    , "Star fruit", "Papaya", "Lime", "Lemon", "Pummelo", "Mandarin", "Orange", "Quince", "Black crowberry", "Apple", "Strawberry", "Lichee", "Mango"]
    for node in node_list:
        G.add_node(node)

  
    nx.draw_networkx_nodes(G, pos, node_color='m', node_size=500)

    # 3. add labels to the nodes
    labels = {}
    for node_name in node_list:
        labels[str(node_name)] = str(node_name)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    # 4. Add the edges 
    for i, w in enumerate(lemon_w):
        if i == 16:
            continue
        G.add_edge(node_list[16], node_list[i], weight=w)

    all_weights = []
    # 4 a. Iterate through the graph nodes to gather all the weights
    for (node1, node2, data) in G.edges(data=True):
        all_weights.append(data['weight'])  # we'll use this when determining edge thickness

    # 4 b. Get unique weights
    unique_weights = list(set(all_weights))

    # 4 c. Plot the edges - one by one!

    for weight in unique_weights:
        # 4 d. Form a filtered list with just the weight you want to draw
        weighted_edges = [(node1, node2) for (node1, node2, edge_attr) in G.edges(data=True) if
                          edge_attr['weight'] == weight]
        # 4 e. I think multiplying by [num_nodes/sum(all_weights)] makes the graphs edges look cleaner
        width = weight * len(node_list) * 2.0 / sum(all_weights)
        nx.draw_networkx_edges(G, pos, edgelist=weighted_edges, width=width, edge_color='gray', label=weight)

    # Plot the graph
    plt.axis('off')
    plt.legend(loc=3, fontsize='xx-small')
    plt.title('Lemon molecular structure similarity')
    plt.savefig("chess_legends.png")

    plt.show()



idx = np.argwhere(np.all(v[..., :] == 0, axis=0))
v2 = np.delete(v, idx, axis=1)

v3, val, vec = PCA(v2)
posi = {}
for j, item in enumerate(items):
    posi[item] = v3[j]

plot_weighted_graph(posi)





















