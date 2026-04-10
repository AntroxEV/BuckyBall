# -*- coding: utf-8 -*-
"""
Abstract Class for Model Registry
Use for recording tags and metadata for various models.

@author: Dr Alessandro Tombari


"""

from abc import ABC, abstractmethod
from collections.abc import Mapping


class ModelRegistry(ABC):

    @abstractmethod
    def add_model(self, model_name: str, model_metadata: Mapping | None = None):
        """
        Add a model to the registry.

        :param model_name: The name of the model.
        :param model_metadata: A dictionary containing metadata about the model.
        """
        pass

    @abstractmethod
    def get_model(self, model_name: str) -> dict:
        """
        Retrieve a model from the registry.

        :param model_name: The name of the model.
        :return: A dictionary containing metadata about the model.
        """
        pass

    @abstractmethod
    def list_models(self) -> set:
        """
        List all models in the registry.

        :return: A set of model names.
        """
        pass
    @abstractmethod
    def delete_model(self, model_name: str):
        """
        Delete a model from the registry.

        :param model_name: The name of the model to delete.
        """
        pass
    @abstractmethod
    def update_model(self, model_name: str, model_metadata: dict):
        """
        Update the metadata of a model in the registry.

        :param model_name: The name of the model to update.
        :param model_metadata: A dictionary containing the updated metadata about the model.
        """
        pass
    @abstractmethod
    def get_up_tag(self, model_name: str, model_key: str) -> int:
        """
        Retrieve a tag associated with a model and increase it.

        :param model_name: The name of the model.
        :param model_key: The key of the tag to increase.

        :return: The current value of the tag.
        """
        pass
    @abstractmethod
    def decrease_tags(self, model_name: str, model_key: str):
        """
        Decrease the tags associated with a model.

        :param model_name: The name of the model.
        :param model_key: The key of the tag to decrease.
        """
        pass
    @abstractmethod
    def reset_registry(self):
        """
        Reset the registry to its initial state.
        """
        pass

