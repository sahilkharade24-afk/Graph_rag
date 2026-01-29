from pdf_loader import load_pdf
from chunker import chunk_text
from embeddings import generate_embeddings
from graph_builder import add_triple

text = load_pdf("data/book.pdf")
chunks = chunk_text(text)

vectors = generate_embeddings(chunks)

add_triple("Python", "is_a", "programming language")

print("✅ Graph RAG pipeline executed!")
