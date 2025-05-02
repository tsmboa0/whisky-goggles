from pydantic import BaseModel, HttpUrl

class RecognitionRequest(BaseModel):
    """
    Request model for image URL input.
    """
    image_url: HttpUrl
