import networkx as nx
import matplotlib.pyplot as plt

def greedy_coloring(graph):
    result = {}
    for node in graph.nodes():
        neighbor_colors = {result[neighbor] for neighbor in graph.neighbors(node) if neighbor in result}
        color = 0
        while color in neighbor_colors:
            color += 1
        result[node] = color
    return result

# Пример графа
G = nx.Graph()
edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
G.add_edges_from(edges)

# Раскраска
coloring = greedy_coloring(G)

# Отображаем граф
node_colors = [coloring[node] for node in G.nodes()]
pos = nx.spring_layout(G)

plt.figure(figsize=(6, 4))
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, cmap=plt.cm.Set3)
plt.title("Graph Coloring with Greedy Algorithm")
plt.show()
