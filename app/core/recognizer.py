from app.core.preprocessing import enhance_image
from app.core.embedding import EmbeddingEngine
from app.core.matcher import WhiskyMatcher
from app.core.vision import WhiskyVisionAnalyzer
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
        self.matcher = WhiskyMatcher()
        logger.info("Matching Engine loaded")
        self.vision_analyzer = WhiskyVisionAnalyzer()
        logger.info("Vision analyzer loaded")
        self.preprocess = enhance_image
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
        processed_image = self.preprocess(image)

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

        # Step 4: Vision – analyze the image with the Vision API
        print("Analyzing the image with the Vision API")
        vision_result = self.vision_analyzer.analyze(image)

        print(f"The Vision API results are: {vision_result}")

        # create an on object of the results
        result_data = {
            "clip_result":matches,
            "vision_result": vision_result
        }

        results.append(result_data)
        
        #Send the results to the mediator for verification
        print("Passing CLIP and OCR results to the AI mediator.")
        mediator_result = graph.invoke({
            "messages": [HumanMessage("Based on these results, which bottle is it?")],
            "vision_result": str(results[0]["vision_result"]),
            "clip_result": str(results[0]["clip_result"])
        })

        result = mediator_result['final_result']

        print(f"The result is: {result}")

        return result
