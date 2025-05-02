import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from app.utils.metadata_loader import load_metadata

class WhiskyMatcher:
    """
    Handles similarity search over whisky bottle embeddings using a Faiss index.
    """
    def __init__(self):
        # define path to the iamge faiss index       
        index_path = "data/faiss_store/image_index.faiss"
        # Load the Faiss index from file (built with embeddings of known bottles)
        try:
            self.index = faiss.read_index(index_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load Faiss index from {index_path}: {e}")
        # Store reference metadata (list of dicts corresponding to index entries)
        self.metadata = load_metadata("data/metadata.csv")
    
    def match_image(self, embedding, top_k=3):
        """
        Find the top_k most similar bottle embeddings to the given embedding.
        Returns a list of metadata dicts for the best matches (including similarity score).
        """
        if embedding is None:
            return []
        # Ensure the query is a 2D array of type float32
        query = embedding.astype('float32').reshape(1, -1)
        # Use Faiss to search the index
        D, I = self.index.search(query, top_k)  # D = distances or scores, I = indices
        results = []
        for rank, idx in enumerate(I[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            item = self.metadata[idx]
            # Prepare match result with similarity score (for IndexFlatIP, D is the dot-product/cosine similarity)
            score = float(D[0][rank])
            result = {
                "id": item.get("id"),
                "name": item.get("name"),
                "region": item.get("region"),
                "fair_price":item.get("fair_price"),
                "shelf_price":item.get("shelf_price"),
                "avg_msrp":item.get("avg_msrp"),
                "abv": item.get("abv"),
                "image_url": item.get("image_url"),
                "confidence_score": score
            }
            results.append(result)
        return results
    
    def match_text(self, text):
        """
        This is used to perform similarity serach the mediator result using BM25
        """
        # Assume: list of 500 bottle metadata dictionaries
        metadata_list = self.metadata

        # Create corpus from bottle names
        corpus = [bottle["name"].lower().split() for bottle in metadata_list]

        # Initialize BM25
        bm25 = BM25Okapi(corpus)

        # Tokenize OCR text
        query_tokens = text.lower().split()

        # Get BM25 scores
        scores = bm25.get_scores(query_tokens)

        # Get best match index
        # best_match_index = int(np.argmax(scores))

        # Get the top 3 match
        top_indices = np.argsort(scores)[::-1][:3]
        top_matches = [metadata_list[i] for i in top_indices]

        return top_matches


