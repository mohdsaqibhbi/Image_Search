import os
from globals import cfg
from tqdm import tqdm

class ImageLoader:
    def __init__(self, model):

        self.embeddings = []
        
        print("Loading Images...")
        
        image_list = [os.path.join(cfg.data.data_location, image_name)
                    for image_name in os.listdir(cfg.data.data_location)]
        
        for idx, image_path in tqdm(enumerate(image_list), total=len(image_list)):
            
            emb = model.get_image_embedding(image_path)
            
            if emb is not None:
                self.embeddings.append({
                    "image_id": idx,
                    "image_path": image_path,
                    "embedding": emb
                })
                
        print("Images Loaded!")