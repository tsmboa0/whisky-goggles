from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.core.recognizer import Recognizer
from app.models.request import RecognitionRequest
from app.models.response import RecognitionResponse
from app.utils.logger import logger
from PIL import Image
import requests

router = APIRouter()
# Initialize the recognizer pipeline (loads models, index, etc. once at startup)
recognizer = Recognizer()

@router.post("/recognize", response_model=RecognitionResponse)
async def recognize_whisky(file: UploadFile = File(...)):
    """
    Recognize whisky bottles from an uploaded image file.
    """
    logger.info("🚀 /Recognize endpoint hit.")

    if not file:
        raise HTTPException(status_code=400, detail="Image file is required.")
    # Read and open the image file
    try:
        from PIL import Image
        image = Image.open(file.file).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file.") from e
    # Run the recognition pipeline
    matches = recognizer.recognize(image)
    # Return the results as a JSON response
    return JSONResponse(content={"matches": matches})

@router.post("/recognize_url", response_model=RecognitionResponse) #response_model=RecognitionResponse
async def recognize_whisky_by_url(request: RecognitionRequest):
    """
    Recognize whisky bottles from an image URL.
    """
    logger.info("🚀 /Recognize_url endpoint hit.")
    
    if not request.image_url:
        raise HTTPException(status_code=400, detail="Image URL is required.")
    # Fetch the image from the URL
    try:
        response = requests.get(str(request.image_url))
        response.raise_for_status()
        image = Image.open(response.content if hasattr(response, 'content') else response.raw).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image: {e}")
    # Run the recognition pipeline
    matches = recognizer.recognize(image)
    return {"matches": matches}
