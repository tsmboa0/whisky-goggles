import io
from typing import Dict
from google.cloud import vision
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class WhiskyVisionAnalyzer:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def _image_to_bytes(self, image: Image.Image) -> bytes:
        buffer = io.BytesIO()
        image.convert("RGB").save(buffer, format="JPEG")
        return buffer.getvalue()

    def analyze(self, image: Image.Image) -> Dict:
        image_bytes = self._image_to_bytes(image)
        vision_image = vision.Image(content=image_bytes)

        features = [
            vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION),
            vision.Feature(type_=vision.Feature.Type.OBJECT_LOCALIZATION),
            vision.Feature(type_=vision.Feature.Type.IMAGE_PROPERTIES),
            vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION)
        ]

        response = self.client.annotate_image({"image": vision_image, "features": features})

        if response.error.message:
            raise RuntimeError(f"Vision API Error: {response.error.message}")

        # Extract OCR
        ocr_text = response.text_annotations[0].description.strip() if response.text_annotations else ""

        # Detect bottles
        bottles = [
            {
                "name": obj.name,
                "confidence": round(obj.score, 3),
                "position": {
                    "x": obj.bounding_poly.normalized_vertices[0].x,
                    "y": obj.bounding_poly.normalized_vertices[0].y,
                    "width": obj.bounding_poly.normalized_vertices[1].x - obj.bounding_poly.normalized_vertices[0].x,
                    "height": obj.bounding_poly.normalized_vertices[2].y - obj.bounding_poly.normalized_vertices[0].y
                }
            }
            for obj in response.localized_object_annotations
            if "bottle" in obj.name.lower() and obj.score >= 0.5
        ]

        # Dominant colors
        colors = []
        for c in response.image_properties_annotation.dominant_colors.colors:
            colors.append({
                "rgb": f"rgb({int(c.color.red)}, {int(c.color.green)}, {int(c.color.blue)})",
                "score": round(c.score, 3),
                "fraction": round(c.pixel_fraction, 3)
            })

        return {
            "type": "whisky_bottle_analysis",
            "bottle_count": len(bottles),
            "detected_bottles": bottles,
            "ocr_text": ocr_text,
            "dominant_colors": colors
        }
