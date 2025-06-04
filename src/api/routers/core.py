import time
from fastapi import APIRouter
from globals import api_root_path, log
from interfaces.services import get_search_images_async
from schema.data import ImageMatchedResponse

router = APIRouter()

@router.get(
    "/search",
    description="""
        Provides image search capability for given queries. Returns the most relevant images
        along with their scores based on the query.
    """,
)
async def search_images(query: str) -> ImageMatchedResponse:

    start = time.time()
    log.info_print("\n\nImage Search Request Received")

    image_matched_data = await get_search_images_async(query)

    message = "Image Search Completed"
    inference_time = round(time.time() - start, 3)
    log.info_print(
        f"Image Search API SUCCESS, Inference Time: {inference_time}",
        custom_dimensions={"method": f"{api_root_path}/search"},
    )

    return ImageMatchedResponse(
        data=image_matched_data,
        respTime=inference_time,
        message=message,
    )