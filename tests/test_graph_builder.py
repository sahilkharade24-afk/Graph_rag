import unittest
import numpy as np
from src.graph_builder import build_graph

class TestGraphBuilder(unittest.TestCase):
    def test_build_graph(self):
        chunks = ["This is the first sentence.", "This is the second sentence.", "This is a completely different sentence."]
        embeddings = np.array([
            [1.0, 0.0, 0.0],
            [0.9, 0.1, 0.0], # Similar to the first sentence
            [0.0, 1.0, 0.0] # Different from the first two
        ])
        graph = build_graph(chunks, embeddings, threshold=0.8)

        # Check that the graph has the correct number of nodes
        self.assertEqual(graph.number_of_nodes(), 3)

        # Check that the nodes have the correct attributes
        self.assertEqual(graph.nodes[0]['chunk'], "This is the first sentence.")
        self.assertEqual(graph.nodes[1]['chunk'], "This is the second sentence.")
        self.assertEqual(graph.nodes[2]['chunk'], "This is a completely different sentence.")
        
        # Check that the embedding attribute is present and correct
        self.assertTrue('embedding' in graph.nodes[0])
        self.assertEqual(graph.nodes[0]['embedding'], '1.0,0.0,0.0')

        # Check that the graph has the correct number of edges
        self.assertEqual(graph.number_of_edges(), 1)

        # Check that the edge is between the correct nodes
        self.assertTrue(graph.has_edge(0, 1))

        # Check that the edge has the correct weight
        self.assertAlmostEqual(graph.edges[0, 1]['weight'], 0.9939, places=4)


if __name__ == '__main__':
    unittest.main()