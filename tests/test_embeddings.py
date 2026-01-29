import unittest
import numpy as np
from src.embeddings import generate_embeddings

class TestEmbeddings(unittest.TestCase):
    def test_generate_embeddings(self):
        chunks = ["This is the first sentence.", "This is the second sentence."]
        embeddings = generate_embeddings(chunks)
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(embeddings[0].shape, (384,))
        self.assertEqual(embeddings[1].shape, (384,))
        # Check that the embeddings are not all zeros
        self.assertFalse(np.all(embeddings[0] == 0))
        self.assertFalse(np.all(embeddings[1] == 0))

if __name__ == '__main__':
    unittest.main()
