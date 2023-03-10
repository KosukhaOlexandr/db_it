# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class DatabaseCreatePost201Response(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    DatabaseCreatePost201Response - a model defined in OpenAPI

        database_name: The database_name of this DatabaseCreatePost201Response [Optional].
    """

    database_name: Optional[str] = Field(alias="database_name", default=None)

DatabaseCreatePost201Response.update_forward_refs()
