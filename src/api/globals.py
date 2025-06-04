import os

from schema.config import AppConfig
from utils.logging import create_logger

APP_NAME = "ImageSearchAPI"
log = create_logger(application=APP_NAME)

api_version = "1.0"
api_root_path = "/api/imageSearch"
api_summary = "Image Search API"
api_description = """
Image Search API provides the capability to perform intelligent search across a collection of images using natural 
language queries.
The goal of the Image Search API is to retrieve the most relevant images that match the user's query.
The API offers search endpoint to support various image retrieval.
"""

cfg = AppConfig()

log.info_print(f"Starting {APP_NAME}")