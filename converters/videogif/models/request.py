from typing import Optional

from pydantic import BaseModel


class ConversionRequest(BaseModel):
    compression_ratio: Optional[float]
    video_url: str
