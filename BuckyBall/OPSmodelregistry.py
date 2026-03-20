# -*- coding: utf-8 -*-
"""
Concrete Class for Model Registry
Use for recording tags and metadata for various models.
Instantiated for OPENSEESPY models

@author: Dr Alessandro Tombari


"""
from abc_modelregistry import ModelRegistry


class OpsModelRegistry(ModelRegistry):
    def __init__(self):
        self.model_metadata: dict[str, dict[str, int]] = {}


    def add_model(self, model_name: str, model_metadata = None):
        metadata = dict(model_metadata or {})
        if model_name not in self.model_metadata:  
            if metadata is None:
                self.model_metadata[model_name] = {"tagMat": 1,
                        "tagEle": 1, 
                        "tagNode": 1}   
            else:
                    self.model_metadata[model_name] = metadata
        else:
            raise ValueError(f"Model '{model_name}' already exists in registry.")

    def get_model(self, model_name: str) -> dict:
        if model_name in self.model_metadata:
            return self.model_metadata[model_name]
        else:
            raise ValueError(f"Model '{model_name}' not found in registry.")

    
    def list_models(self) -> set:
        return set(self.model_metadata.keys())

    def delete_model(self, model_name: str):
        if model_name in self.model_metadata:
            del self.model_metadata[model_name]
        else:
            raise ValueError(f"Model '{model_name}' not found in registry.")  

    def update_model(self, model_name: str, model_metadata: dict):
        if model_name in self.model_metadata:
            self.model_metadata[model_name].update(model_metadata)
        else:
            raise ValueError(f"Model '{model_name}' not found in registry.")

    def get_up_tag(self, model_name: str, model_key: str) -> int:
            if model_key == "tagMat":
                if model_name in self.model_metadata:
                    tag = self.model_metadata[model_name].get("tagMat", None)
                    if tag is None:
                        raise ValueError(f"Model metadata 'tagMat' not found for model '{model_name}'.")
                    else: 
                        self.model_metadata[model_name]["tagMat"] += 1 
                        return tag
                else:
                    raise ValueError(f"Model '{model_name}' not found in registry.")
            elif model_key == "tagEle":
                if model_name in self.model_metadata:
                    tag = self.model_metadata[model_name].get("tagEle", None)
                    if tag is None:
                        raise ValueError(f"Model metadata 'tagEle' not found for model '{model_name}'.")    
                    else:
                        self.model_metadata[model_name]["tagEle"] += 1
                        return tag
                else:
                    raise ValueError(f"Model '{model_name}' not found in registry.")
            elif model_key == "tagNode":
                if model_name in self.model_metadata:
                    tag = self.model_metadata[model_name].get("tagNode", None)
                    if tag is None:
                        raise ValueError(f"Model metadata 'tagNode' not found for model '{model_name}'.")    
                    else:
                        self.model_metadata[model_name]["tagNode"] += 1
                        return tag
                else:
                    raise ValueError(f"Model '{model_name}' not found in registry.")
            else:
                raise ValueError(f"Model metadata '{model_key}' not found in registry.")

    def decrease_tags(self, model_name: str, model_key: str):
        if model_key == "tagMat":
            if model_name in self.model_metadata:
                if self.model_metadata[model_name]["tagMat"] > 1:
                    self.model_metadata[model_name]["tagMat"] -= 1
                else:
                    raise ValueError(f"Cannot decrease 'tagMat' below 1 for model '{model_name}'.")
        elif model_key == "tagEle":
            if model_name in self.model_metadata:
                if self.model_metadata[model_name]["tagEle"] > 1:
                    self.model_metadata[model_name]["tagEle"] -= 1
                else:
                    raise ValueError(f"Cannot decrease 'tagEle' below 1 for model '{model_name}'.")
        elif model_key == "tagNode":
            if model_name in self.model_metadata:
                if self.model_metadata[model_name]["tagNode"] > 1:
                    self.model_metadata[model_name]["tagNode"] -= 1
                else:
                    raise ValueError(f"Cannot decrease 'tagNode' below 1 for model '{model_name}'.")
        else:
            raise ValueError(f"Model metadata '{model_key}' not found in registry.")

    def clear_registry(self):
        self.model_metadata.clear()
    
