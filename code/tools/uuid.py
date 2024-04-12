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
@file      :uuid.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2024-03-15 10:38:22
@copyright :Copyright (c) 2024
"""
import urandom

int_ = int      # The built-in int type
bytes_ = bytes  # The built-in bytes type


class UUID:

    def __init__(self, bytes=None, version=None, int=None):
        if bytes is not None:
            if len(bytes) != 16:
                raise ValueError('bytes is not a 16-char string')
            assert isinstance(bytes, bytes_), repr(bytes)
            int = int_.from_bytes(bytes, "big")
        if int is not None:
            if not 0 <= int < (1 << 128):
                raise ValueError('int is out of range (need a 128-bit value)')
        if version is not None:
            if not 1 <= version <= 5:
                raise ValueError('illegal version number')
            # Set the variant to RFC 4122.
            int &= ~(0xc000 << 48)
            int |= 0x8000 << 48
            # Set the version number.
            int &= ~(0xf000 << 64)
            int |= version << 76
        self.int = int

    def __str__(self):
        hex = '%032x' % self.int
        return '%s-%s-%s-%s-%s' % (hex[:8], hex[8:12], hex[12:16], hex[16:20], hex[20:])


def uuid4():
    return UUID(bytes=bytes([urandom.randint(0, 0xFF) for i in range(16)]), version=4)
