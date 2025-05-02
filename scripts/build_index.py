import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PIL import Image
import numpy as np
import faiss
import pandas as pd

from app.core.embedding import EmbeddingEngine
from app.utils import metadata_loader
import torch
torch.set_num_threads(1)  # Limit PyTorch to 1 thread


def build_index():
    print("Starting...")
    # Load metadata to get list of all items
    image_index_path = os.path.join(os.path.dirname(__file__), '../data/faiss_store/image_index.faiss')
    text_index_path = os.path.join(os.path.dirname(__file__), '../data/faiss_store/text_index.faiss')
    image_dir=os.path.join(os.path.dirname(__file__), '../data/bottle_images')
    metadata_path = os.path.join(os.path.dirname(__file__), '../data/metadata.csv')

    metadata = metadata_loader.load_metadata(metadata_path)
    print("Loaded metadata")
    embedder = EmbeddingEngine()
    print("Embedder Initd")

    d = None
    image_embeddings = []
    bottle_name = []
    # Optional: initialize background removal session to preprocess all images
    rembg_session = None
    try:
        from rembg import new_session, remove
        rembg_session = new_session()
    except ImportError:
        remove = None
    print("Entering Loop")
    for item in metadata:
        # Get the image path from the metadata
        print("iterating over image: ",item['id'],".jpg")
        image_path = os.path.join(image_dir, f"{item['id']}.jpg") # images are named with id.jpg

        #Extract the bottle names from the metadata
        bottle_name.append(item['name'])

        if not os.path.exists(image_path):
            print(f"Warning: Image for ID {item['id']} not found at {image_path}. Skipping.")
            continue
        
        # Open the image
        try:
            img = Image.open(image_path)
        except Exception as e:
            print(f"Error opening image for ID {item['id']}: {e}. Skipping.")
            continue
        
        img = img.convert("RGB")  # Ensure image is in RGB mode
        # Get embedding for the image
        vec = embedder.embed_image(img)
        if d is None:
            d = vec.shape[0]
        image_embeddings.append(vec)

    if not image_embeddings:
        print("No embeddings were generated. Index not built.")
        return
    print("Loop done...packaging the embeddings")

    image_embeddings = np.array(image_embeddings, dtype='float32')

    #Generate the text embeddings for the bottle list
    text_embeddings = embedder.embed_text(bottle_name)
    
    # Build an Image Faiss index (Inner Product for cosine similarity on normalized vectors)
    image_index = faiss.IndexFlatIP(d)  # Using Inner Product for cosine similarity
    image_index.add(image_embeddings)         # Add vectors to the index

    #Build a text Faiss index
    text_dimention = text_embeddings.shape[1]
    text_index = faiss.IndexFlatL2(text_dimention)
    text_index.add(text_embeddings)
    
    # Save the Image and Text Faiss index to their specified path
    faiss.write_index(image_index, image_index_path)
    faiss.write_index(text_index, text_index_path)

    print(f"Saved Image Faiss index to {image_index_path} (entries: {image_index.ntotal}).")
    print(f"Saved Text Faiss index to {text_index_path} (entries: {text_index.ntotal}).")

if __name__ == "__main__":
    build_index()
