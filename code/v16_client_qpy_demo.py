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
@file      :v16_client_qpy_demo.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2024-03-25 11:21:14
@copyright :Copyright (c) 2024
"""

import modem
import utime
import _thread

from usr.tools import uwebsocket, logging
from usr.ocpp.v16 import call, call_result
from usr.ocpp.v16 import ChargePoint as cp
from usr.ocpp.v16.enums import (
    RegistrationStatus,
    CancelReservationStatus,
    CertificateSignedStatus,
    AvailabilityType,
    AvailabilityStatus,
    ConfigurationStatus,
    ClearCacheStatus,
    ChargingProfilePurposeType,
    HashAlgorithm,
    ClearChargingProfileStatus,
    DeleteCertificateStatus,
    MessageTrigger,
    TriggerMessageStatus,
    ChargingRateUnitType,
    GetCompositeScheduleStatus,
    CertificateUse,
    GetInstalledCertificateStatus,
    Log,
    ChargingProfileKindType,
    RecurrencyKind,
    ResetType,
    UpdateType,
    AuthorizationStatus,
    DiagnosticsStatus,
    FirmwareStatus,
    UploadLogStatus,
    ReadingContext,
    ValueFormat,
    Measurand,
    Phase,
    Location,
    UnitOfMeasure,
    Reason,
    ChargePointErrorCode,
    ChargePointStatus,
)
from usr.ocpp.v16.datatypes import (
    CertificateHashData,
    LogParameters,
    ChargingProfile,
    AuthorizationData,
    IdTagInfo,
    Firmware,
    MeterValue,
    SampledValue,
    ChargingSchedule,
    ChargingSchedulePeriod,
)

logger = logging.getLogger(__name__)


IMEI = modem.getDevImei()


def utcnow():
    if utime.getTimeZone() != 0:
        utime.setTimeZone(0)
    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000000".format(*utime.localtime())


class ChargePoint(cp):

    def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="ICU Eve Mini",
            charge_point_vendor="Alfen BV",
            firmware_version="#1:3.4.0-2990#N:217H;1.0-223"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == RegistrationStatus.accepted:
            logger.info("Connected to central system.")

    def send_cancel_reservation(self):
        request = call.CancelReservationPayload(
            reservation_id=123
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == CancelReservationStatus.accepted:
            logger.info("Cancel reservation status %s." % response.status)

    def send_certificate_signed(self):
        request = call.CertificateSignedPayload(
            certificate_chain="TEST_CERTIFICATE_CHAIN"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == CertificateSignedStatus.accepted:
            logger.info("Certificate signed status %s." % response.status)

    def send_change_availability(self):
        request = call.ChangeAvailabilityPayload(
            connector_id=123,
            type=AvailabilityType.inoperative
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == AvailabilityStatus.accepted:
            logger.info("Change availability status %s." % response.status)

    def send_change_configuration(self):
        request = call.ChangeConfigurationPayload(
            key="period",
            value="30"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == ConfigurationStatus.accepted:
            logger.info("Change configuration status %s." % response.status)

    def send_clear_cache(self):
        request = call.ClearCachePayload()
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == ClearCacheStatus.accepted:
            logger.info("Clear cache status %s." % response.status)

    def send_clear_charging_profile(self):
        request = call.ClearChargingProfilePayload(
            id=123,
            connector_id=456,
            charging_profile_purpose=ChargingProfilePurposeType.charge_point_max_profile,
            stack_level=789,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == ClearChargingProfileStatus.accepted:
            logger.info("Clear charging profile status %s." % response.status)

    def send_delete_certificate(self):
        request = call.DeleteCertificatePayload(
            certificate_hash_data=CertificateHashData(
                hash_algorithm=HashAlgorithm.sha256,
                issuer_name_hash="issuer_name_hash",
                issuer_key_hash="issuer_key_hash",
                serial_number="serial_number",
            )
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == DeleteCertificateStatus.accepted:
            logger.info("Delete certificate status %s." % response.status)

    def send_extended_trigger_message(self):
        request = call.ExtendedTriggerMessagePayload(
            requested_message=MessageTrigger.boot_notification,
            connector_id=123,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == TriggerMessageStatus.accepted:
            logger.info("Extended trigger message status %s." % response.status)

    def send_get_composite_schedule(self):
        request = call.GetCompositeSchedulePayload(
            connector_id=123,
            duration=10,
            charging_rate_unit=ChargingRateUnitType.watts,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == GetCompositeScheduleStatus.accepted:
            logger.info("Extended trigger message status %s." % response.status)
            logger.info(
                "connector_id %s, schedule_start %s, charging_schedule %s" % (
                    response.connector_id, response.schedule_start, response.charging_schedule
                )
            )

    def send_get_configuration(self):
        request = call.GetConfigurationPayload(
            key=["Config1", "Config2", "Config3"]
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.GetConfigurationPayload):
            logger.info("configuration_key %s." % response.configuration_key)
            logger.info("unknown_key %s." % response.unknown_key)

    def send_get_diagnostics(self):
        request = call.GetDiagnosticsPayload(
            location="location",
            retries=10,
            retry_interval=10,
            start_time=utcnow(),
            stop_time=utcnow(),
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.GetDiagnosticsPayload):
            logger.info("file_name %s." % response.file_name)

    def send_get_installed_certificate_ids(self):
        request = call.GetInstalledCertificateIdsPayload(
            certificate_type=CertificateUse.central_system_root_certificate
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == GetInstalledCertificateStatus.accepted:
            logger.info("certificate_hash_data %s." % response.certificate_hash_data)

    def send_get_local_list_version(self):
        request = call.GetLocalListVersionPayload()
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.GetLocalListVersionPayload):
            logger.info("list_version %s." % response.list_version)

    def send_get_log(self):
        request = call.GetLogPayload(
            log=LogParameters(
                remote_location="remote_location",
                oldest_timestamp=utcnow(),
                latest_timestamp=utcnow()
            ),
            log_type=Log.diagnostics_log,
            request_id=123,
            retries=3,
            retry_interval=10,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.GetLogPayload):
            logger.info("status %s." % response.status)
            logger.info("filename %s." % response.filename)

    def send_install_certificate(self):
        request = call.InstallCertificatePayload(
            certificate_type=CertificateUse.central_system_root_certificate,
            certificate="certificate"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.InstallCertificatePayload):
            logger.info("status %s." % response.status)

    def send_remote_start_transaction(self):
        request = call.RemoteStartTransactionPayload(
            id_tag="id_tag",
            connector_id=123,
            charging_profile=ChargingProfile(
                charging_profile_id=123,
                stack_level=456,
                charging_profile_purpose=ChargingProfilePurposeType.charge_point_max_profile,
                charging_profile_kind=ChargingProfileKindType.absolute,
                charging_schedule=ChargingSchedule(
                    charging_rate_unit=ChargingRateUnitType.watts,
                    charging_schedule_period=[
                        ChargingSchedulePeriod(
                            start_period=10,
                            limit=20.0,
                            number_phases=30
                        ),
                    ],
                    duration=10,
                    start_schedule=utcnow(),
                    min_charging_rate=20.0
                ),
                transaction_id=789,
                recurrency_kind=RecurrencyKind.daily,
                valid_from=utcnow(),
                valid_to=utcnow(),
            ),
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.RemoteStartTransactionPayload):
            logger.info("status %s." % response.status)

    def send_remote_stop_transaction(self):
        request = call.RemoteStopTransactionPayload(
            transaction_id=123,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.RemoteStopTransactionPayload):
            logger.info("status %s." % response.status)

    def send_reserve_now(self):
        request = call.ReserveNowPayload(
            connector_id=123,
            expiry_date=utcnow(),
            id_tag="id_tag",
            reservation_id=456,
            parent_id_tag="parent_id_tag",
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.ReserveNowPayload):
            logger.info("status %s." % response.status)

    def send_reset(self):
        request = call.ResetPayload(
            type=ResetType.hard
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.ResetPayload):
            logger.info("status %s." % response.status)

    def send_send_local_list(self):
        request = call.SendLocalListPayload(
            list_version=123,
            update_type=UpdateType.differential,
            local_authorization_list=[
                AuthorizationData(
                    id_tag="id_tag",
                    id_tag_info=IdTagInfo(
                        status=AuthorizationStatus.accepted,
                        parent_id_tag="parent_id_tag",
                        expiry_date=utcnow()
                    )
                ),
                AuthorizationData(
                    id_tag="id_tag",
                    id_tag_info=IdTagInfo(
                        status=AuthorizationStatus.accepted,
                        parent_id_tag="parent_id_tag",
                        expiry_date=utcnow()
                    )
                ),
            ],
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.SendLocalListPayload):
            logger.info("status %s." % response.status)

    def send_set_charging_profile(self):
        request = call.SetChargingProfilePayload(
            connector_id=123,
            cs_charging_profiles=ChargingProfile(
                charging_profile_id=123,
                stack_level=456,
                charging_profile_purpose=ChargingProfilePurposeType.charge_point_max_profile,
                charging_profile_kind=ChargingProfileKindType.absolute,
                charging_schedule=ChargingSchedule(
                    charging_rate_unit=ChargingRateUnitType.watts,
                    charging_schedule_period=[
                        ChargingSchedulePeriod(
                            start_period=10,
                            limit=20.0,
                            number_phases=30
                        ),
                    ],
                    duration=10,
                    start_schedule=utcnow(),
                    min_charging_rate=20.0
                ),
                transaction_id=789,
                recurrency_kind=RecurrencyKind.daily,
                valid_from=utcnow(),
                valid_to=utcnow(),
            )
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.SetChargingProfilePayload):
            logger.info("status %s." % response.status)

    def send_signed_update_firmware(self):
        request = call.SignedUpdateFirmwarePayload(
            request_id=123,
            firmware=Firmware(
                location="location",
                retrieve_date_time=utcnow(),
                signing_certificate="signing_certificate",
                signature="signature",
                install_date_time=utcnow()
            ),
            retries=3,
            retry_interval=10
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.SignedUpdateFirmwarePayload):
            logger.info("status %s." % response.status)

    def send_trigger_message(self):
        request = call.TriggerMessagePayload(
            requested_message=MessageTrigger.boot_notification,
            connector_id=123
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.TriggerMessagePayload):
            logger.info("status %s." % response.status)

    def send_unlock_connector(self):
        request = call.UnlockConnectorPayload(
            connector_id=123
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.UnlockConnectorPayload):
            logger.info("status %s." % response.status)

    def send_update_firmware(self):
        request = call.UpdateFirmwarePayload(
            location="http://www.quectel.com",
            retrieve_date=utcnow(),
            retries=3,
            retry_interval=10,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.UpdateFirmwarePayload):
            logger.info("response %s." % response)

    def send_authorize(self):
        request = call.AuthorizePayload(
            id_tag="id_tag",
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.AuthorizePayload):
            logger.info("id_tag_info %s." % response.id_tag_info)

    def send_diagnostics_status_notification(self):
        request = call.DiagnosticsStatusNotificationPayload(
            status=DiagnosticsStatus.idle,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.DiagnosticsStatusNotificationPayload):
            logger.info("response %s." % response)

    def send_firmware_status_notification(self):
        request = call.FirmwareStatusNotificationPayload(
            status=FirmwareStatus.downloaded,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.FirmwareStatusNotificationPayload):
            logger.info("response %s." % response)

    def send_heartbeat(self):
        request = call.HeartbeatPayload()
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.HeartbeatPayload):
            logger.info("current_time %s." % response.current_time)

    def send_log_status_notification(self):
        request = call.LogStatusNotificationPayload(
            status=UploadLogStatus.bad_message,
            request_id=123,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.LogStatusNotificationPayload):
            logger.info("response %s." % response)

    def send_meter_values_payload(self):
        request = call.MeterValuesPayload(
            connector_id=123,
            meter_value=[
                MeterValue(
                    timestamp=utcnow(),
                    sampled_value=[
                        SampledValue(
                            value="test",
                            context=ReadingContext.interruption_begin,
                            format=ValueFormat.raw,
                            measurand=Measurand.current_export,
                            phase=Phase.l1,
                            location=Location.inlet,
                            unit=UnitOfMeasure.wh
                        )
                    ]
                )
            ],
            transaction_id=456,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.MeterValuesPayload):
            logger.info("response %s." % response)

    def send_security_event_notification(self):
        request = call.SecurityEventNotificationPayload(
            type="test_type",
            timestamp=utcnow(),
            tech_info="tech_info"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.SecurityEventNotificationPayload):
            logger.info("response %s." % response)

    def send_sign_certificate(self):
        request = call.SignCertificatePayload(
            csr="csr"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.SignCertificatePayload):
            logger.info("status %s." % response.status)

    def send_signed_firmware_status_notification(self):
        request = call.SignedFirmwareStatusNotificationPayload(
            status=FirmwareStatus.downloaded,
            request_id=123,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.SignedFirmwareStatusNotificationPayload):
            logger.info("response %s." % response)

    def send_start_transaction(self):
        request = call.StartTransactionPayload(
            connector_id=123,
            id_tag="id_tag",
            meter_start=456,
            timestamp=utcnow(),
            reservation_id=789,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.StartTransactionPayload):
            logger.info("transaction_id %s." % response.transaction_id)
            logger.info("id_tag_info %s." % response.id_tag_info)

    def send_stop_transaction(self):
        request = call.StopTransactionPayload(
            meter_stop=123,
            timestamp=utcnow(),
            transaction_id=456,
            reason=Reason.emergency_stop,
            id_tag="id_tag",
            transaction_data=[
                MeterValue(
                    timestamp=utcnow(),
                    sampled_value=[
                        SampledValue(
                            value="test",
                            context=ReadingContext.interruption_begin,
                            format=ValueFormat.raw,
                            measurand=Measurand.current_export,
                            phase=Phase.l1,
                            location=Location.inlet,
                            unit=UnitOfMeasure.wh
                        )
                    ]
                ),
            ],
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.StopTransactionPayload):
            logger.info("id_tag_info %s." % response.id_tag_info)

    def send_status_notification(self):
        request = call.StatusNotificationPayload(
            connector_id=123,
            error_code=ChargePointErrorCode.connector_lock_failure,
            status=ChargePointStatus.available,
            timestamp=utcnow(),
            info="info",
            vendor_id="vendor_id",
            vendor_error_code="vendor_error_code",
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.StatusNotificationPayload):
            logger.info("response %s." % response)

    def send_data_transfer(self):
        request = call.DataTransferPayload(
            vendor_id="vendor_id",
            message_id="message_id",
            data="data"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, call_result.DataTransferPayload):
            logger.info("status %s." % response.status)
            logger.info("data %s." % response.data)


if __name__ == "__main__":
    ws = uwebsocket.Client.connect(
        "ws://106.15.58.32:31499/%s" % IMEI,
        # "ws://xxx.xxx.xxx.xxx:xxxx/868543063288971",
        headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
        debug=False
    )
    cp = ChargePoint(IMEI, ws)

    _thread.stack_size(0x2000)
    tid = _thread.start_new_thread(cp.start, ())
    utime.sleep_ms(200)

    cp_send_fun = [i for i in dir(cp) if i.startswith("send_")]
    # logger.debug("cp_send_fun %s" % repr(cp_send_fun))
    for name in cp_send_fun:
        getattr(cp, name)()
        utime.sleep_ms(100)
        break
