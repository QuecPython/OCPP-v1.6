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

"""
@file      : __init__.py
@author    : Jack Sun (jack.sun@quectel.com)
@brief     : <Description>
@version   : v1.0.0
@date      : 2024-04-23 15:57:26
@copyright : Copyright (c) 2024
"""

from usr.ocpp.charge_point import ChargePoint as cp
from usr.ocpp.v16 import call, call_result


class ChargePoint(cp):
    _call = call
    _call_result = call_result
    _ocpp_version = "1.6"
