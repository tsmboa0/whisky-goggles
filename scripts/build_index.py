import os
import sys
import numpy as np
import faiss
import pickle
from PIL import Image
import torch

# Ensure relative import for app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.embedding import EmbeddingEngine

torch.set_num_threads(1)

def build_index():
    print("Starting index build...")
    
    image_dir = os.path.join(os.path.dirname(__file__), '../data/new_bottle_images')
    index_path = os.path.join(os.path.dirname(__file__), '../data/faiss_store/index.faiss')
    name_map_path = os.path.join(os.path.dirname(__file__), '../data/faiss_store/bottle_names.pkl')

    print(f"loading embedding engine")
    embedder = EmbeddingEngine()
    print("Embedding engine loaded")
    image_embeddings = []
    image_names = []

    print("Loading images from:", image_dir)
    count = 0
    
    print(f"The directory length is: {len(os.listdir(image_dir))}")
    for file in sorted(os.listdir(image_dir)):
        if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        image_path = os.path.join(image_dir, file)
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            print(f"Error opening {file}: {e}")
            continue
        
        print(f"Embedding {file}")
        vec = embedder.embed_image(image)
        image_embeddings.append(vec)
        image_names.append(os.path.splitext(file)[0])  # strip file extension
        count += 1
        print(f"The count is: {count}")
        

    if not image_embeddings:
        print("No images processed. Aborting.")
        return

    print("Building FAISS index...")
    image_embeddings = np.array(image_embeddings, dtype='float32')
    dim = image_embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)  # cosine similarity requires normalized vectors
    index.add(image_embeddings)

    print(f"Saving FAISS index to {index_path}")
    faiss.write_index(index, index_path)

    print(f"Saving name map to {name_map_path}")
    with open(name_map_path, 'wb') as f:
        pickle.dump(image_names, f)

    print("Indexing complete. Total images indexed:", len(image_names))

if __name__ == "__main__":
    build_index()
