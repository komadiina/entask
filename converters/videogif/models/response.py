from typing import Optional

from pydantic import BaseModel


class ConversionResponse(BaseModel):
    loss_factor: float = 1
    download_url: str
