import os
import argparse
import networkx as nx
import numpy as np
from src.pdf_loader import load_pdf
from src.chunker import chunk_text
from src.embeddings import generate_embeddings
from src.graph_builder import build_graph
from src.retriever import get_most_similar_indices
from src.generator import get_answer

def build():
    # 1. Get a list of PDF files from the data directory.
    data_dir = 'data'
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' not found.")
        return
    
    pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in {data_dir}")
        return

    # 2. Create an empty list to store all chunks.
    all_chunks = []

    # 3. Loop through each PDF file.
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        file_path = os.path.join(data_dir, pdf_file)
        # a. Load the PDF.
        text = load_pdf(file_path)
        # b. Chunk the text.
        chunks = chunk_text(text)
        # c. Add the chunks to the list of all chunks.
        all_chunks.extend(chunks)

    # 4. Generate embeddings for all chunks.
    print(f"Generating embeddings for {len(all_chunks)} chunks...")
    embeddings = generate_embeddings(all_chunks)

    # 5. Build the graph.
    print("Building graph...")
    graph = build_graph(all_chunks, embeddings)

    # 6. Save the graph to a file.
    print("Saving graph to graph.gexf...")
    nx.write_gexf(graph, "graph.gexf")

    print("Done.")

def query(query_text):
    # 1. Load the graph.
    if not os.path.exists("graph.gexf"):
        print("Error: graph.gexf not found. Please run 'build' first.")
        return

    print("Loading graph...")
    graph = nx.read_gexf("graph.gexf")
    
    # Extract chunks and embeddings
    nodes = []
    embeddings = []
    for node_id, data in graph.nodes(data=True):
        nodes.append(data['chunk'])
        embeddings.append([float(x) for x in data['embedding'].split(',')])

    embeddings = np.array(embeddings)

    # 2. Generate embedding for the query.
    print("Generating query embedding...")
    query_embedding = generate_embeddings([query_text])[0]

    # 3. Find relevant chunks using the retriever.
    print("Retrieving relevant context from graph...")
    indices, similarities = get_most_similar_indices(query_embedding, embeddings, k=5)
    
    context_chunks = [nodes[i] for i in indices]
    
    # 4. Include neighbors from the graph for more context
    expanded_context = set(context_chunks)
    for idx in indices:
        node_id = idx if idx in graph else str(idx)
        if node_id in graph:
            neighbors = list(graph.neighbors(node_id))
            for neighbor in neighbors:
                expanded_context.add(graph.nodes[neighbor]['chunk'])
    
    print(f"Retrieved {len(expanded_context)} relevant context pieces.")

    # 5. Generate answer using the LLM.
    print("Generating answer...")
    answer = get_answer(query_text, list(expanded_context))
    
    print("\n" + "="*50)
    print(f"QUERY: {query_text}")
    print("-" * 50)
    print(f"ANSWER:\n{answer}")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(description="Graph RAG")
    parser.add_argument("action", choices=["build", "query"], help="Action to perform")
    parser.add_argument("--query_text", help="Text to query")
    args = parser.parse_args()

    if args.action == "build":
        build()
    elif args.action == "query":
        if not args.query_text:
            print("Please provide a query with --query_text")
            return
        query(args.query_text)

if __name__ == '__main__':
    main()
