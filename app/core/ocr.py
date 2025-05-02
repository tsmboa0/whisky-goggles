import easyocr
import numpy as np
from app.utils.logger import logger

class OCREngine:
    """
    Optical Character Recognition engine using EasyOCR to extract text from images.
    """
    def __init__(self, languages=['en']):
        # Initialize the EasyOCR Reader with specified languages (default English).
        # We disable GPU for compatibility; set gpu=True for faster performance if available.
        self.reader = easyocr.Reader(languages, gpu=True)
    
    def extract_text(self, image):
        """
        Run OCR on the provided PIL image and return the extracted text (concatenated).
        """
        # Convert PIL image to numpy array as required by EasyOCR
        img_array = np.array(image.convert("RGB"))
        # Perform text detection and recognition
        results = self.reader.readtext(img_array)
        if not results:
            return ""
        # Concatenate all detected text pieces separated by space
        texts = [res[1] for res in results]  # each result is (bbox, text, confidence)
        logger.info("The OCR extracted text is: "," ".join(texts).strip())
        
        return " ".join(texts).strip()
