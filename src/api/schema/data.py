from pydantic import BaseModel, Field

class ImageMatched(BaseModel):
    image_location: str
    score: float

class ImageMatchedData(BaseModel):
    query: str
    image_matched: list[ImageMatched] = Field(
        ..., description="List of images matched with their Scores."
    )

class ImageMatchedResponse(BaseModel):
    data: ImageMatchedData = Field(
        ...,
        description="Image Matched Data, containing the List of images matched with their Scores.",
    )
    respTime: float = Field(
        ..., description="Response Time in seconds.", examples=[1.332]
    )
    message: str = Field(
        ..., description="Response Message.", examples=["Image matched Completed"]
    )