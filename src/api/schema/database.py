import faiss
import json
import torch
import numpy as np
from globals import cfg
class FAISSDatabase:
    def __init__(self, embeddings):
        
        self.embeddings = embeddings
        self.index_path = cfg.database.faiss_index_location
        self.image_map_path = cfg.database.image_mapping_location
        self.image_vectors = []
        self.image_map = {}
        
        self.load_database()
        
    def load_database(self):

        for idx, item in enumerate(self.embeddings):
            vector = item["embedding"]
            
            if isinstance(vector, torch.Tensor):
                vector = vector.numpy()
                vector = vector.astype("float32")
            
            self.image_vectors.append(vector)

            self.image_map[idx] = {
                "image_id": item["image_id"],
                "image_path": item["image_path"]
            }

        self.image_vectors = np.stack(self.image_vectors)
        faiss.normalize_L2(self.image_vectors)
        d = self.image_vectors.shape[1]
        index = faiss.IndexFlatIP(d)
        index.add(self.image_vectors)
        faiss.write_index(index, self.index_path)
        
        with open(self.image_map_path, "w") as f:
            json.dump(self.image_map, f, indent=2)