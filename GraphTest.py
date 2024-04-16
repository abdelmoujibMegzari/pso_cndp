import unittest

from Graph import Graph


class TestGraph(unittest.TestCase):
    """
    Test cases for the Graph class.
    """

    def setUp(self):
        """
        Code to be executed before each test method.
        """
        # Create a graph with 5 nodes and add edges
        self.graph = Graph(5)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(3, 4)

    def test_add_edge(self):
        """
        Test adding edges to the graph.
        """
        self.assertEqual(
            self.graph.adjacency_list, {0: {1}, 1: {0, 2}, 2: {1, 3}, 3: {2, 4}, 4: {3}}
        )

    def test_delete_nodes(self):
        """
        Test deleting nodes from the graph.
        """
        # Delete multiple elements
        self.graph.delete_nodes({1, 2})
        self.assertEqual(self.graph.adjacency_list, {0: set(), 3: {4}, 4: {3}})
        self.assertEqual(self.graph.number_of_nodes, 3)
        # Delete single element
        self.graph.delete_nodes({4})
        self.assertEqual(self.graph.adjacency_list, {0: set(), 3: set()})
        # Delete twice
        self.graph.delete_nodes({4})
        self.assertEqual(self.graph.adjacency_list, {0: set(), 3: set()})

    def test_clone_graph(self):
        """
        Test cloning the graph.
        """
        g2 = self.graph.clone_graph()
        self.assertEqual(g2.adjacency_list, self.graph.adjacency_list)
        self.assertEqual(g2.number_of_nodes, self.graph.number_of_nodes)

    def test_pairwise_connectivity(self):
        """
        Test calculating pairwise connectivity.
        """
        self.assertEqual(self.graph.pairwise_connectivity(), 10)
        self.graph.delete_nodes({1})
        self.assertEqual(self.graph.pairwise_connectivity(), 3)
        self.graph.delete_nodes({2})
        self.assertEqual(self.graph.pairwise_connectivity(), 1)

        # Test pairwise connectivity with no edges

        empty_graph = Graph(3)
        self.assertEqual(empty_graph.pairwise_connectivity(), 0)

        # Test pairwise connectivity with only one node

        single_node_graph = Graph(1)
        self.assertEqual(single_node_graph.pairwise_connectivity(), 0)

        # Test pairwise connectivity with all nodes connected

        complete_graph = Graph(4)
        complete_graph.add_edge(0, 1)
        complete_graph.add_edge(0, 2)
        complete_graph.add_edge(0, 3)
        complete_graph.add_edge(1, 2)
        complete_graph.add_edge(1, 3)
        complete_graph.add_edge(2, 3)
        self.assertEqual(complete_graph.pairwise_connectivity(), 6)

    def test_vertex_cover(self):
        """
        Test finding a vertex cover of the graph.
        """
        kept, deleted = self.graph.vertex_cover()
        self.assertEqual(len(kept) + len(deleted), self.graph.number_of_nodes)
        self.assertNotEqual(len(kept), 0)
        self.graph.delete_nodes(deleted)
        for node in self.graph.adjacency_list:
            self.assertEqual(self.graph.adjacency_list[node], set())

        # Test vertex cover with no edges

        empty_graph = Graph(3)
        kept, deleted = empty_graph.vertex_cover()
        self.assertEqual(len(deleted), 0)
        self.assertEqual(len(kept), 3)

        # Test vertex cover with only one node

        single_node_graph = Graph(1)
        kept, deleted = single_node_graph.vertex_cover()
        self.assertEqual(len(deleted), 0)
        self.assertEqual(len(kept), 1)

        # Test vertex cover with all nodes connected

        complete_graph = Graph(4)
        complete_graph.add_edge(0, 1)
        complete_graph.add_edge(0, 2)
        complete_graph.add_edge(0, 3)
        complete_graph.add_edge(1, 2)
        complete_graph.add_edge(1, 3)
        complete_graph.add_edge(2, 3)
        kept, deleted = complete_graph.vertex_cover()
        self.assertEqual(len(deleted), 3)
        self.assertEqual(len(kept), 1)

    def test_invalid_input(self):
        """
        Test behavior with invalid inputs.
        """

        # Test negative number of nodes

        with self.assertRaises(ValueError):
            Graph(-5)

        # Test non-existent nodes

        with self.assertRaises(KeyError):
            self.graph.add_edge(0, 6)

        # Test incorrect file format

        with self.assertRaises(FileNotFoundError):
            Graph(file="invalid_graph.txt")


if __name__ == "__main__":
    unittest.main()
