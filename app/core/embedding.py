import torch
import numpy as np
from transformers import CLIPModel, CLIPProcessor
from sentence_transformers import SentenceTransformer



class EmbeddingEngine:
    """
    Uses a pre-trained CLIP model to generate embeddings for images.
    """
    def __init__(self, image_model_name="openai/clip-vit-base-patch32", text_model_name="all-MiniLM-L6-v2", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load CLIP model and image processor
        self.image_model = CLIPModel.from_pretrained(image_model_name)
        self.image_processor = CLIPProcessor.from_pretrained(image_model_name, use_fast=True)

        # Load Sentence Transformer for text embedding
        self.text_model = SentenceTransformer(text_model_name)  # Small + fast model

        # Move model to the specified device (CPU or GPU)
        self.image_model.to(self.device)
        self.image_model.eval()  # set to evaluation mode (not strictly necessary for Transformers)
    
    def embed_image(self, image):
        """
        Compute the CLIP embedding vector for a PIL image. Returns a 1D numpy array.
        """
        # Preprocess the image using CLIP's processor (includes resizing, normalization, etc.)
        inputs = self.image_processor(images=image, return_tensors="pt")
        pixel_values = inputs["pixel_values"].to(self.device)
        with torch.no_grad():
            image_features = self.image_model.get_image_features(pixel_values=pixel_values)  # :contentReference[oaicite:3]{index=3}
        # Convert to numpy and normalize the vector to unit length
        vector = image_features[0].cpu().numpy().astype('float32')
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
        return vector
    
    def embed_text(self, texts):
        """
        Compute the text embedding vector for bottle names. Returns a 1D numpy array
        """
        text_embeddings = self.text_model.encode(texts, show_progress_bar=True)

        return text_embeddings
