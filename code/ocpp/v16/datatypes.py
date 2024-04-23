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
@file      : datatypes.py
@author    : Jack Sun (jack.sun@quectel.com)
@brief     : <Description>
@version   : v1.0.0
@date      : 2024-04-23 15:57:26
@copyright : Copyright (c) 2024
"""

from usr.ocpp.dataclasses import dataclass

from usr.ocpp.v16.enums import (
    StrEnum,
    AuthorizationStatus,
    ChargingProfileKindType,
    ChargingProfilePurposeType,
    ChargingRateUnitType,
    CiStringType,
    HashAlgorithm,
    Location,
    Measurand,
    Phase,
    ReadingContext,
    RecurrencyKind,
    UnitOfMeasure,
    ValueFormat,
)


class IdTagInfo(dataclass):
    """
    Contains status information about an identifier. It is returned in
    Authorize, Start Transaction and Stop Transaction responses.

    If expiryDate is not given, the status has no end date.
    """

    # status: AuthorizationStatus
    # parent_id_tag: Optional[str] = None
    # expiry_date: Optional[str] = None

    def __init__(self, status, parent_id_tag=None, expiry_date=None):
        self.status = status
        self.parent_id_tag = parent_id_tag
        self.expiry_date = expiry_date

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": AuthorizationStatus
                },
                "parent_id_tag": {
                    "type": str,
                    "maxLength": 20
                },
                "expiry_date": {
                    "type": str,
                    "format": "date-time"
                }
            },
            "required": [
                "status"
            ]
        }


class AuthorizationData(dataclass):
    """
    Elements that constitute an entry of a Local Authorization List update.
    """

    # id_tag: str
    # id_tag_info: Optional[IdTagInfo] = None

    def __init__(self, id_tag, id_tag_info=None):
        self.id_tag = id_tag
        self.id_tag_info = id_tag_info

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "id_tag": {
                    "type": str,
                    "maxLength": 20
                },
                "id_tag_info": {
                    "type": dataclass,
                    "cls": IdTagInfo
                }
            },
            "required": [
                "id_tag"
            ]
        }


class ChargingSchedulePeriod(dataclass):
    # start_period: int
    # limit: float
    # number_phases: Optional[int] = None

    def __init__(self, start_period, limit, number_phases=None):
        self.start_period = start_period
        self.limit = limit
        self.number_phases = number_phases

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "start_period": {
                    "type": int
                },
                "limit": {
                    "type": float,
                    "multipleOf": 0.1
                },
                "number_phases": {
                    "type": int
                }
            },
            "required": {
                "start_period",
                "limit"
            }
        }


class ChargingSchedule(dataclass):
    # charging_rate_unit: ChargingRateUnitType
    # charging_schedule_period: List[ChargingSchedulePeriod]
    # duration: Optional[int] = None
    # start_schedule: Optional[str] = None
    # min_charging_rate: Optional[float] = None

    def __init__(self, charging_rate_unit, charging_schedule_period, duration=None, start_schedule=None, min_charging_rate=None):
        self.charging_rate_unit = charging_rate_unit
        self.charging_schedule_period = charging_schedule_period
        self.duration = duration
        self.start_schedule = start_schedule
        self.min_charging_rate = min_charging_rate

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "charging_rate_unit": {
                    "type": StrEnum,
                    "enum": ChargingRateUnitType
                },
                "charging_schedule_period": {
                    "type": list,
                    "items": {
                        "type": dataclass,
                        "cls": ChargingSchedulePeriod
                    }
                },
                "duration": {
                    "type": int
                },
                "start_schedule": {
                    "type": str,
                    "format": "date-time"
                },
                "min_charging_rate": {
                    "type": float,
                    "multipleOf": 0.1
                }
            },
            "required": [
                "charging_rate_unit",
                "charging_schedule_period"
            ]
        }


class ChargingProfile(dataclass):
    """
    A ChargingProfile consists of a ChargingSchedule, describing the
    amount of power or current that can be delivered per time interval.
    """

    # charging_profile_id: int
    # stack_level: int
    # charging_profile_purpose: ChargingProfilePurposeType
    # charging_profile_kind: ChargingProfileKindType
    # charging_schedule: ChargingSchedule
    # transaction_id: Optional[int] = None
    # recurrency_kind: Optional[RecurrencyKind] = None
    # valid_from: Optional[str] = None
    # valid_to: Optional[str] = None

    def __init__(self, charging_profile_id, stack_level, charging_profile_purpose,
                 charging_profile_kind, charging_schedule, transaction_id=None,
                 recurrency_kind=None, valid_from=None, valid_to=None):
        self.charging_profile_id = charging_profile_id
        self.stack_level = stack_level
        self.charging_profile_purpose = charging_profile_purpose
        self.charging_profile_kind = charging_profile_kind
        self.charging_schedule = charging_schedule
        self.transaction_id = transaction_id
        self.recurrency_kind = recurrency_kind
        self.valid_from = valid_from
        self.valid_to = valid_to

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "charging_profile_id": {
                    "type": int
                },
                "stack_level": {
                    "type": int
                },
                "charging_profile_purpose": {
                    "type": StrEnum,
                    "enum": ChargingProfilePurposeType
                },
                "charging_profile_kind": {
                    "type": StrEnum,
                    "enum": ChargingProfileKindType
                },
                "charging_schedule": {
                    "type": dataclass,
                    "cls": ChargingSchedule
                },
                "transaction_id": {
                    "type": int
                },
                "recurrency_kind": {
                    "type": StrEnum,
                    "enum": RecurrencyKind
                },
                "valid_from": {
                    "type": str,
                    "format": "date-time"
                },
                "valid_to": {
                    "type": str,
                    "format": "date-time"
                }
            },
            "required": [
                "charging_profile_id",
                "stack_level",
                "charging_profile_purpose",
                "charging_profile_kind",
                "charging_schedule"
            ]
        }


class KeyValue(dataclass):
    """
    Contains information about a specific configuration key.
    It is returned in GetConfiguration.conf.
    """

    # key: str
    # readonly: bool
    # value: Optional[str] = None

    def __init__(self, key, readonly, value=None):
        self.key = key
        self.readonly = readonly
        self.value = value
        self.__post_init__()

    def __post_init__(self):
        if len(self.key) > CiStringType.ci_string_50:
            raise ValueError("Field key is longer than 50 characters")

        if self.value and len(self.value) > CiStringType.ci_string_500:
            raise ValueError("Field key is longer than 500 characters")

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "key": {
                    "type": str
                },
                "readonly": {
                    "type": bool
                },
                "value": {
                    "type": str
                }
            },
            "required": [
                "key",
                "readonly"
            ]
        }


class SampledValue(dataclass):
    """
    Single sampled value in MeterValues. Each value can be accompanied by
    optional fields.
    """

    # value: str
    # context: Optional[ReadingContext] = None
    # format: Optional[ValueFormat] = None
    # measurand: Optional[Measurand] = None
    # phase: Optional[Phase] = None
    # location: Optional[Location] = None
    # unit: Optional[UnitOfMeasure] = None

    def __init__(self, value, context=None, format=None, measurand=None, phase=None, location=None, unit=None):
        self.value = value
        self.context = context
        self.format = format
        self.measurand = measurand
        self.phase = phase
        self.location = location
        self.unit = unit

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "value": {
                    "type": str
                },
                "context": {
                    "type": StrEnum,
                    "enum": ReadingContext
                },
                "format": {
                    "type": StrEnum,
                    "enum": ValueFormat
                },
                "measurand": {
                    "type": StrEnum,
                    "enum": Measurand
                },
                "phase": {
                    "type": StrEnum,
                    "enum": Phase
                },
                "location": {
                    "type": StrEnum,
                    "enum": Location
                },
                "unit": {
                    "type": StrEnum,
                    "enum": UnitOfMeasure
                }
            },
            "required": [
                "value"
            ]
        }


class MeterValue(dataclass):
    """
    Collection of one or more sampled values in MeterValues.req.
    All sampled values in a MeterValue are sampled at the same point in time.
    """

    # timestamp: str
    # sampled_value: List[SampledValue]

    def __init__(self, timestamp, sampled_value):
        self.timestamp = timestamp
        self.sampled_value = sampled_value

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "timestamp": {
                    "type": str,
                    "format": "date-time"
                },
                "sampled_value": {
                    "type": list,
                    "items": {
                        "type": dataclass,
                        "cls": SampledValue
                    }
                }
            },
            "required": [
                "timestamp",
                "sampled_value"
            ]
        }


# Security Extension


class CertificateHashData(dataclass):
    """
    CertificateHashDataType is used by:
    DeleteCertificate.req, GetInstalledCertificateIds.conf
    """

    # hash_algorithm: HashAlgorithm
    # issuer_name_hash: str
    # issuer_key_hash: str
    # serial_number: str

    def __init__(self, hash_algorithm, issuer_name_hash, issuer_key_hash, serial_number):
        self.hash_algorithm = hash_algorithm
        self.issuer_name_hash = issuer_name_hash
        self.issuer_key_hash = issuer_key_hash
        self.serial_number = serial_number

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "hash_algorithm": {
                    "type": StrEnum,
                    "enum": HashAlgorithm
                },
                "issuer_name_hash": {
                    "type": str,
                    "maxLength": 128
                },
                "issuer_key_hash": {
                    "type": str,
                    "maxLength": 128
                },
                "serial_number": {
                    "type": str,
                    "maxLength": 40
                }
            },
            "required": [
                "hash_algorithm",
                "issuer_name_hash",
                "issuer_key_hash",
                "serial_number"
            ],
        }


class Firmware(dataclass):
    """
    Represents a copy of the firmware that can be loaded/updated on the Charge Point.
    FirmwareType is used by: SignedUpdateFirmware.req
    """

    # location: str
    # retrieve_date_time: str
    # signing_certificate: str
    # install_date_time: Optional[str] = None
    # signature: Optional[str] = None

    def __init__(self, location, retrieve_date_time, signing_certificate, signature, install_date_time=None):
        self.location = location
        self.retrieve_date_time = retrieve_date_time
        self.signing_certificate = signing_certificate
        self.signature = signature
        self.install_date_time = install_date_time

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "location": {
                    "type": str,
                    "maxLength": 512
                },
                "retrieve_date_time": {
                    "type": str,
                    "format": "date-time"
                },
                "signing_certificate": {
                    "type": str,
                    "maxLength": 5500
                },
                "signature": {
                    "type": str,
                    "maxLength": 800
                },
                "install_date_time": {
                    "type": str,
                    "format": "date-time"
                }
            },
            "required": [
                "location",
                "retrieve_date_time",
                "signing_certificate",
                "signature"
            ]
        }


class LogParameters(dataclass):
    """
    Class for detailed information the retrieval of logging entries.
    LogParametersType is used by: GetLog.req
    """

    # remote_location: str
    # oldest_timestamp: Optional[str] = None
    # latest_timestamp: Optional[str] = None

    def __init__(self, remote_location, oldest_timestamp=None, latest_timestamp=None):
        self.remote_location = remote_location
        self.oldest_timestamp = oldest_timestamp
        self.latest_timestamp = latest_timestamp

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "remote_location": {
                    "type": str,
                    "maxLength": 512
                },
                "oldest_timestamp": {
                    "type": str,
                    "format": "date-time"
                },
                "latest_timestamp": {
                    "type": str,
                    "format": "date-time"
                }
            },
            "required": [
                "remote_location"
            ]
        }
