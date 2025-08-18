from models.request import ConversionRequest
from pydantic import BaseModel


class WorkflowOutput(BaseModel):
    data: ConversionRequest
    processing: bool
    finished: bool


class CompressionWorkflowOutput(BaseModel):
    data: ConversionRequest
    processing: bool
    finished: bool
    status: str


class CollateWorkflowOutput(BaseModel):
    data: ConversionRequest
    processing: bool
    finished: bool
    status: str


class ThumbnailsWorkflowOutput(BaseModel):
    data: ConversionRequest
    processing: bool
    finished: bool
    status: str
