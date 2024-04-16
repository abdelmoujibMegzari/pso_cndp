import random
from collections import deque
from copy import deepcopy


class Graph:
    """
    This class represents a Graph object. It can be initialized with a specified number of nodes or by reading from a file.
    The graph is represented using an adjacency list, using a dictionnary where keys are nodes and values are sets of adjacent nodes.
    """

    def __init__(self, number_of_nodes=0, file=None, adjacency_list=None):
        """
        Initializes the graph. If a file is provided, it reads the graph from the file.
        Otherwise, it creates an empty graph with the specified number of nodes.
        The adjacency list can also be passed directly as a dictionary.

        :param number_of_nodes: The number of nodes in the graph
        :type number_of_nodes: int
        :param file: The file to read the graph from
        :type file: str
        :param adjacency_list: The adjacency list of the graph
        :type adjacency_list: dict
        """
        self.pairwise = -1
        if number_of_nodes < 0:
            raise ValueError("The number of nodes must be positive.")
        self.adjacency_list = {}
        if file:
            with open(file, "r") as f:
                number_of_nodes = int(f.readline())
                self.number_of_nodes = number_of_nodes
                for _ in range(number_of_nodes):
                    line = f.readline()
                    node, neighbors = line.split(":")
                    self.adjacency_list[int(node)] = set(map(int, neighbors.split()))
        else:
            self.number_of_nodes = number_of_nodes
            if adjacency_list is None:
                for i in range(number_of_nodes):
                    self.adjacency_list[i] = set()
            else:
                self.adjacency_list = adjacency_list

    def add_edge(self, vertex1, vertex2):
        """
        Add an edge between vertex1 and vertex2.

        :param vertex1: one vertex of the edge
        :type vertex1: int
        :param vertex2: the other vertex of the edge
        :type vertex2: int
        """
        self.adjacency_list[vertex1].add(vertex2)
        self.adjacency_list[vertex2].add(vertex1)
        self.pairwise = -1

    def delete_nodes(self, deleted_nodes):
        """
        Delete a set of nodes from the graph.

        :param deleted_nodes: set of nodes to be deleted
        :type deleted_nodes: set
        """
        deleted_nodes = set(deleted_nodes)
        for node in self.adjacency_list:
            self.adjacency_list[node] -= deleted_nodes
        for deleted_node in deleted_nodes:
            if deleted_node in self.adjacency_list:
                self.adjacency_list.pop(deleted_node)
        self.number_of_nodes -= len(deleted_nodes)
        self.pairwise = -1

    def clone_graph(self):
        """
        Create a deep copy of the graph.

        :return: a deep copy of the graph
        :rtype: Graph
        """
        return Graph(self.number_of_nodes, adjacency_list=deepcopy(self.adjacency_list))

    def pairwise_connectivity(self):
        """
        Calculate the pairwise connectivity of the graph.

        :return: the pairwise connectivity of the graph
        :rtype: int
        """
        pairwise_connectivity = 0  # Counter for the number of connected pairs of nodes
        visited = set()  # Set to keep track of visited nodes
        for start_node in self.adjacency_list.keys():
            if start_node in visited:
                continue
            connected_component_node_count = 1
            queue = deque()
            queue.append(start_node)
            visited.add(start_node)
            while queue:
                node = queue.popleft()
                for neighbor in self.adjacency_list[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        connected_component_node_count += 1
            pairwise_connectivity += (
                connected_component_node_count
                * (connected_component_node_count - 1)
                // 2
            )
        return pairwise_connectivity

    def vertex_cover(self):
        """
        Return a vertex cover of the graph.

        :return: a vertex cover of the graph
        :rtype: tuple
        """
        remaining = set(self.adjacency_list.keys())
        deleted = set()
        kept = set()
        while remaining:
            starting_vertex = random.sample(sorted(remaining), 1)[0]
            kept.add(starting_vertex)
            deleted.update(self.adjacency_list[starting_vertex])
            remaining -= deleted | kept
        return kept, deleted
