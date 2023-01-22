import sys
import _thread
import math
import re
import collections
from timeit import default_timer as timer
from datetime import timedelta
import numpy as np

#|------------------------------ Main method ------------------------------|#

def main():
    # N = number of edges, M = number of edges, C = number of students to transfer, P = number of routes
    N, M, C, P, routes, remove_edges = read_data()
    source = min([int(route[0]) for route in routes])
    sink = max([int(route[1]) for route in routes])
    edges = [edge for edge in reversed(remove_edges)]

    # Turn routes into dictionary
    route_dict = {}
    for index, route in enumerate(routes):
        route_dict[index] = route 

    # Adding essential edges to graph
    minimal_routes = []
    for k, v in route_dict.items():
        if k not in remove_edges:
            minimal_routes.append(v)
    min_rts = minimal_routes
    minimal_routes = tuple(minimal_routes)

    ind = 0
    high = len(edges)
    maxflow = 0
    maxflow, min_rts, high = binary_search(edges, 0, high, C, N, minimal_routes, min_rts, route_dict, ind, source, sink, maxflow)

    # Bugfix
    if maxflow < C:
        min_rts.append(route_dict.get(edges[high]))
        network = get_network_matrix(N, min_rts)        
        maxflow = int(edmonds_karp(network, source, sink))
    
    print((len(routes)-len(min_rts)), maxflow, sep=' ')


#|------------------------------ Algorithm ------------------------------|#


def edmonds_karp(graph, source, sink):
    """Returns the maximum flow from source to sink in the given graph."""

    # This array is filled by BFS and to store path
    parent = [-1] * len(graph)

    max_flow = 0  # There is no flow initially

    # Augment the flow while there is path from source to sink
    while bfs(graph, source, sink, parent):

        # Find minimum residual capacity of the edges along the
        # path filled by BFS. Or we can say find the maximum flow
        # through the path found.
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        # Add path flow to overall flow
        max_flow += path_flow

        # Update residual capacities of the edges and reverse edges
        # along the path
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]

    return max_flow

def bfs(graph, s, t, parent):
    """Returns true if there is a path from source 's' to sink 't' in
    residual graph. Also fills parent[] to store the path."""

    # Mark all the vertices as not visited
    visited = [False] * len(graph)

    # Create a queue for BFS
    queue = collections.deque()

    # Mark the source node as visited and enqueue it
    queue.append(s)
    visited[s] = True

    # BFS loop starts here
    while queue:
        u = queue.popleft()

        # Find all adjacent vertices to u where there is non zero capacity
        # queue the found vertices, mark as true and set u as parent
        for i, val in enumerate(graph[u]):
            if (visited[i] == False) and (val > 0):
                queue.append(i)
                visited[i] = True
                parent[i] = u

    return visited[t]



#|------------------------------ Complementary functions ------------------------------|#

def read_data(data = sys.stdin.readlines()):
    N = int(data[0].split()[0])
    M = int(data[0].split()[1])
    C = int(data[0].split()[2])
    P = int(data[0].split()[3])

    # Get all the routes as a list
    routes = []
    for i in range(1, M+1):
        d = data[i].split()
        routes.append([d[0], d[1], d[2]])
 
    # List of edges to remove
    remove_edges = [int(i.split()[0]) for i in data[M+1:]]

    return N, M, C, P, routes, remove_edges


def get_network_matrix(N, routes):
    matrix = np.empty((N, N))#.fill(np.nan)
    matrix[:] = np.NaN
    for route in routes:
        matrix[int(route[0]), int(route[1])] = int(route[2])
        matrix[int(route[1]), int(route[0])] = int(route[2])
    return matrix

def binary_search(edges, low, high, C, N, minimal_routes, min_rts, route_dict, ind, source, sink, maxflow):
    # Base case 
    if high == low:
        return maxflow, min_rts, high

    mid = (high + low) // 2

    # Initiate min_rts with the essential routes
    min_rts = [el for el in minimal_routes]     # Det här blir otroligt ineffektivt, men måste uppdatera utan att minimal_routes ändras

    for i in range(0, mid+1):
        min_rts.append(route_dict.get(edges[i]))
    network = get_network_matrix(N, min_rts)                 
    maxflow = int(edmonds_karp(network, source, sink))
 
    if maxflow < C:
        return binary_search(edges, mid + 1, high, C, N, minimal_routes, min_rts, route_dict, ind, source, sink, maxflow)
 
    else:
        return binary_search(edges, low, mid, C, N, minimal_routes, min_rts, route_dict, ind, source, sink, maxflow)      


if __name__ == '__main__':
    main()
