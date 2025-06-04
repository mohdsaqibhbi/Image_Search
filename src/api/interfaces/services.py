from schema.data import ImageMatchedData
from schema.database import FAISSDatabase
from services.load_model import ModelLoader
from services.load_data import ImageLoader
from services.inference import ImageSearchEngine

model = ModelLoader()
image_loader = ImageLoader(model)
database = FAISSDatabase(image_loader.embeddings)
search_engine = ImageSearchEngine(model, database)

def get_search_images(query: str) -> ImageMatchedData:

    image_matched_data = search_engine.search(query)
    return image_matched_data

async def get_search_images_async(query: str) -> ImageMatchedData:

    image_matched_data = search_engine.search(query)
    return image_matched_data