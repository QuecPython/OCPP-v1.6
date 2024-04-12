# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :dataclasses.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2024-03-23 15:20:06
@copyright :Copyright (c) 2024
"""

from usr.ocpp.exceptions import SchemaValidationError


class StrEnum:
    pass


class dataclass:

    def __schemas__(self):
        # {"properties": {}, "required": []}
        return {}


# def asdict(obj):
#     if hasattr(obj, "__dict__"):
#         _dict_ = {key: (asdict(val) if is_dataclass(val) else val) for key, val in obj.__dict__.items() if not key.startswith("_")}
#         return _dict_
#     return obj


def asdict(obj):
    if is_dataclass(obj):
        return {key: (val if isinstance(val, (int, float, str)) else asdict(val)) for key, val in obj.__dict__.items() if not key.startswith("_")}
    elif isinstance(obj, list):
        return [asdict(i) for i in obj]
    return obj


def is_dataclass(obj):
    return isinstance(obj, dataclass)


def validate_dataclass(data, cls):
    if data:
        _schemas_ = cls.__schemas__()
        if _schemas_:
            for key in _schemas_["required"]:
                if key not in data.keys():
                    raise SchemaValidationError("required", "%s required filed %s" % (cls.__name__, key))
            for key, val in data.items():
                if key not in _schemas_["properties"].keys():
                    raise SchemaValidationError("NotExist", "%s %s is not in properties." % (cls.__name__, key))
                if _schemas_["properties"][key]["type"] in (int, float, str):
                    if not isinstance(val, _schemas_["properties"][key]["type"]):
                        raise SchemaValidationError("type", "%s %s value type is not compared." % (cls.__name__, key))
                if _schemas_["properties"][key]["type"] is str:
                    if _schemas_["properties"][key].get("maxLength"):
                        if len(val) > _schemas_["properties"][key]["maxLength"]:
                            raise SchemaValidationError(
                                "maxLength",
                                "%s %s value length %s is larger than maxLength %s." % (
                                    cls.__name__, key, len(val), _schemas_["properties"][key]["maxLength"]
                                )
                            )
                if _schemas_["properties"][key]["type"] is StrEnum:
                    _enum_obj = _schemas_["properties"][key]["enum"]
                    if val not in [v for k, v in _enum_obj.__dict__.items() if not k.startswith("_")]:
                        raise SchemaValidationError("type", "%s %s value is not in enums." % (cls.__name__, key))
                if _schemas_["properties"][key]["type"] is dataclass:
                    validate_dataclass(val, _schemas_["properties"][key]["cls"])
                if _schemas_["properties"][key]["type"] is list:
                    if val:
                        if _schemas_["properties"][key]["items"]["type"] is str:
                            for item in val:
                                if not isinstance(item, str):
                                    raise SchemaValidationError("type", "%s %s items type is not string." % (cls.__name__, key))
                                if _schemas_["properties"][key]["items"].get("maxLength"):
                                    if len(item) > _schemas_["properties"][key]["items"].get("maxLength"):
                                        raise SchemaValidationError(
                                            "maxLength",
                                            "%s %s item length %s is larger than maxLength %s." % (
                                                cls.__name__, key, len(item), _schemas_["properties"][key]["items"]["maxLength"]
                                            )
                                        )
                        if _schemas_["properties"][key]["items"]["type"] is dataclass:
                            for item in val:
                                validate_dataclass(item, _schemas_["properties"][key]["items"]["cls"])
