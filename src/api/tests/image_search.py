import time
from interfaces.services import get_search_images
from schema.data import ImageMatchedResponse

if __name__ == "__main__":
    
    start = time.time()
    
    query = "desert"
    image_matched_data = get_search_images(query)
    
    message = "Image Search Completed"
    inference_time = round(time.time() - start, 3)
    
    image_matched_response = ImageMatchedResponse(
        data=image_matched_data,
        respTime=inference_time,
        message=message,
    )
    
    print("Response:")
    print(image_matched_response.json())
    print("Done")