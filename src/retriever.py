import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity

class Retriever:
    def __init__(self, embeddings):
        self.embeddings = np.array(embeddings)
        self.nn = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.nn.fit(self.embeddings)

    def retrieve(self, query_embedding, k=5):
        """
        Retrieves the top k most similar nodes.
        """
        distances, indices = self.nn.kneighbors([query_embedding], n_neighbors=k)
        return indices[0], 1 - distances[0] # Return indices and similarities

def get_most_similar_indices(query_embedding, embeddings, k=5):
    retriever = Retriever(embeddings)
    return retriever.retrieve(query_embedding, k)
