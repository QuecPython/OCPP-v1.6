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
@file      : call.py
@author    : Jack Sun (jack.sun@quectel.com)
@brief     : <Description>
@version   : v1.0.0
@date      : 2024-04-23 15:57:26
@copyright : Copyright (c) 2024
"""

from usr.ocpp.dataclasses import dataclass

from usr.ocpp.v16.enums import (
    StrEnum,
    AvailabilityType,
    CertificateUse,
    ChargePointErrorCode,
    ChargePointStatus,
    ChargingProfilePurposeType,
    ChargingRateUnitType,
    DiagnosticsStatus,
    FirmwareStatus,
    Log,
    MessageTrigger,
    Reason,
    ResetType,
    UpdateType,
    UploadLogStatus,
)

from usr.ocpp.v16.datatypes import (
    CertificateHashData,
    LogParameters,
    ChargingProfile,
    AuthorizationData,
    Firmware,
    MeterValue,
)

# Most types of CALL messages can originate from only 1 source, either
# from a Charge Point or Central System, but not from both.
#
# Take for example the CALL for an ChangeConfiguration action. This type of
# CALL can only be send from a Central System to Charging Station, not
# the other way around.
#
# For some types of CALL messages the opposite is true; for example for the
# CALL message for a BootNotification action. This can only come from a Charge
# Point and send to a Central System.
#
# The only CALL that can originate from both a Central System and a
# Charge Point is the CALL message for a DataTransfer.

# The now following section of classes are for CALL messages that flow
# from Central System to Charge Point.


class CancelReservationPayload(dataclass):
    # reservation_id: int

    def __init__(self, reservation_id):
        self.reservation_id = reservation_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "reservation_id": {
                    "type": int
                }
            },
            "required": [
                "reservation_id"
            ],
        }


class CertificateSignedPayload(dataclass):
    # certificate_chain: str

    def __init__(self, certificate_chain):
        self.certificate_chain = certificate_chain

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "certificate_chain": {
                    "type": str,
                    "maxLength": 10000
                }
            },
            "required": [
                "certificate_chain"
            ],
        }


class ChangeAvailabilityPayload(dataclass):
    # connector_id: int
    # type: AvailabilityType

    def __init__(self, connector_id, type):
        self.connector_id = connector_id
        self.type = type

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "connector_id": {
                    "type": int
                },
                "type": {
                    "type": StrEnum,
                    "enum": AvailabilityType
                }
            },
            "required": [
                "connector_id",
                "type"
            ]
        }


class ChangeConfigurationPayload(dataclass):
    # key: str
    # value: str

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "key": {
                    "type": str,
                    "maxLength": 50
                },
                "value": {
                    "type": str,
                    "maxLength": 500
                }
            },
            "required": [
                "key",
                "value"
            ],
        }


class ClearCachePayload(dataclass):
    pass


class ClearChargingProfilePayload(dataclass):
    # id: Optional[int] = None
    # connector_id: Optional[int] = None
    # charging_profile_purpose: Optional[ChargingProfilePurposeType] = None
    # stack_level: Optional[int] = None

    def __init__(self, id=None, connector_id=None, charging_profile_purpose=None, stack_level=None):
        self.id = id
        self.connector_id = connector_id
        self.charging_profile_purpose = charging_profile_purpose
        self.stack_level = stack_level

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "id": {
                    "type": int
                },
                "connector_id": {
                    "type": int
                },
                "charging_profile_purpose": {
                    "type": StrEnum,
                    "enum": ChargingProfilePurposeType
                },
                "stack_level": {
                    "type": int
                }
            },
            "required": []
        }


class DeleteCertificatePayload(dataclass):
    # certificate_hash_data: Dict

    def __init__(self, certificate_hash_data):
        self.certificate_hash_data = certificate_hash_data

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "certificate_hash_data": {
                    "type": dataclass,
                    "cls": CertificateHashData
                }
            },
            "required": [
                "certificate_hash_data"
            ]
        }


class ExtendedTriggerMessagePayload(dataclass):
    # requested_message: MessageTrigger
    # connector_id: Optional[int] = None

    def __init__(self, requested_message, connector_id=None):
        self.requested_message = requested_message
        self.connector_id = connector_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "requested_message": {
                    "type": StrEnum,
                    "enum": MessageTrigger
                },
                "connector_id": {
                    "type": int
                }
            },
            "required": [
                "requested_message"
            ]
        }


class GetCompositeSchedulePayload(dataclass):
    # connector_id: int
    # duration: int
    # charging_rate_unit: Optional[ChargingRateUnitType] = None

    def __init__(self, connector_id, duration, charging_rate_unit=None):
        self.connector_id = connector_id
        self.duration = duration
        self.charging_rate_unit = charging_rate_unit

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "connector_id": {
                    "type": int
                },
                "duration": {
                    "type": int
                },
                "charging_rate_unit": {
                    "type": StrEnum,
                    "enum": ChargingRateUnitType
                }
            },
            "required": [
                "connector_id",
                "duration"
            ]
        }


class GetConfigurationPayload(dataclass):
    # key: Optional[List] = None

    def __init__(self, key=None):
        self.key = key

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "key": {
                    "type": list,
                    "items": {
                        "type": str,
                        "maxLength": 50
                    }
                }
            },
            "required": []
        }


class GetDiagnosticsPayload(dataclass):
    # location: str
    # retries: Optional[int] = None
    # retry_interval: Optional[int] = None
    # start_time: Optional[str] = None
    # stop_time: Optional[str] = None

    def __init__(self, location, retries=None, retry_interval=None, start_time=None, stop_time=None):
        self.location = location
        self.retries = retries
        self.retry_interval = retry_interval
        self.start_time = start_time
        self.stop_time = stop_time

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "location": {
                    "type": str,
                    "format": "uri"
                },
                "retries": {
                    "type": int
                },
                "retry_interval": {
                    "type": int
                },
                "start_time": {
                    "type": str,
                    "format": "date-time"
                },
                "stop_time": {
                    "type": str,
                    "format": "date-time"
                }
            },
            "required": [
                "location"
            ]
        }


class GetInstalledCertificateIdsPayload(dataclass):
    # certificate_type: CertificateUse

    def __init__(self, certificate_type):
        self.certificate_type = certificate_type

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "certificate_type": {
                    "type": StrEnum,
                    "enum": CertificateUse
                }
            },
            "required": [
                "certificate_type"
            ]
        }


class GetLocalListVersionPayload(dataclass):
    pass


class GetLogPayload(dataclass):
    # log: Dict
    # log_type: Log
    # request_id: int
    # retries: Optional[int] = None
    # retry_interval: Optional[int] = None

    def __init__(self, log, log_type, request_id, retries=None, retry_interval=None):
        self.log = log
        self.log_type = log_type
        self.request_id = request_id
        self.retries = retries
        self.retry_interval = retry_interval

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "log": {
                    "type": dataclass,
                    "cls": LogParameters
                },
                "log_type": {
                    "type": StrEnum,
                    "enum": Log
                },
                "request_id": {
                    "type": int
                },
                "retries": {
                    "type": int
                },
                "retry_interval": {
                    "type": int
                }
            },
            "required": [
                "log",
                "log_type",
                "request_id"
            ]
        }


class InstallCertificatePayload(dataclass):
    # certificate_type: CertificateUse
    # certificate: str

    def __init__(self, certificate_type, certificate):
        self.certificate_type = certificate_type
        self.certificate = certificate

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "certificate_type": {
                    "type": StrEnum,
                    "enum": CertificateUse
                },
                "certificate": {
                    "type": str,
                    "maxLength": 5500
                }
            },
            "required": [
                "certificate_type",
                "certificate"
            ]
        }


class RemoteStartTransactionPayload(dataclass):
    # id_tag: str
    # connector_id: Optional[int] = None
    # charging_profile: Optional[Dict] = None

    def __init__(self, id_tag, connector_id=None, charging_profile=None):
        self.id_tag = id_tag
        self.connector_id = connector_id
        self.charging_profile = charging_profile

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "id_tag": {
                    "type": str,
                    "maxLength": 20
                },
                "connector_id": {
                    "type": int
                },
                "charging_profile": {
                    "type": dataclass,
                    "cls": ChargingProfile
                }
            },
            "required": [
                "id_tag"
            ]
        }


class RemoteStopTransactionPayload(dataclass):
    # transaction_id: int

    def __init__(self, transaction_id):
        self.transaction_id = transaction_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "transaction_id": {
                    "type": int
                }
            },
            "required": [
                "transaction_id"
            ]
        }


class ReserveNowPayload(dataclass):
    # connector_id: int
    # expiry_date: str
    # id_tag: str
    # reservation_id: int
    # parent_id_tag: Optional[str] = None

    def __init__(self, connector_id, expiry_date, id_tag, reservation_id, parent_id_tag=None):
        self.connector_id = connector_id
        self.expiry_date = expiry_date
        self.id_tag = id_tag
        self.reservation_id = reservation_id
        self.parent_id_tag = parent_id_tag

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "connector_id": {
                    "type": int
                },
                "expiry_date": {
                    "type": str,
                    "format": "date-time"
                },
                "id_tag": {
                    "type": str,
                    "maxLength": 20
                },
                "reservation_id": {
                    "type": int
                },
                "parent_id_tag": {
                    "type": str,
                    "maxLength": 20
                }
            },
            "required": [
                "connector_id",
                "expiry_date",
                "id_tag",
                "reservation_id"
            ]
        }


class ResetPayload(dataclass):
    # type: ResetType

    def __init__(self, type):
        self.type = type

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "type": {
                    "type": StrEnum,
                    "enum": ResetType
                }
            },
            "required": [
                "type"
            ]
        }


class SendLocalListPayload(dataclass):
    # list_version: int
    # update_type: UpdateType
    # local_authorization_list: List = field(default_factory=list)

    def __init__(self, list_version, update_type, local_authorization_list=[]):
        self.list_version = list_version
        self.update_type = update_type
        self.local_authorization_list = local_authorization_list

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "list_version": {
                    "type": int
                },
                "update_type": {
                    "type": StrEnum,
                    "enum": UpdateType
                },
                "local_authorization_list": {
                    "type": list,
                    "items": {
                        "type": dataclass,
                        "cls": AuthorizationData
                    }
                }
            },
            "required": [
                "list_version",
                "update_type"
            ]
        }


class SetChargingProfilePayload(dataclass):
    # connector_id: int
    # cs_charging_profiles: Dict

    def __init__(self, connector_id, cs_charging_profiles):
        self.connector_id = connector_id
        self.cs_charging_profiles = cs_charging_profiles

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "connector_id": {
                    "type": int
                },
                "cs_charging_profiles": {
                    "type": dataclass,
                    "cls": ChargingProfile
                }
            },
            "required": [
                "connector_id",
                "cs_charging_profiles"
            ]
        }


class SignedUpdateFirmwarePayload(dataclass):
    # request_id: int
    # firmware: Dict
    # retries: Optional[int] = None
    # retry_interval: Optional[int] = None

    def __init__(self, request_id, firmware, retries=None, retry_interval=None):
        self.request_id = request_id
        self.firmware = firmware
        self.retries = retries
        self.retry_interval = retry_interval

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "request_id": {
                    "type": int
                },
                "firmware": {
                    "type": dataclass,
                    "cls": Firmware
                },
                "retries": {
                    "type": int
                },
                "retry_interval": {
                    "type": int
                }
            },
            "required": [
                "request_id",
                "firmware"
            ]
        }


class TriggerMessagePayload(dataclass):
    # requested_message: MessageTrigger
    # connector_id: Optional[int] = None

    def __init__(self, requested_message, connector_id=None):
        self.requested_message = requested_message
        self.connector_id = connector_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "requested_message": {
                    "type": StrEnum,
                    "enum": MessageTrigger
                },
                "connector_id": {
                    "type": int
                }
            },
            "required": [
                "requested_message"
            ]
        }


class UnlockConnectorPayload(dataclass):
    # connector_id: int

    def __init__(self, connector_id):
        self.connector_id = connector_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "connector_id": {
                    "type": int
                }
            },
            "required": [
                "connector_id"
            ]
        }


class UpdateFirmwarePayload(dataclass):
    # location: str
    # retrieve_date: str
    # retries: Optional[int] = None
    # retry_interval: Optional[int] = None

    def __init__(self, location, retrieve_date, retries=None, retry_interval=None):
        self.location = location
        self.retrieve_date = retrieve_date
        self.retries = retries
        self.retry_interval = retry_interval

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "location": {
                    "type": str,
                    "format": "uri"
                },
                "retrieve_date": {
                    "type": str,
                    "format": "date-time"
                },
                "retries": {
                    "type": int
                },
                "retry_interval": {
                    "type": int
                }
            },
            "required": [
                "location",
                "retrieve_date"
            ]
        }


# The CALL messages that flow from Charge Point to Central System are listed
# in the bottom part of this module.


class AuthorizePayload(dataclass):
    # id_tag: str

    def __init__(self, id_tag):
        self.id_tag = id_tag

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "id_tag": {
                    "type": str,
                    "maxLength": 20
                }
            },
            "required": [
                "id_tag"
            ]
        }


class BootNotificationPayload(dataclass):
    # charge_point_model: str
    # charge_point_vendor: str
    # charge_box_serial_number: Optional[str] = None
    # charge_point_serial_number: Optional[str] = None
    # firmware_version: Optional[str] = None
    # iccid: Optional[str] = None
    # imsi: Optional[str] = None
    # meter_serial_number: Optional[str] = None
    # meter_type: Optional[str] = None

    def __init__(self, charge_point_model, charge_point_vendor, charge_box_serial_number=None,
                 charge_point_serial_number=None, firmware_version=None, iccid=None, imsi=None,
                 meter_serial_number=None, meter_type=None):
        self.charge_point_model = charge_point_model
        self.charge_point_vendor = charge_point_vendor
        self.charge_box_serial_number = charge_box_serial_number
        self.charge_point_serial_number = charge_point_serial_number
        self.firmware_version = firmware_version
        self.iccid = iccid
        self.imsi = imsi
        self.meter_serial_number = meter_serial_number
        self.meter_type = meter_type

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "charge_point_model": {
                    "type": str,
                    "maxLength": 20
                },
                "charge_point_vendor": {
                    "type": str,
                    "maxLength": 20
                },
                "charge_box_serial_number": {
                    "type": str,
                    "maxLength": 25
                },
                "charge_point_serial_number": {
                    "type": str,
                    "maxLength": 25
                },
                "firmware_version": {
                    "type": str,
                    "maxLength": 50
                },
                "iccid": {
                    "type": str,
                    "maxLength": 20
                },
                "imsi": {
                    "type": str,
                    "maxLength": 20
                },
                "meter_serial_number": {
                    "type": str,
                    "maxLength": 25
                },
                "meter_type": {
                    "type": str,
                    "maxLength": 25
                }
            },
            "required": [
                "charge_point_model",
                "charge_point_vendor"
            ]
        }


class DiagnosticsStatusNotificationPayload(dataclass):
    # status: DiagnosticsStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": DiagnosticsStatus
                }
            },
            "required": [
                "status"
            ]
        }


class FirmwareStatusNotificationPayload(dataclass):
    # status: FirmwareStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": FirmwareStatus
                }
            },
            "required": [
                "status"
            ]
        }


class HeartbeatPayload(dataclass):
    pass


class LogStatusNotificationPayload(dataclass):
    # status: UploadLogStatus
    # request_id: int

    def __init__(self, status, request_id):
        self.status = status
        self.request_id = request_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": UploadLogStatus
                },
                "request_id": {
                    "type": int
                }
            },
            "required": [
                "status",
                "request_id"
            ]
        }


class MeterValuesPayload(dataclass):
    # connector_id: int
    # meter_value: List = field(default_factory=list)
    # transaction_id: Optional[int] = None

    def __init__(self, connector_id, meter_value, transaction_id=None):
        self.connector_id = connector_id
        self.meter_value = meter_value
        self.transaction_id = transaction_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "connector_id": {
                    "type": int
                },
                "meter_value": {
                    "type": list,
                    "items": {
                        "type": dataclass,
                        "cls": MeterValue
                    }
                },
                "transaction_id": {
                    "type": int
                }
            },
            "required": [
                "connector_id",
                "meter_value"
            ]
        }


class SecurityEventNotificationPayload(dataclass):
    # type: str
    # timestamp: str
    # tech_info: Optional[str]

    def __init__(self, type, timestamp, tech_info=None):
        self.type = type
        self.timestamp = timestamp
        self.tech_info = tech_info

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "type": {
                    "type": str,
                    "maxLength": 50
                },
                "timestamp": {
                    "type": str,
                    "format": "date-time"
                },
                "tech_info": {
                    "type": str,
                    "maxLength": 255
                },
            },
            "required": [
                "type",
                "timestamp"
            ]
        }


class SignCertificatePayload(dataclass):
    # csr: str

    def __init__(self, csr):
        self.csr = csr

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "csr": {
                    "type": str,
                    "maxLength": 5500
                }
            },
            "required": [
                "csr"
            ]
        }


class SignedFirmwareStatusNotificationPayload(dataclass):
    # status: FirmwareStatus
    # request_id: int

    def __init__(self, status, request_id):
        self.status = status
        self.request_id = request_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": FirmwareStatus
                },
                "request_id": {
                    "type": int
                }
            },
            "required": [
                "status",
                "request_id"
            ]
        }


class StartTransactionPayload(dataclass):
    # connector_id: int
    # id_tag: str
    # meter_start: int
    # timestamp: str
    # reservation_id: Optional[int] = None

    def __init__(self, connector_id, id_tag, meter_start, timestamp, reservation_id=None):
        self.connector_id = connector_id
        self.id_tag = id_tag
        self.meter_start = meter_start
        self.timestamp = timestamp
        self.reservation_id = reservation_id

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "connector_id": {
                    "type": int
                },
                "id_tag": {
                    "type": str,
                    "maxLength": 20
                },
                "meter_start": {
                    "type": int
                },
                "timestamp": {
                    "type": str,
                    "format": "date-time"
                },
                "reservation_id": {
                    "type": int
                }
            },
            "required": [
                "connector_id",
                "id_tag",
                "meter_start",
                "timestamp"
            ]
        }


class StopTransactionPayload(dataclass):
    # meter_stop: int
    # timestamp: str
    # transaction_id: int
    # reason: Optional[Reason] = None
    # id_tag: Optional[str] = None
    # transaction_data: Optional[List] = None

    def __init__(self, meter_stop, timestamp, transaction_id, reason=None, id_tag=None, transaction_data=None):
        self.meter_stop = meter_stop
        self.timestamp = timestamp
        self.transaction_id = transaction_id
        self.reason = reason
        self.id_tag = id_tag
        self.transaction_data = transaction_data

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "meter_stop": {
                    "type": int
                },
                "timestamp": {
                    "type": str,
                    "format": "date-time"
                },
                "transaction_id": {
                    "type": int
                },
                "reason": {
                    "type": StrEnum,
                    "enum": Reason
                },
                "id_tag": {
                    "type": str,
                    "maxLength": 20
                },
                "transaction_data": {
                    "type": list,
                    "items": {
                        "type": dataclass,
                        "cls": MeterValue
                    }
                }
            },
            "required": [
                "meter_stop",
                "timestamp",
                "transaction_id"
            ]
        }


class StatusNotificationPayload(dataclass):
    # connector_id: int
    # error_code: ChargePointErrorCode
    # status: ChargePointStatus
    # timestamp: Optional[str] = None
    # info: Optional[str] = None
    # vendor_id: Optional[str] = None
    # vendor_error_code: Optional[str] = None

    def __init__(self, connector_id, error_code, status, timestamp=None, info=None, vendor_id=None, vendor_error_code=None):
        self.connector_id = connector_id
        self.error_code = error_code
        self.status = status
        self.timestamp = timestamp
        self.info = info
        self.vendor_id = vendor_id
        self.vendor_error_code = vendor_error_code

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "connector_id": {
                    "type": int
                },
                "error_code": {
                    "type": StrEnum,
                    "enum": ChargePointErrorCode
                },
                "status": {
                    "type": StrEnum,
                    "enum": ChargePointStatus
                },
                "timestamp": {
                    "type": str,
                    "format": "date-time"
                },
                "info": {
                    "type": str,
                    "maxLength": 50
                },
                "vendor_id": {
                    "type": str,
                    "maxLength": 255
                },
                "vendor_error_code": {
                    "type": str,
                    "maxLength": 50
                }
            },
            "required": [
                "connector_id",
                "error_code",
                "status"
            ]
        }


# The DataTransfer CALL can be send both from Central System as well as from a
# Charge Point.


class DataTransferPayload(dataclass):
    # vendor_id: str
    # message_id: Optional[str] = None
    # data: Optional[str] = None

    def __init__(self, vendor_id, message_id=None, data=None):
        self.vendor_id = vendor_id
        self.message_id = message_id
        self.data = data

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "vendor_id": {
                    "type": str,
                    "maxLength": 255
                },
                "message_id": {
                    "type": str,
                    "maxLength": 50
                },
                "data": {
                    "type": str,
                }
            },
            "required": [
                "vendor_id"
            ]
        }
