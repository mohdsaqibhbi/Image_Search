import json
import os
from typing import Any
from pydantic import BaseModel

class ModelConfig(BaseModel):
    modelname: str
    device: str = "cpu"
    
class DataConfig(BaseModel):
    data_location: str
    
class DatabaseConfig(BaseModel):
    faiss_index_location: str
    image_mapping_location: str

class AppConfig(BaseModel):
    model: ModelConfig
    data: DataConfig
    database: DatabaseConfig

    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]) -> None:
        with open(os.path.join(os.getcwd(), "config.json"), "r") as f:
            config = json.load(f)
        super().__init__(*args, **{**kwargs, **config})