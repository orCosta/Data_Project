import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import cm

items = ["Coconut", "Grapefruit", "Banana", "Grape", "Blackberry", "Guava", "Peach", "Sweet cherry", "Date", "Passion fruit", "Kiwi", "Pineapple", "Custard apple"
    , "Star fruit", "Papaya", "Lime", "Lemon", "Pummelo", "Mandarin", "Orange", "Quince", "Black crowberry", "Apple", "Strawberry", "Lichee", "Mango"]
lemon_w = [ 67, 76,  61,  85,  45,  84,  76,  49,  68,  31,  65,  69,  25,  50,  89, 104, 293,  42, 158, 181,  31,   1,   0,  60,  29,  71]

def plot_weighted_graph():
    "Plot a weighted graph"

    # 2. Add nodes
    G = nx.Graph()  # Create a graph object called G
    node_list = ["Coconut", "Grapefruit", "Banana", "Grape", "Blackberry", "Guava", "Peach", "Sweet cherry", "Date", "Passion fruit", "Kiwi", "Pineapple", "Custard apple"
    , "Star fruit", "Papaya", "Lime", "Lemon", "Pummelo", "Mandarin", "Orange", "Quince", "Black crowberry", "Apple", "Strawberry", "Lichee", "Mango"]
    for node in node_list:
        G.add_node(node)

    # Note: You can also try a spring_layout
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='green', node_size=500)

    # 3. If you want, add labels to the nodes
    labels = {}
    for node_name in node_list:
        labels[str(node_name)] = str(node_name)
    nx.draw_networkx_labels(G, pos, labels, font_size=11)

    # 4. Add the edges (4C2 = 6 combinations)
    # NOTE: You usually read this data in from some source
    # To keep the example self contained, I typed this out
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


# ----START OF SCRIPT
if __name__ == '__main__':
    plot_weighted_graph()