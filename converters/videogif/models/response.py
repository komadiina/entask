from pydantic import BaseModel
from typing import Optional


class ConversionResponse(BaseModel):
    loss_factor: float = 1
    download_url: str
