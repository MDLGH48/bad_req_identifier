from fastapi import responses
from typing_extensions import Literal


def invalid_collection_response(
        collections: list,
        mode: Literal["create", "read"]) -> responses.JSONResponse:

    response_error_mssg = {
        "create": "api collection already exists",
        "read": "api collection not found"
    }[mode]

    return responses.JSONResponse(
        status_code=422,
        content={
            "message": response_error_mssg,
            "available_collections": collections
        })
