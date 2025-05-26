import faiss
import numpy as np
import pickle
from PIL import Image
from app.utils.metadata_loader import load_metadata
from rank_bm25 import BM25Okapi
import pandas as pd

class WhiskyMatcher:
    """
    Handles similarity search over whisky bottle embeddings using Faiss image index
    and a name map to return bottle identities directly.
    """
    def __init__(self):
        # Load FAISS image index
        image_index_path = "data/faiss_store/index.faiss"
        name_map_path = "data/faiss_store/bottle_names.pkl"
        metadata_path = "data/metadata.csv"
        
        try:
            self.image_index = faiss.read_index(image_index_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load FAISS image index: {e}")

        try:
            with open(name_map_path, "rb") as f:
                self.name_map = pickle.load(f)  # list of image names or IDs
        except Exception as e:
            raise RuntimeError(f"Failed to load image name map: {e}")
        try:
            self.metadata_map = self._load_metadata_as_dict(metadata_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load metadata CSV: {e}")
        
    def _load_metadata_as_dict(self, csv_path):
        df = pd.read_csv(csv_path)
        return {str(row["id"]): row.to_dict() for _, row in df.iterrows()}


    def match_image(self, embedding, top_k: int = 3):
        """
        Match the input image to known bottles using CLIP + FAISS.
        Returns a list of dicts: [{name, confidence_score}, ...]
        """
        if embedding is None:
            return []

        # Get normalized embedding
        embedding = embedding.astype('float32').reshape(1, -1)

        # Search FAISS index
        D, I = self.image_index.search(embedding, top_k)

        results = []
        for rank in range(top_k):
            idx = I[0][rank]
            score = D[0][rank]

            if 0 <= idx < len(self.name_map):
                bottle_id = self.name_map[idx]
                metadata = self.metadata_map.get(str(bottle_id))
                if metadata:
                    metadata["confidence_score"] = float(score)
                    results.append(metadata)

        return results

    
    def match_text(self, text):
        """
        This is used to perform similarity search the mediator result using BM25
        """
        # Assume: list of 500 bottle metadata dictionaries
        metadata_list = load_metadata("data/metadata.csv")

        # Create corpus from bottle names
        corpus = [bottle["name"].lower().split() for bottle in metadata_list]

        # Initialize BM25
        bm25 = BM25Okapi(corpus)

        # Tokenize OCR text
        query_tokens = text.lower().split()

        # Get BM25 scores
        scores = bm25.get_scores(query_tokens)

        # Get the top 3 match
        top_indices = np.argsort(scores)[::-1][:3]
        top_matches = [metadata_list[i] for i in top_indices]

        return top_matches


