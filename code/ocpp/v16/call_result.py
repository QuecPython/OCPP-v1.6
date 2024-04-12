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

from usr.ocpp.dataclasses import dataclass

from usr.ocpp.v16.datatypes import (
    IdTagInfo,
    CertificateHashData,
    ChargingSchedule,
    KeyValue,
)

from usr.ocpp.v16.enums import (
    StrEnum,
    AvailabilityStatus,
    CancelReservationStatus,
    CertificateSignedStatus,
    CertificateStatus,
    ChargingProfileStatus,
    ClearCacheStatus,
    ClearChargingProfileStatus,
    ConfigurationStatus,
    DataTransferStatus,
    DeleteCertificateStatus,
    GenericStatus,
    GetCompositeScheduleStatus,
    GetInstalledCertificateStatus,
    LogStatus,
    RegistrationStatus,
    RemoteStartStopStatus,
    ReservationStatus,
    ResetStatus,
    TriggerMessageStatus,
    UnlockStatus,
    UpdateFirmwareStatus,
    UpdateStatus,
)


# Most types of CALLRESULT messages can originate from only 1 source, either
# from a Charge Point or Central System, but not from both.
#
# Take for example the CALLRESULT for an Authorize action. This type of
# CALLRESULT can only be send from a Central System to Charging Station, not
# the other way around.
#
# For some types of CALLRESULT messages the opposite is true; for example for
# the CALLRESULT message for a Reset action. This can only come from a Charge
# Point to a Central System.
#
# The only CALLRESULT that can originate from both a Central System and a
# Charge Point is the CALLRESULT message for a DataTransfer.

# The now following section of classes are for CALLRESULT messages that flow
# from Central System to Charge Point.


class AuthorizePayload(dataclass):
    # id_tag_info: IdTagInfo

    def __init__(self, id_tag_info):
        self.id_tag_info = id_tag_info

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "id_tag_info": {
                    "type": dataclass,
                    "cls": IdTagInfo
                }
            },
            "required": [
                "id_tag_info"
            ]
        }


class BootNotificationPayload(dataclass):
    # current_time: str
    # interval: int
    # status: RegistrationStatus

    def __init__(self, current_time, interval, status):
        self.current_time = current_time
        self.interval = interval
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "current_time": {
                    "type": str,
                    "format": "date-time"
                },
                "interval": {
                    "type": int
                },
                "status": {
                    "type": StrEnum,
                    "enum": RegistrationStatus
                }
            },
            "required": [
                "current_time",
                "interval",
                "status"
            ]
        }


class DiagnosticsStatusNotificationPayload(dataclass):
    pass


class FirmwareStatusNotificationPayload(dataclass):
    pass


class HeartbeatPayload(dataclass):
    # current_time: str

    def __init__(self, current_time):
        self.current_time = current_time

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "current_time": {
                    "type": str,
                    "format": "date-time"
                }
            },
            "required": [
                "current_time"
            ]
        }


class LogStatusNotificationPayload(dataclass):
    pass


class SecurityEventNotificationPayload(dataclass):
    pass


class SignCertificatePayload(dataclass):
    # status: GenericStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": GenericStatus
                }
            },
            "required": [
                "status"
            ]
        }


class MeterValuesPayload(dataclass):
    pass


class StartTransactionPayload(dataclass):
    # transaction_id: int
    # id_tag_info: IdTagInfo

    def __init__(self, transaction_id, id_tag_info):
        self.transaction_id = transaction_id
        self.id_tag_info = id_tag_info

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "transaction_id": {
                    "type": int
                },
                "id_tag_info": {
                    "type": dataclass,
                    "cls": IdTagInfo
                }
            },
            "required": [
                "transaction_id",
                "id_tag_info"
            ]
        }


class StatusNotificationPayload(dataclass):
    pass


class StopTransactionPayload(dataclass):
    # id_tag_info: Optional[IdTagInfo] = None

    def __init__(self, id_tag_info=None):
        self.id_tag_info = id_tag_info

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "id_tag_info": {
                    "type": dataclass,
                    "cls": IdTagInfo
                }
            },
            "required": []
        }

# The CALLRESULT messages that flow from Charge Point to Central System are
# listed in the bottom part of this module.


class CancelReservationPayload(dataclass):
    # status: CancelReservationStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": CancelReservationStatus
                }
            },
            "required": [
                "status"
            ]
        }


class CertificateSignedPayload(dataclass):
    # status: CertificateSignedStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": CertificateSignedStatus
                }
            },
            "required": [
                "status"
            ]
        }


class ChangeAvailabilityPayload(dataclass):
    # status: AvailabilityStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": AvailabilityStatus
                }
            },
            "required": [
                "status"
            ]
        }


class ChangeConfigurationPayload(dataclass):
    # status: ConfigurationStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": ConfigurationStatus
                }
            },
            "required": [
                "status"
            ]
        }


class ClearCachePayload(dataclass):
    # status: ClearCacheStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": ClearCacheStatus
                }
            },
            "required": [
                "status"
            ]
        }


class ClearChargingProfilePayload(dataclass):
    # status: ClearChargingProfileStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": ClearChargingProfileStatus
                }
            },
            "required": [
                "status"
            ]
        }


class DeleteCertificatePayload(dataclass):
    # status: DeleteCertificateStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": DeleteCertificateStatus
                }
            },
            "required": [
                "status"
            ]
        }


class ExtendedTriggerMessagePayload(dataclass):
    # status: TriggerMessageStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": TriggerMessageStatus
                }
            },
            "required": [
                "status"
            ]
        }


class GetInstalledCertificateIdsPayload(dataclass):
    # status: GetInstalledCertificateStatus
    # certificate_hash_data: Optional[List] = None

    def __init__(self, status, certificate_hash_data=None):
        self.status = status
        self.certificate_hash_data = certificate_hash_data

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": GetInstalledCertificateStatus
                },
                "certificate_hash_data": {
                    "type": list,
                    "items": {
                        "type": dataclass,
                        "cls": CertificateHashData
                    }
                }
            },
            "required": [
                "status"
            ]
        }


class GetCompositeSchedulePayload(dataclass):
    # status: GetCompositeScheduleStatus
    # connector_id: Optional[int] = None
    # schedule_start: Optional[str] = None
    # charging_schedule: Optional[Dict] = None

    def __init__(self, status, connector_id=None, schedule_start=None, charging_schedule=None):
        self.status = status
        self.connector_id = connector_id
        self.schedule_start = schedule_start
        self.charging_schedule = charging_schedule

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": GetCompositeScheduleStatus
                },
                "connector_id": {
                    "type": int
                },
                "schedule_start": {
                    "type": str,
                    "format": "date-time"
                },
                "charging_schedule": {
                    "type": dataclass,
                    "cls": ChargingSchedule
                }
            },
            "required": [
                "status"
            ]
        }


class GetConfigurationPayload(dataclass):
    # configuration_key: Optional[List] = None
    # unknown_key: Optional[List] = None

    def __init__(self, configuration_key=None, unknown_key=None):
        self.configuration_key = configuration_key
        self.unknown_key = unknown_key

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "configuration_key": {
                    "type": list,
                    "items": {
                        "type": dataclass,
                        "cls": KeyValue
                    }
                },
                "unknown_key": {
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
    # file_name: Optional[str] = None

    def __init__(self, file_name=None):
        self.file_name = file_name

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "file_name": {
                    "type": str,
                    "maxLength": 255
                }
            },
            "required": [
                "file_name"
            ]
        }


class GetLocalListVersionPayload(dataclass):
    # list_version: int

    def __init__(self, list_version):
        self.list_version = list_version

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "list_version": {
                    "type": int
                }
            },
            "required": [
                "list_version"
            ]
        }


class GetLogPayload(dataclass):
    # status: LogStatus
    # filename: Optional[str] = None

    def __init__(self, status, filename=None):
        self.status = status
        self.filename = filename

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": LogStatus
                },
                "filename": {
                    "type": str,
                    "maxLength": 255
                }
            },
            "required": [
                "status"
            ]
        }


class InstallCertificatePayload(dataclass):
    # status: CertificateStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": CertificateStatus
                }
            },
            "required": [
                "status"
            ]
        }


class RemoteStartTransactionPayload(dataclass):
    # status: RemoteStartStopStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": RemoteStartStopStatus
                }
            },
            "required": [
                "status"
            ]
        }


class RemoteStopTransactionPayload(dataclass):
    # status: RemoteStartStopStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": RemoteStartStopStatus
                }
            },
            "required": [
                "status"
            ]
        }


class ReserveNowPayload(dataclass):
    # status: ReservationStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": ReservationStatus
                }
            },
            "required": [
                "status"
            ]
        }


class ResetPayload(dataclass):
    # status: ResetStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": ResetStatus
                }
            },
            "required": [
                "status"
            ]
        }


class SendLocalListPayload(dataclass):
    # status: UpdateStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": UpdateStatus
                }
            },
            "required": [
                "status"
            ]
        }


class SetChargingProfilePayload(dataclass):
    # status: ChargingProfileStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": ChargingProfileStatus
                }
            },
            "required": [
                "status"
            ]
        }


class SignedFirmwareStatusNotificationPayload(dataclass):
    pass


class SignedUpdateFirmwarePayload(dataclass):
    # status: UpdateFirmwareStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": UpdateFirmwareStatus
                }
            },
            "required": [
                "status"
            ]
        }


class TriggerMessagePayload(dataclass):
    # status: TriggerMessageStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": TriggerMessageStatus
                }
            },
            "required": [
                "status"
            ]
        }


class UnlockConnectorPayload(dataclass):
    # status: UnlockStatus

    def __init__(self, status):
        self.status = status

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": UnlockStatus
                }
            },
            "required": [
                "status"
            ]
        }


class UpdateFirmwarePayload(dataclass):
    pass


# The DataTransfer CALLRESULT can be send both from Central System as well as
# from a Charge Point.


class DataTransferPayload(dataclass):
    # status: DataTransferStatus
    # data: Optional[str] = None

    def __init__(self, status, data=None):
        self.status = status
        self.data = data

    @staticmethod
    def __schemas__():
        return {
            "properties": {
                "status": {
                    "type": StrEnum,
                    "enum": DataTransferStatus
                },
                "data": {
                    "type": str,
                }
            },
            "required": [
                "status"
            ]
        }
