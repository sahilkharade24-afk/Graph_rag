import unittest
from src.chunker import chunk_text

class TestChunker(unittest.TestCase):
    def test_chunk_text(self):
        text = "This is the first sentence.\nThis is the second sentence.\n\nThis is the third sentence."
        chunks = chunk_text(text)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0], "This is the first sentence.")
        self.assertEqual(chunks[1], "This is the second sentence.")
        self.assertEqual(chunks[2], "This is the third sentence.")

if __name__ == '__main__':
    unittest.main()

