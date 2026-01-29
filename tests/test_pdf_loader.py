import unittest
import os
from src.pdf_loader import load_pdf

class TestPdfLoader(unittest.TestCase):
    def test_load_pdf(self):
        # Path to the test PDF file
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Simple Steps to Option Trading Success.pdf')

        # Load the PDF
        text = load_pdf(file_path)

        # Check that the text is not empty
        self.assertTrue(len(text) > 0)

if __name__ == '__main__':
    unittest.main()
