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
@file      :v16_server_demo.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2024-03-25 10:43:41
@copyright :Copyright (c) 2024
"""

import asyncio
import logging
import websockets
from datetime import datetime

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result
from ocpp.v16.enums import (
    Action,
    RegistrationStatus,
    CancelReservationStatus,
    CertificateSignedStatus,
    AvailabilityStatus,
    ConfigurationStatus,
    ClearCacheStatus,
    ClearChargingProfileStatus,
    DeleteCertificateStatus,
    TriggerMessageStatus,
    GetCompositeScheduleStatus,
    ChargingRateUnitType,
    GetInstalledCertificateStatus,
    HashAlgorithm,
    LogStatus,
    CertificateStatus,
    RemoteStartStopStatus,
    ReservationStatus,
    ResetStatus,
    UpdateStatus,
    ChargingProfileStatus,
    UpdateFirmwareStatus,
    UnlockStatus,
    AuthorizationStatus,
    GenericStatus,
    DataTransferStatus,
)
from ocpp.v16.datatypes import (
    ChargingSchedule,
    ChargingSchedulePeriod,
    KeyValue,
    CertificateHashData,
    IdTagInfo,
)

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    @on(Action.BootNotification)
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        logging.info("charge_point_model %s, charge_point_vendor %s, kwargs %s" % (charge_point_model, charge_point_vendor, repr(kwargs)))
        assert charge_point_vendor == "Alfen BV"
        assert charge_point_model == "ICU Eve Mini"
        assert kwargs["firmware_version"] == "#1:3.4.0-2990#N:217H;1.0-223"

        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.CancelReservation)
    async def on_cancel_reservation(self, reservation_id):
        logging.info("reservation_id %s" % (reservation_id))

        return call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )

    @on(Action.CertificateSigned)
    async def on_certificate_signed(self, certificate_chain):
        logging.info("certificate_chain %s" % (certificate_chain))

        return call_result.CertificateSignedPayload(
            status=CertificateSignedStatus.accepted
        )

    @on(Action.ChangeAvailability)
    async def on_change_availability(self, connector_id, type):
        logging.info("connector_id %s, type %s" % (connector_id, type))

        return call_result.ChangeAvailabilityPayload(
            status=AvailabilityStatus.accepted
        )

    @on(Action.ChangeConfiguration)
    async def on_change_configuration(self, key, value):
        logging.info("key %s, value %s" % (key, value))

        return call_result.ChangeConfigurationPayload(
            status=ConfigurationStatus.accepted
        )

    @on(Action.ClearCache)
    async def on_clear_cache(self, **kwargs):
        logging.info("kwargs %s" % repr(kwargs))

        return call_result.ClearCachePayload(
            status=ClearCacheStatus.accepted
        )

    @on(Action.ClearChargingProfile)
    async def on_clear_charging_profile(self, **kwargs):
        logging.info(
            "id %s, connector_id %s, charging_profile_purpose %s, stack_level %s" % (
                kwargs.get("id"), kwargs.get("connector_id"),
                kwargs.get("charging_profile_purpose"), kwargs.get("stack_level")
            )
        )

        return call_result.ClearChargingProfilePayload(
            status=ClearChargingProfileStatus.accepted
        )

    @on(Action.DeleteCertificate)
    async def on_delete_certificate(self, certificate_hash_data):
        logging.info("certificate_hash_data %s" % repr(certificate_hash_data))

        return call_result.DeleteCertificatePayload(
            status=DeleteCertificateStatus.accepted
        )

    @on(Action.ExtendedTriggerMessage)
    async def on_extended_trigger_message(self, requested_message, **kwargs):
        logging.info("requested_message %s, connector_id %s" % (requested_message, kwargs.get("connector_id")))

        return call_result.ExtendedTriggerMessagePayload(
            status=TriggerMessageStatus.accepted
        )

    @on(Action.GetCompositeSchedule)
    async def on_get_composite_schedule(self, connector_id, duration, **kwargs):
        logging.info(
            "connector_id %s, duration %s, charging_rate_unit %s" % (
                connector_id, duration, kwargs.get("charging_rate_unit")
            )
        )

        return call_result.GetCompositeSchedulePayload(
            status=GetCompositeScheduleStatus.accepted,
            connector_id=connector_id,
            schedule_start=datetime.utcnow().isoformat(),
            charging_schedule=ChargingSchedule(
                charging_rate_unit=ChargingRateUnitType.watts,
                charging_schedule_period=[
                    ChargingSchedulePeriod(start_period=1, limit=2.2, number_phases=3),
                    ChargingSchedulePeriod(start_period=1, limit=2.2, number_phases=3),
                    ChargingSchedulePeriod(start_period=1, limit=2.2, number_phases=3)
                ],
                duration=duration,
                start_schedule=datetime.utcnow().isoformat(),
                min_charging_rate=1.0,
            ),
        )

    @on(Action.GetConfiguration)
    async def on_get_configuration(self, **kwargs):
        logging.info("key %s" % kwargs.get("key"))

        return call_result.GetConfigurationPayload(
            configuration_key=[
                KeyValue(key="Config1", readonly=True, value="Value1"),
                KeyValue(key="Config2", readonly=False, value="Value2")
            ],
            unknown_key=["Config3"]
        )

    @on(Action.GetDiagnostics)
    async def on_get_diagnostics(self, location, **kwargs):
        logging.info("location %s" % location)
        logging.info("retries %s" % kwargs.get("retries"))
        logging.info("retry_interval %s" % kwargs.get("retry_interval"))
        logging.info("start_time %s" % kwargs.get("start_time"))
        logging.info("stop_time %s" % kwargs.get("stop_time"))

        return call_result.GetDiagnosticsPayload(
            file_name="diagnostics file"
        )

    @on(Action.GetInstalledCertificateIds)
    async def on_get_installed_certificate_ids(self, certificate_type):
        logging.info("certificate_type %s" % certificate_type)

        return call_result.GetInstalledCertificateIdsPayload(
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
    async def on_get_local_list_version(self):
        logging.info("on_get_local_list_version")

        return call_result.GetLocalListVersionPayload(
            list_version=123
        )

    @on(Action.GetLog)
    async def on_get_log(self, log, log_type, request_id, **kwargs):
        logging.info("log %s" % str(log))
        logging.info("log_type %s" % log_type)
        logging.info("request_id %s" % request_id)
        logging.info("retries %s" % kwargs.get("retries"))
        logging.info("retry_interval %s" % kwargs.get("retry_interval"))

        return call_result.GetLogPayload(
            status=LogStatus.accepted,
            filename="logfilename"
        )

    @on(Action.InstallCertificate)
    async def on_install_certificate(self, certificate_type, certificate):
        logging.info("certificate_type %s" % certificate_type)
        logging.info("certificate %s" % certificate)

        return call_result.InstallCertificatePayload(
            status=CertificateStatus.accepted,
        )

    @on(Action.RemoteStartTransaction)
    async def on_remote_start_transaction(self, id_tag, **kwargs):
        logging.info("id_tag %s" % id_tag)
        logging.info("connector_id %s" % kwargs.get("connector_id"))
        logging.info("charging_profile %s" % kwargs.get("charging_profile"))

        return call_result.RemoteStartTransactionPayload(
            status=RemoteStartStopStatus.accepted,
        )

    @on(Action.RemoteStopTransaction)
    async def on_remote_stop_transaction(self, transaction_id):
        logging.info("transaction_id %s" % transaction_id)

        return call_result.RemoteStopTransactionPayload(
            status=RemoteStartStopStatus.accepted,
        )

    @on(Action.ReserveNow)
    async def on_reserve_now(self, connector_id, expiry_date, id_tag, reservation_id, **kwargs):
        logging.info("connector_id %s" % connector_id)
        logging.info("expiry_date %s" % expiry_date)
        logging.info("id_tag %s" % id_tag)
        logging.info("reservation_id %s" % reservation_id)
        logging.info("parent_id_tag %s" % kwargs.get("parent_id_tag"))

        return call_result.ReserveNowPayload(
            status=ReservationStatus.accepted,
        )

    @on(Action.Reset)
    async def on_reset(self, type):
        logging.info("type %s" % type)

        return call_result.ResetPayload(
            status=ResetStatus.accepted,
        )

    @on(Action.SendLocalList)
    async def on_send_local_list(self, list_version, update_type, **kwargs):
        logging.info("list_version %s" % list_version)
        logging.info("update_type %s" % update_type)
        logging.info("local_authorization_list %s" % kwargs.get("local_authorization_list"))

        return call_result.SendLocalListPayload(
            status=UpdateStatus.accepted,
        )

    @on(Action.SetChargingProfile)
    async def on_set_charging_profile(self, connector_id, cs_charging_profiles):
        logging.info("connector_id %s" % connector_id)
        logging.info("cs_charging_profiles %s" % cs_charging_profiles)

        return call_result.SetChargingProfilePayload(
            status=ChargingProfileStatus.accepted,
        )

    @on(Action.SignedUpdateFirmware)
    async def on_signed_update_firmware(self, request_id, firmware, **kwargs):
        logging.info("request_id %s" % request_id)
        logging.info("firmware %s" % firmware)
        logging.info("retries %s" % kwargs.get("retries"))
        logging.info("retry_interval %s" % kwargs.get("retry_interval"))

        return call_result.SignedUpdateFirmwarePayload(
            status=UpdateFirmwareStatus.accepted,
        )

    @on(Action.TriggerMessage)
    async def on_trigger_message(self, requested_message, **kwargs):
        logging.info("requested_message %s" % requested_message)
        logging.info("connector_id %s" % kwargs.get("connector_id"))

        return call_result.TriggerMessagePayload(
            status=TriggerMessageStatus.accepted,
        )

    @on(Action.UnlockConnector)
    async def on_unlock_connector(self, connector_id):
        logging.info("connector_id %s" % connector_id)

        return call_result.UnlockConnectorPayload(
            status=UnlockStatus.accepted,
        )

    @on(Action.UpdateFirmware)
    async def on_update_firmware(self, location, retrieve_date, **kwargs):
        logging.info("location %s" % location)
        logging.info("retrieve_date %s" % retrieve_date)
        logging.info("retries %s" % kwargs.get("retries"))
        logging.info("retry_interval %s" % kwargs.get("retry_interval"))

        return call_result.UpdateFirmwarePayload()

    @on(Action.Authorize)
    async def on_authorize(self, id_tag):
        logging.info("id_tag %s" % id_tag)

        return call_result.AuthorizePayload(
            id_tag_info=IdTagInfo(
                status=AuthorizationStatus.accepted,
                parent_id_tag="parent_id_tag",
                expiry_date=datetime.utcnow().isoformat()
            )
        )

    @on(Action.DiagnosticsStatusNotification)
    async def on_diagnostics_status_notification(self, status):
        logging.info("status %s" % status)

        return call_result.DiagnosticsStatusNotificationPayload()

    @on(Action.FirmwareStatusNotification)
    async def on_firmware_status_notification(self, status):
        logging.info("status %s" % status)

        return call_result.FirmwareStatusNotificationPayload()

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        logging.info("on_heartbeat")

        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )

    @on(Action.LogStatusNotification)
    async def on_log_status_notification(self, status, request_id):
        logging.info("status %s" % status)
        logging.info("request_id %s" % request_id)

        return call_result.LogStatusNotificationPayload()

    @on(Action.MeterValues)
    async def on_meter_values(self, connector_id, meter_value, **kwargs):
        logging.info("connector_id %s" % connector_id)
        logging.info("meter_value %s" % meter_value)
        logging.info("transaction_id %s" % kwargs.get("transaction_id"))

        return call_result.MeterValuesPayload()

    @on(Action.SecurityEventNotification)
    async def on_security_event_notification(self, type, timestamp, **kwargs):
        logging.info("type %s" % type)
        logging.info("timestamp %s" % timestamp)
        logging.info("tech_info %s" % kwargs.get("tech_info"))

        return call_result.SecurityEventNotificationPayload()

    @on(Action.SignCertificate)
    async def on_sign_certificate(self, csr):
        logging.info("csr %s" % csr)

        return call_result.SignCertificatePayload(
            status=GenericStatus.accepted
        )

    @on(Action.SignedFirmwareStatusNotification)
    async def on_signed_firmware_status_notification(self, status, request_id):
        logging.info("status %s" % status)
        logging.info("request_id %s" % request_id)

        return call_result.SignedFirmwareStatusNotificationPayload()

    @on(Action.StartTransaction)
    async def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp, **kwargs):
        logging.info("connector_id %s" % connector_id)
        logging.info("id_tag %s" % id_tag)
        logging.info("meter_start %s" % meter_start)
        logging.info("timestamp %s" % timestamp)
        logging.info("reservation_id %s" % kwargs.get("reservation_id"))

        return call_result.StartTransactionPayload(
            transaction_id=123,
            id_tag_info=IdTagInfo(
                status=AuthorizationStatus.accepted,
                parent_id_tag="parent_id_tag",
                expiry_date=datetime.utcnow().isoformat()
            )
        )

    @on(Action.StopTransaction)
    async def on_stop_transaction(self, meter_stop, timestamp, transaction_id, **kwargs):
        logging.info("meter_stop %s" % meter_stop)
        logging.info("timestamp %s" % timestamp)
        logging.info("transaction_id %s" % transaction_id)
        logging.info("reason %s" % kwargs.get("reason"))
        logging.info("id_tag %s" % kwargs.get("id_tag"))
        logging.info("transaction_data %s" % kwargs.get("transaction_data"))

        return call_result.StopTransactionPayload(
            id_tag_info=IdTagInfo(
                status=AuthorizationStatus.accepted,
                parent_id_tag="parent_id_tag",
                expiry_date=datetime.utcnow().isoformat()
            )
        )

    @on(Action.StatusNotification)
    async def on_status_notification(self, connector_id, error_code, status, **kwargs):
        logging.info("connector_id %s" % connector_id)
        logging.info("error_code %s" % error_code)
        logging.info("status %s" % status)
        logging.info("timestamp %s" % kwargs.get("timestamp"))
        logging.info("info %s" % kwargs.get("info"))
        logging.info("vendor_id %s" % kwargs.get("vendor_id"))
        logging.info("vendor_error_code %s" % kwargs.get("vendor_error_code"))

        return call_result.StatusNotificationPayload()

    @on(Action.DataTransfer)
    async def on_data_transfer(self, vendor_id, **kwargs):
        logging.info("vendor_id %s" % vendor_id)
        logging.info("message_id %s" % kwargs.get("message_id"))
        logging.info("data %s" % kwargs.get("data"))

        return call_result.DataTransferPayload(
            status=DataTransferStatus.accepted,
            data="data"
        )


async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers[
            'Sec-WebSocket-Protocol']
        logging.info("requested_protocols %s" % requested_protocols)
    except KeyError:
        logging.info("Client hasn't requested any Subprotocol. Closing Connection")
        return await websocket.close()

    if websocket.subprotocol == requested_protocols:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports  %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()

    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        31499,
        subprotocols=['ocpp1.6.0']
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
