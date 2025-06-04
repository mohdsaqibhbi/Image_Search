import torch
from globals import cfg
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

class ModelLoader:
    def __init__(self,):
        
        self.model = CLIPModel.from_pretrained(
            cfg.model.modelname).to(cfg.model.device)
        self.processor = CLIPProcessor.from_pretrained(cfg.model.modelname, use_fast=True)
        self.tokenizer = self.processor.tokenizer
        
    # def get_image_embedding(self, image_path):
        
    #     try:
    #         image = Image.open(image_path).convert("RGB")
    #         processor(images=image, return_tensors="pt").to(model.device)
    #         image = self.processor(image=image).unsqueeze(0).to(cfg.model.device)
            
    #         with torch.no_grad():
    #             embedding = self.model.encode_image(image).squeeze(0)
    #             embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    #             embedding = embedding.cpu()
            
    #         return embedding
        
    #     except Exception as e:
    #         print(f"[Warning] Could not process image {image_path}: {e}")
    #         return None
    
    def get_image_embedding(self, image_path):
        
        try:

            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt").to(cfg.model.device)
            
            with torch.no_grad():
                embedding = self.model.get_image_features(**inputs)
                embedding = embedding / embedding.norm(dim=-1, keepdim=True)  # Normalize
                embedding = embedding.squeeze(0).cpu()  # Remove batch dim and move to CPU

            return embedding

        except Exception as e:
            print(f"[Warning] Could not process image {image_path}: {e}")
            return None

    # def get_text_embedding(self, text_query):
        
    #     with torch.no_grad():
    #         tokenized = self.tokenizer([text_query]).to(cfg.model.device)
    #         text_embedding = self.model.encode_text(tokenized).squeeze(0)
    #         text_embedding = text_embedding / text_embedding.norm(dim=-1, keepdim=True)
    #         text_embedding = text_embedding.cpu()
        
    #     return text_embedding
    
    def get_text_embedding(self, text_query):
        
        try:

            tokenized = self.tokenizer([text_query], return_tensors="pt")
            tokenized = {k: v.to(cfg.model.device) for k, v in tokenized.items()}

            with torch.no_grad():
                text_embedding = self.model.get_text_features(**tokenized)
                text_embedding = text_embedding / text_embedding.norm(dim=-1, keepdim=True)
                text_embedding = text_embedding.squeeze(0).cpu()

            return text_embedding

        except Exception as e:
            print(f"[Warning] Could not process text '{text_query}': {e}")
            return None