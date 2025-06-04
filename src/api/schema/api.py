from typing import Optional
from pydantic import BaseModel, Field


class APIHealthCheckResponse(BaseModel):

    message: str = Field(
        ..., description="Health Check Message", examples=["API is Healthy"]
    )