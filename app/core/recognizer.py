from app.core import preprocessing
from app.core.embedding import EmbeddingEngine
from app.core.ocr import OCREngine
from app.core.matcher import WhiskyMatcher
from app.utils import metadata_loader
from app.core.mediator import graph
from langchain_core.messages import HumanMessage
from app.utils.logger import logger

class Recognizer:
    """
    High-level recognizer that uses preprocessing, embedding, OCR, and matcher 
    to identify whisky bottles in an image.
    """
    def __init__(self):
        # Initialize core components: image embedder, text reader, and matcher
        self.embedder = EmbeddingEngine()
        logger.info("Clip embedder loaded")
        self.ocr_engine = OCREngine()
        logger.info("OCR engine loaded")
        self.matcher = WhiskyMatcher()
        logger.info("Matching Engine loaded")
        # Prepare background removal session (to speed up multiple calls)
        try:
            from rembg import new_session
            self.rembg_session = new_session()  # uses default model (u2net)
        except ImportError:
            self.rembg_session = None

    def recognize(self, image):
        """
        Process the input image (which may contain multiple bottles) and return 
        a list of identified whisky bottles with their details.
        """
        # Step 1: Preprocessing – remove background and split into bottle crops
        print("strting recognizer step1: Preprocess")
        # bottle_images = preprocessing.preprocess_image(image, session=self.rembg_session)

        results = []

        # Step 2: Embedding – obtain CLIP feature vector for the bottle image
        if image.mode != "RGB":
            image = image.convert("RGB")

        print("Embedding the image")
        embedding = self.embedder.embed_image(image)

        # Step 3: Matching – query the FAISS index for similar embeddings
        print("Matching the image")
        matches = self.matcher.match_image(embedding, top_k=3)

        if not matches:
            print("No match found!")
            matches=[]

        # Step 4: OCR – read text from the bottle label (if any)
        print("running OCR on uploaded image")
        label_text = self.ocr_engine.extract_text(image)

        # create an on object of the results
        result_data = {
            "clip_result":matches,
            "ocr_result": label_text
        }

        results.append(result_data)
        
        #Send the results to the mediator for verification
        print("Passing CLIP and OCR results to the AI mediator.")
        mediator_result = graph.invoke({
            "messages": [HumanMessage("Based on these results, which bottle is it?")],
            "ocr_result": str(results[0]["ocr_result"]),
            "clip_result": str(results[0]["clip_result"])
        })

        result = mediator_result['final_result']

        print(f"The result is: {result}")

        return result
