# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from enum import Enum
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class ColumnType(str, Enum):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ColumnType - a model defined in OpenAPI

    """
    INTEGER = "int"
    STRING = "str"
    CHAR = "char"
    REAL = "float"
    COMPLEX = "complex"

#ColumnType.update_forward_refs()
