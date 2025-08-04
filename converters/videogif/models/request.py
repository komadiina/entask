from pydantic import BaseModel
from typing import Optional


class ConversionRequest(BaseModel):
    compression_ratio: Optional[float]
    video_url: str
