from enum import Enum
from pydantic import BaseModel, validator, Field
from typing import List, Optional, Union, Any
from typing_extensions import Literal
from enum import Enum


class FieldTypes(Enum):
    Int = int
    String = str
    Boolean = bool
    List = list
    Date = str  # regex-dd-mm-yyyy
    Email = str  # regex
    Auth_Token = str
    UUID = str  # regex


class ComponentSchema(BaseModel):
    name: str
    types: List[Union[Literal[
        tuple([k for k, v in FieldTypes.__members__.items()])]]]
    required: bool

    # could change to underscore all of these
    @validator("types", pre=True)
    def validate_auth_token_type(cls, v):
        if "Auth-Token" in v:
            return v[v.index("Auth-Token")].replace("-", "_")


class ModelSchema(BaseModel):
    path: str
    method: str
    query_params: List[Union[ComponentSchema, Any]]
    headers: List[Union[ComponentSchema, Any]]
    body: List[Union[ComponentSchema, Any]]


class RequestDetail(BaseModel):
    is_correct: bool
    request_value: Any


class ComponentReport(BaseModel):
    extra_fields: List[Any]
    missing_fields: List[Any]
    incorrect_types: List[Union[RequestDetail, Any]]


class ComponentModel(BaseModel):
    headers: ComponentReport
    query_params: ComponentReport
    body: ComponentReport


class ModelInferenceResponse(BaseModel):
    path: str
    method: RequestDetail
    components: ComponentModel

# using ANY to workaround annoying bug https://github.com/samuelcolvin/pydantic/issues/1624
