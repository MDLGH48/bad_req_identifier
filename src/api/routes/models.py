from typing import Any, List
from typing_extensions import Literal
from fastapi import Depends, APIRouter, Request, Path
from api import utils
from data import model_crud, types
from core import model_inference

router = APIRouter()


@router.post("/{api_collection}/create")
def create_model_collection(
    api_collection: str,
    model_collection: List[types.ModelSchema]
):

    api_collections = model_crud.operations.retrieve_all_collection_names()

    try:
        new_model_collection_list = model_crud.operations.create_collection(
            collection_name=api_collection,
            model=[m.dict() for m in model_collection])

        return new_model_collection_list

    except model_crud.CollectionExistsException:

        return utils.invalid_collection_response(
            collections=api_collections,
            mode="create")


@router.post("/{api_collection}/inference", response_model=types.ModelInferenceResponse)
async def identify_request(
    api_collection: str,
    target_request: dict
):
    if api_collection not in model_crud.operations.retrieve_all_collection_names():
        return utils.invalid_collection_response(
            collections=api_collections,
            mode="read")

    target_request_path = target_request["path"]

    model = model_crud.operations.retrieve_model(
        collection_name=api_collection,
        path=target_request_path)

    result = await model_inference.identify_abnormal_request(
        request=target_request,
        model=model)

    return {"path": target_request_path, **result}