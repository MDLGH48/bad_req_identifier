
import json
from typing_extensions import Literal
from pydantic import BaseModel
from data import types


def left_set_diff(left, right): return list(set(left).difference(set(right)))


def mutate_field(field_list: list, mode=Literal["request", "model"]) -> dict:
    if mode == "model":
        return {
            item["name"]: {
                "types": item["types"],
                "required": item["required"]
            } for item in field_list
        }

    elif mode == "request":
        return {
            item["name"]: item["value"] for item in field_list
        }


def check_component_fields(request_field: list, model_field: list):
    request_field = mutate_field(request_field, mode="request")
    model_field = mutate_field(model_field, mode="model")

    component_check = dict(
        extra_fields=left_set_diff(request_field.keys(), model_field.keys()),
        missing_fields=[]
    )
    type_mismatch_report = []
    for k, v in model_field.items():
        try:
            request_field_value = request_field[k]
            allowed_types = [
                types.FieldTypes[t.replace("-", "_")].value for t in v["types"]]

            if type(request_field_value) not in allowed_types:
                type_mismatch_report.append(
                    dict(
                        field_name=k,
                        request_value=request_field_value,
                        allowed=v["types"]
                    )
                )
        except KeyError:
            if v["required"]:
                component_check["missing_fields"].append(k)
            continue

    return {
        **component_check,
        "incorrect_types": type_mismatch_report
    }


async def identify_abnormal_request(request: dict, model: dict):
    method_check = dict(
        is_correct=False if request["method"] != model["method"] else True,
        request_value=request["method"]
    )
    component_report = dict(
        headers=check_component_fields(
            request["headers"], model["headers"]),
        query_params=check_component_fields(
            request["query_params"], model["query_params"]),
        body=check_component_fields(
            request["body"], model["body"]),
    )
    return {
        "method": method_check,
        "components": component_report
    }
