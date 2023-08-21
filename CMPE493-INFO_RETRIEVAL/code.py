# -*- coding: utf-8 -*-
"""PageRank_Updated.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/152E1SZyNZccxk4YxjM2boLpp0sduFA4w
"""

from google.colab import drive
drive.mount('/content/drive')

"""<font color ='blue'> Data Readering And Preprocessing """

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    vertices = {}
    edges = []
    is_vertex = True

    for line in lines:
        line = line.strip()
        if line == '*Vertices':
            continue
        elif line == '*Edges':
            is_vertex = False
            continue

        if is_vertex:
            try:
                vertex_id, vertex_name = line.split(' ', 1)  # splitting only on the first space
                vertices[int(vertex_id)] = vertex_name.strip('"')
            except ValueError:
                # This line is not a vertex data line, skip it
                continue
        else:
            vertex1, vertex2 = map(int, line.split(' '))
            edges.append((vertex1, vertex2))

    return vertices, edges

vertices, edges = read_data('/content/drive/MyDrive/Colab Notebooks/data.txt') # Reading data from 'data.txt' file

print("Vertices:", vertices)
print("Edges:", edges)

print("\nNumber of nodes (vertices):", len(vertices))
print("Number of edges:", len(edges))

"""<font color ='blue'> Graph of Vertices And Nodes"""

def create_graph(vertices, edges):
    graph = {vertex: [] for vertex in vertices}

    for edge in edges:
        vertex1, vertex2 = edge
        graph[vertex1].append(vertex2)
        graph[vertex2].append(vertex1)

    return graph

graph = create_graph(vertices, edges) # Creating graph

# Printing graph
for vertex, connected_vertices in graph.items():
    print(f"Vertex {vertex} ({vertices[vertex]}): {connected_vertices}")

"""<font color ='blue'> Directed Graph And Adjacency Matrix"""

def create_directed_graph(vertices, edges):
    graph = {vertex: [] for vertex in vertices}

    for edge in edges:
        vertex1, vertex2 = edge
        graph[vertex1].append(vertex2)  # Edge from vertex1 to vertex2

    return graph

def create_adjacency_matrix(vertices, edges):
    # Initializing the adjacency matrix with zeros
    adjacency_matrix = np.zeros((len(vertices), len(vertices)))

    for edge in edges:
        vertex1, vertex2 = edge
        # As the vertices are 1-indexed, we subtract 1 when accessing the matrix
        adjacency_matrix[vertex1-1][vertex2-1] = 1
        adjacency_matrix[vertex2-1][vertex1-1] = 1  # For undirected graph

    return adjacency_matrix

directed_graph = create_directed_graph(vertices, edges)
adjacency_matrix = create_adjacency_matrix(vertices, edges)

print("Directed Graph:", directed_graph)
print("Adjacency Matrix:\n", adjacency_matrix)

"""<font color ='blue'> Itrative PageRank Algorithm Implementation """

def page_rank(graph, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
    nodes = graph.keys()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}

    min_value = (1.0-damping_factor) / graph_size  # value for nodes without out links

    # initialize the page rank dict with 1/N for all nodes
    pagerank = dict.fromkeys(nodes, 1.0/graph_size)

    for i in range(max_iterations):
        diff = 0  # total difference compared to last iteration
        # for each node do the pagerank computation
        for node in nodes:
            rank = min_value
            for referring_page in graph[node]:
                rank += damping_factor * pagerank[referring_page] / len(graph[referring_page])

            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank

        # stop if PageRank has converged
        if diff < min_delta:
            break

    return pagerank

# Applying PageRank on the graph
pagerank = page_rank(graph)

# Printing the PageRank scores
for node, score in pagerank.items():
    print(f"Node {node} ({vertices[node]}): {score}")

"""<font color ='blue'>The above are the nodes, people, and corresponding scores.  """

def print_top_20_nodes(pagerank, vertices):

    sorted_nodes = sorted(pagerank.items(), key=lambda item: item[1], reverse=True) # Sorting the nodes by their PageRank scores in descending order
    top_20_nodes = sorted_nodes[:20] # Selecting the top 20 nodes

    # Printing names and PageRank scores of the top 20 nodes
    for node, score in top_20_nodes:
        print(f"Node {node} ({vertices[node]}): {score}")

"""<font color ='blue'> Final Result"""

print_top_20_nodes(pagerank, vertices)

"""#<font color = 'blue'>  **--------------------------THE END------------------------**"""