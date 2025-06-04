import faiss
import json
import torch
import numpy as np
from globals import cfg
from schema.data import ImageMatched, ImageMatchedData

class ImageSearchEngine:
    def __init__(self, model, database):
            
        self.model = model
        self.index = faiss.read_index(database.index_path)
        with open(database.image_map_path, "r") as f:
            self.image_map = json.load(f)

    def search(self, query: str, top_k: int = 5) -> ImageMatchedData:

        query_vector = self.model.get_text_embedding(query)
        if isinstance(query_vector, torch.Tensor):
            query_vector = query_vector.numpy()
            query_vector = query_vector.astype("float32")
            query_vector = np.expand_dims(query_vector, axis=0)
        
        faiss.normalize_L2(query_vector)

        D, I = self.index.search(query_vector, top_k)

        image_matched = []
        for score, idx in zip(D[0], I[0]):
            if str(idx) in self.image_map:
                item = self.image_map[str(idx)]
                image_matched.append(ImageMatched(
                    image_location=item["image_path"],
                    score=round(float(score), 3)
                ))

        image_matched_data = ImageMatchedData(
            query=query,
            image_matched=image_matched
        )

        return image_matched_data