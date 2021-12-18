import os
import glob
import json
from core.config import settings
from typing import List
from typing_extensions import Literal
from fastapi import Path


class CollectionExistsException(Exception):
    pass


class ModelCRUD:
    # could inherit parent class based on mode --> class FileCRUD | class DbCRUD
    def __init__(self):
        self.DB_MODE = settings.DATA_STORAGE_MODE == "db_storage"
        self.BASE_DIR = "src/data/static/"
        self.model_io = lambda collection_name, fmode: open(
            f"src/data/static/{collection_name}/models.json", fmode)

    @property
    def db_mode(self):
        if self.DB_MODE:
            # just a todo
            raise NotImplementedError(
                "database functionality is not implemented yet")
        else:
            return False

    def create_collection(self, collection_name: str, model: List[dict]) -> list:
        '''
        @param collection_name: (str): new index name where collection of models should be stored (locally creates dir | db creates collection/idx--> not implemeneted) 
        @param model: (List[dict]): the collection of paths and their models
        '''
        if self.db_mode:
            pass
        else:
            try:
                os.mkdir(f"{self.BASE_DIR}/{collection_name}")
                json.dump(model, self.model_io(collection_name, "w"))
                return self.retrieve_all_collection_names()

            except FileExistsError:
                raise CollectionExistsException

    def retrieve_all_collection_names(self) -> list:
        '''
        returns list of all model collection names
        '''
        if self.db_mode:
            pass
        else:
            collection_names = [name.split("/")[-1]
                                for name in glob.glob("src/data/static/*")]
            return collection_names

    def retrieve_model(self, collection_name: str, path: str = None) -> dict:
        '''
        @param collection_name: (str): index name of the model collections to retrieve 
        @param path: (str): the api path of the relevant model to retrieve
        '''
        if self.db_mode:
            pass
        else:

            model_collection = json.load(self.model_io(collection_name, "r"))
            if not path:
                return model_collection
            else:
                return [model for model in model_collection if model["path"] == path][0]

    def update_collection(self, collection_name: str, model: dict) -> dict:
        raise NotImplementedError("update functionality does not exists")

    def update_model(self, collection_name: str, model: dict) -> dict:
        raise NotImplementedError("update functionality does not exists")

    def delete_collection(collection_name: str) -> list:
        raise NotImplementedError("delete functionality does not exists")

    def delete_model(collection_name: str, path: str) -> list:
        raise NotImplementedError("delete functionality does not exists")


operations = ModelCRUD()
