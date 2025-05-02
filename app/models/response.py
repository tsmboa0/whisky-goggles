from pydantic import BaseModel
from typing import List, Optional

class BottleMatch(BaseModel):
    id: int
    name: str
    region: Optional[str]
    abv: float
    image_url: str
    avg_msrp: Optional[float]
    fair_price: float
    shelf_price: float
    confidence_score: Optional[float]

class RecognitionResponse(BaseModel):
    matches: List[BottleMatch]
