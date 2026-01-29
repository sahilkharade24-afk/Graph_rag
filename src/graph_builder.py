from neo4j import GraphDatabase
import networkx as nx

uri = "bolt://localhost:7687"
username = "neo4j"
password = "your_password"

driver = GraphDatabase.driver(uri, auth=(username, password))

def add_triple(s, r, o):
    with driver.session() as session:
        session.run(f"""
        MERGE (a:Entity {{name: '{s}'}})
        MERGE (b:Entity {{name: '{o}'}})
        MERGE (a)-[:{r.upper()}]->(b)
        """)

def build_graph(chunks, embeddings):
    """
    Builds a NetworkX graph from text chunks and their embeddings.
    Adds sequential edges between consecutive chunks.
    """
    G = nx.Graph()
    for i, chunk in enumerate(chunks):
        # Convert embedding to comma-separated string for compatible storage (matching app.py loading)
        emb_str = ",".join(map(str, embeddings[i]))
        G.add_node(str(i), chunk=chunk, embedding=emb_str)
    
    # Add sequential edges
    for i in range(len(chunks) - 1):
        G.add_edge(str(i), str(i+1))
        
    return G
