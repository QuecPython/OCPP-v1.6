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

import gc
import modem
import utime
import _thread

from usr.tools import uwebsocket, logging
from usr.ocpp.routing import on
from usr.ocpp.v16 import ChargePoint as cp
from usr.ocpp.v16.enums import (
    Action,
    RegistrationStatus,
    CancelReservationStatus,
    CertificateSignedStatus,
    AvailabilityStatus,
    ConfigurationStatus,
    ClearCacheStatus,
    HashAlgorithm,
    ClearChargingProfileStatus,
    DeleteCertificateStatus,
    TriggerMessageStatus,
    ChargingRateUnitType,
    GetCompositeScheduleStatus,
    GetInstalledCertificateStatus,
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
    LogStatus,
    CertificateStatus,
    RemoteStartStopStatus,
    ReservationStatus,
    ResetStatus,
    UpdateStatus,
    ChargingProfileStatus,
    UpdateFirmwareStatus,
    UnlockStatus,
    DataTransferStatus,
)
from usr.ocpp.v16.datatypes import (
    CertificateHashData,
    MeterValue,
    SampledValue,
    ChargingSchedule,
    ChargingSchedulePeriod,
    KeyValue,
)

logger = logging.getLogger(__name__)

if hasattr(modem, "getDevMAC"):
    IMEI = modem.getDevMAC()
elif hasattr(modem, "getDevImei"):
    IMEI = modem.getDevImei()
else:
    IMEI = "0001"


def utcnow():
    if utime.getTimeZone() != 0:
        utime.setTimeZone(0)
    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000000".format(*utime.localtime())


class ChargePoint(cp):

    def send_authorize(self):
        request = self._call.AuthorizePayload(
            id_tag="id_tag",
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.AuthorizePayload):
            logger.info("id_tag_info %s." % response.id_tag_info)

    def send_boot_notification(self):
        request = self._call.BootNotificationPayload(
            charge_point_model="ICU Eve Mini",
            charge_point_vendor="Alfen BV",
            firmware_version="#1:3.4.0-2990#N:217H;1.0-223"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == RegistrationStatus.accepted:
            logger.info("Connected to central system.")

    def send_diagnostics_status_notification(self):
        request = self._call.DiagnosticsStatusNotificationPayload(
            status=DiagnosticsStatus.idle,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.DiagnosticsStatusNotificationPayload):
            logger.info("response %s." % response)

    def send_firmware_status_notification(self):
        request = self._call.FirmwareStatusNotificationPayload(
            status=FirmwareStatus.downloaded,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.FirmwareStatusNotificationPayload):
            logger.info("response %s." % response)

    def send_heartbeat(self):
        request = self._call.HeartbeatPayload()
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.HeartbeatPayload):
            logger.info("current_time %s." % response.current_time)

    def send_log_status_notification(self):
        request = self._call.LogStatusNotificationPayload(
            status=UploadLogStatus.bad_message,
            request_id=123,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.LogStatusNotificationPayload):
            logger.info("response %s." % response)

    def send_meter_values_payload(self):
        request = self._call.MeterValuesPayload(
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

        if isinstance(response, self._call_result.MeterValuesPayload):
            logger.info("response %s." % response)

    def send_security_event_notification(self):
        request = self._call.SecurityEventNotificationPayload(
            type="test_type",
            timestamp=utcnow(),
            tech_info="tech_info"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.SecurityEventNotificationPayload):
            logger.info("response %s." % response)

    def send_sign_certificate(self):
        request = self._call.SignCertificatePayload(
            csr="csr"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.SignCertificatePayload):
            logger.info("status %s." % response.status)

    def send_signed_firmware_status_notification(self):
        request = self._call.SignedFirmwareStatusNotificationPayload(
            status=FirmwareStatus.downloaded,
            request_id=123,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.SignedFirmwareStatusNotificationPayload):
            logger.info("response %s." % response)

    def send_start_transaction(self):
        request = self._call.StartTransactionPayload(
            connector_id=123,
            id_tag="id_tag",
            meter_start=456,
            timestamp=utcnow(),
            reservation_id=789,
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.StartTransactionPayload):
            logger.info("transaction_id %s." % response.transaction_id)
            logger.info("id_tag_info %s." % response.id_tag_info)

    def send_stop_transaction(self):
        request = self._call.StopTransactionPayload(
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

        if isinstance(response, self._call_result.StopTransactionPayload):
            logger.info("id_tag_info %s." % response.id_tag_info)

    def send_status_notification(self):
        request = self._call.StatusNotificationPayload(
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

        if isinstance(response, self._call_result.StatusNotificationPayload):
            logger.info("response %s." % response)

    def send_data_transfer(self):
        request = self._call.DataTransferPayload(
            vendor_id="vendor_id",
            message_id="message_id",
            data="data"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if isinstance(response, self._call_result.DataTransferPayload):
            logger.info("status %s." % response.status)
            logger.info("data %s." % response.data)

    @on(Action.CancelReservation)
    def on_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))

        return self._call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )

    @on(Action.CertificateSigned)
    def on_certificate_signed(self, certificate_chain):
        logger.info("certificate_chain %s" % (certificate_chain))

        return self._call_result.CertificateSignedPayload(
            status=CertificateSignedStatus.accepted
        )

    @on(Action.ChangeAvailability)
    def on_change_availability(self, connector_id, type):
        logger.info("connector_id %s, type %s" % (connector_id, type))

        return self._call_result.ChangeAvailabilityPayload(
            status=AvailabilityStatus.accepted
        )

    @on(Action.ChangeConfiguration)
    def on_change_configuration(self, key, value):
        logger.info("key %s, value %s" % (key, value))

        return self._call_result.ChangeConfigurationPayload(
            status=ConfigurationStatus.accepted
        )

    @on(Action.ClearCache)
    def on_clear_cache(self, **kwargs):
        logger.info("kwargs %s" % repr(kwargs))

        return self._call_result.ClearCachePayload(
            status=ClearCacheStatus.accepted
        )

    @on(Action.ClearChargingProfile)
    def on_clear_charging_profile(self, **kwargs):
        logger.info(
            "id %s, connector_id %s, charging_profile_purpose %s, stack_level %s" % (
                kwargs.get("id"), kwargs.get("connector_id"),
                kwargs.get("charging_profile_purpose"), kwargs.get("stack_level")
            )
        )

        return self._call_result.ClearChargingProfilePayload(
            status=ClearChargingProfileStatus.accepted
        )

    @on(Action.DeleteCertificate)
    def on_delete_certificate(self, certificate_hash_data):
        logger.info("certificate_hash_data %s" % repr(certificate_hash_data))

        return self._call_result.DeleteCertificatePayload(
            status=DeleteCertificateStatus.accepted
        )

    @on(Action.ExtendedTriggerMessage)
    def on_extended_trigger_message(self, requested_message, **kwargs):
        logger.info("requested_message %s, connector_id %s" % (requested_message, kwargs.get("connector_id")))

        return self._call_result.ExtendedTriggerMessagePayload(
            status=TriggerMessageStatus.accepted
        )

    @on(Action.GetCompositeSchedule)
    def on_get_composite_schedule(self, connector_id, duration, **kwargs):
        logger.info(
            "connector_id %s, duration %s, charging_rate_unit %s" % (
                connector_id, duration, kwargs.get("charging_rate_unit")
            )
        )

        return self._call_result.GetCompositeSchedulePayload(
            status=GetCompositeScheduleStatus.accepted,
            connector_id=connector_id,
            schedule_start=utcnow(),
            charging_schedule=ChargingSchedule(
                charging_rate_unit=ChargingRateUnitType.watts,
                charging_schedule_period=[
                    ChargingSchedulePeriod(start_period=1, limit=2.2, number_phases=3),
                    ChargingSchedulePeriod(start_period=1, limit=2.2, number_phases=3),
                    ChargingSchedulePeriod(start_period=1, limit=2.2, number_phases=3)
                ],
                duration=duration,
                start_schedule=utcnow(),
                min_charging_rate=1.0,
            ),
        )

    @on(Action.GetConfiguration)
    def on_get_configuration(self, **kwargs):
        logger.info("key %s" % kwargs.get("key"))

        return self._call_result.GetConfigurationPayload(
            configuration_key=[
                KeyValue(key="Config1", readonly=True, value="Value1"),
                KeyValue(key="Config2", readonly=False, value="Value2")
            ],
            unknown_key=["Config3"]
        )

    @on(Action.GetDiagnostics)
    def on_get_diagnostics(self, location, **kwargs):
        logger.info("location %s" % location)
        logger.info("retries %s" % kwargs.get("retries"))
        logger.info("retry_interval %s" % kwargs.get("retry_interval"))
        logger.info("start_time %s" % kwargs.get("start_time"))
        logger.info("stop_time %s" % kwargs.get("stop_time"))

        return self._call_result.GetDiagnosticsPayload(
            file_name="diagnostics file"
        )

    @on(Action.GetInstalledCertificateIds)
    def on_get_installed_certificate_ids(self, certificate_type):
        logger.info("certificate_type %s" % certificate_type)

        return self._call_result.GetInstalledCertificateIdsPayload(
            status=GetInstalledCertificateStatus.accepted,
            certificate_hash_data=[
                CertificateHashData(
                    hash_algorithm=HashAlgorithm.sha256,
                    issuer_name_hash="issuer_name_hash",
                    issuer_key_hash="issuer_key_hash",
                    serial_number="serial_number",
                )
            ]
        )

    @on(Action.GetLocalListVersion)
    def on_get_local_list_version(self):
        logger.info("on_get_local_list_version")

        return self._call_result.GetLocalListVersionPayload(
            list_version=123
        )

    @on(Action.GetLog)
    def on_get_log(self, log, log_type, request_id, **kwargs):
        logger.info("log %s" % str(log))
        logger.info("log_type %s" % log_type)
        logger.info("request_id %s" % request_id)
        logger.info("retries %s" % kwargs.get("retries"))
        logger.info("retry_interval %s" % kwargs.get("retry_interval"))

        return self._call_result.GetLogPayload(
            status=LogStatus.accepted,
            filename="logfilename"
        )

    @on(Action.InstallCertificate)
    def on_install_certificate(self, certificate_type, certificate):
        logger.info("certificate_type %s" % certificate_type)
        logger.info("certificate %s" % certificate)

        return self._call_result.InstallCertificatePayload(
            status=CertificateStatus.accepted,
        )

    @on(Action.RemoteStartTransaction)
    def on_remote_start_transaction(self, id_tag, **kwargs):
        logger.info("id_tag %s" % id_tag)
        logger.info("connector_id %s" % kwargs.get("connector_id"))
        logger.info("charging_profile %s" % kwargs.get("charging_profile"))

        return self._call_result.RemoteStartTransactionPayload(
            status=RemoteStartStopStatus.accepted,
        )

    @on(Action.RemoteStopTransaction)
    def on_remote_stop_transaction(self, transaction_id):
        logger.info("transaction_id %s" % transaction_id)

        return self._call_result.RemoteStopTransactionPayload(
            status=RemoteStartStopStatus.accepted,
        )

    @on(Action.ReserveNow)
    def on_reserve_now(self, connector_id, expiry_date, id_tag, reservation_id, **kwargs):
        logger.info("connector_id %s" % connector_id)
        logger.info("expiry_date %s" % expiry_date)
        logger.info("id_tag %s" % id_tag)
        logger.info("reservation_id %s" % reservation_id)
        logger.info("parent_id_tag %s" % kwargs.get("parent_id_tag"))

        return self._call_result.ReserveNowPayload(
            status=ReservationStatus.accepted,
        )

    @on(Action.Reset)
    def on_reset(self, type):
        logger.info("type %s" % type)

        return self._call_result.ResetPayload(
            status=ResetStatus.accepted,
        )

    @on(Action.SendLocalList)
    def on_send_local_list(self, list_version, update_type, **kwargs):
        logger.info("list_version %s" % list_version)
        logger.info("update_type %s" % update_type)
        logger.info("local_authorization_list %s" % kwargs.get("local_authorization_list"))

        return self._call_result.SendLocalListPayload(
            status=UpdateStatus.accepted,
        )

    @on(Action.SetChargingProfile)
    def on_set_charging_profile(self, connector_id, cs_charging_profiles):
        logger.info("connector_id %s" % connector_id)
        logger.info("cs_charging_profiles %s" % cs_charging_profiles)

        return self._call_result.SetChargingProfilePayload(
            status=ChargingProfileStatus.accepted,
        )

    @on(Action.SignedUpdateFirmware)
    def on_signed_update_firmware(self, request_id, firmware, **kwargs):
        logger.info("request_id %s" % request_id)
        logger.info("firmware %s" % firmware)
        logger.info("retries %s" % kwargs.get("retries"))
        logger.info("retry_interval %s" % kwargs.get("retry_interval"))

        return self._call_result.SignedUpdateFirmwarePayload(
            status=UpdateFirmwareStatus.accepted,
        )

    @on(Action.TriggerMessage)
    def on_trigger_message(self, requested_message, **kwargs):
        logger.info("requested_message %s" % requested_message)
        logger.info("connector_id %s" % kwargs.get("connector_id"))

        return self._call_result.TriggerMessagePayload(
            status=TriggerMessageStatus.accepted,
        )

    @on(Action.UnlockConnector)
    def on_unlock_connector(self, connector_id):
        logger.info("connector_id %s" % connector_id)

        return self._call_result.UnlockConnectorPayload(
            status=UnlockStatus.unlocked,
        )

    @on(Action.UpdateFirmware)
    def on_update_firmware(self, location, retrieve_date, **kwargs):
        logger.info("location %s" % location)
        logger.info("retrieve_date %s" % retrieve_date)
        logger.info("retries %s" % kwargs.get("retries"))
        logger.info("retry_interval %s" % kwargs.get("retry_interval"))

        return self._call_result.UpdateFirmwarePayload()

    @on(Action.DataTransfer)
    def on_data_transfer(self, vendor_id, **kwargs):
        logger.info("vendor_id %s" % vendor_id)
        logger.info("message_id %s" % kwargs.get("message_id"))
        logger.info("data %s" % kwargs.get("data"))

        return self._call_result.DataTransferPayload(
            status=DataTransferStatus.accepted,
            data="data"
        )


def main():
    logger.debug("_thread.get_heap_size() %s, gc.mem_alloc() %s" % (_thread.get_heap_size(), gc.mem_alloc()))
    ws = uwebsocket.Client.connect(
        "ws://106.15.58.32:31499/%s" % IMEI,
        # "ws://xxx.xxx.xxx.xxx:xxxx/868543063288971",
        headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
        debug=False
    )
    logger.debug("_thread.get_heap_size() %s, gc.mem_alloc() %s" % (_thread.get_heap_size(), gc.mem_alloc()))
    cp = ChargePoint(IMEI, ws)
    logger.debug("_thread.get_heap_size() %s, gc.mem_alloc() %s" % (_thread.get_heap_size(), gc.mem_alloc()))

    _thread.stack_size(0x1000)
    tid = _thread.start_new_thread(cp.start, ())
    logger.debug("cp start tid %s" % tid)
    utime.sleep_ms(200)
    logger.debug("_thread.get_heap_size() %s, gc.mem_alloc() %s" % (_thread.get_heap_size(), gc.mem_alloc()))

    cp_send_fun = [i for i in dir(cp) if i.startswith("send_")]
    logger.debug("cp_send_fun %s" % repr(cp_send_fun))
    logger.debug("_thread.get_heap_size() %s, gc.mem_alloc() %s" % (_thread.get_heap_size(), gc.mem_alloc()))
    for name in cp_send_fun:
        getattr(cp, name)()
        logger.debug("_thread.get_heap_size() %s, gc.mem_alloc() %s" % (_thread.get_heap_size(), gc.mem_alloc()))
        utime.sleep_ms(100)
        break


if __name__ == "__main__":
    main()
