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
    # LogStatus,
    # CertificateStatus,
    # RemoteStartStopStatus,
    # ReservationStatus,
    # ResetStatus,
    # UpdateStatus,
    # ChargingProfileStatus,
    # UpdateFirmwareStatus,
    # UnlockStatus,
    AuthorizationStatus,
    GenericStatus,
    DataTransferStatus,
    AvailabilityType,
    ChargingProfilePurposeType,
    MessageTrigger,
    CertificateUse,
    Log,
    ChargingProfileKindType,
    RecurrencyKind,
    ResetType,
    UpdateType,
)
from ocpp.v16.datatypes import (
    ChargingSchedule,
    ChargingSchedulePeriod,
    # KeyValue,
    CertificateHashData,
    IdTagInfo,
    LogParameters,
    ChargingProfile,
    AuthorizationData,
    Firmware,
)

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    @on(Action.Authorize)
    async def on_authorize(self, id_tag):
        logging.info("id_tag %s" % id_tag)

        return self._call_result.AuthorizePayload(
            id_tag_info=IdTagInfo(
                status=AuthorizationStatus.accepted,
                parent_id_tag="parent_id_tag",
                expiry_date=datetime.utcnow().isoformat()
            )
        )

    @on(Action.BootNotification)
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        logging.info("charge_point_model %s, charge_point_vendor %s, kwargs %s" % (charge_point_model, charge_point_vendor, repr(kwargs)))
        assert charge_point_vendor == "Alfen BV"
        assert charge_point_model == "ICU Eve Mini"
        assert kwargs["firmware_version"] == "#1:3.4.0-2990#N:217H;1.0-223"

        return self._call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.DiagnosticsStatusNotification)
    async def on_diagnostics_status_notification(self, status):
        logging.info("status %s" % status)

        return self._call_result.DiagnosticsStatusNotificationPayload()

    @on(Action.FirmwareStatusNotification)
    async def on_firmware_status_notification(self, status):
        logging.info("status %s" % status)

        return self._call_result.FirmwareStatusNotificationPayload()

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        logging.info("on_heartbeat")

        return self._call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )

    @on(Action.LogStatusNotification)
    async def on_log_status_notification(self, status, request_id):
        logging.info("status %s" % status)
        logging.info("request_id %s" % request_id)

        return self._call_result.LogStatusNotificationPayload()

    @on(Action.MeterValues)
    async def on_meter_values(self, connector_id, meter_value, **kwargs):
        logging.info("connector_id %s" % connector_id)
        logging.info("meter_value %s" % meter_value)
        logging.info("transaction_id %s" % kwargs.get("transaction_id"))

        return self._call_result.MeterValuesPayload()

    @on(Action.SecurityEventNotification)
    async def on_security_event_notification(self, type, timestamp, **kwargs):
        logging.info("type %s" % type)
        logging.info("timestamp %s" % timestamp)
        logging.info("tech_info %s" % kwargs.get("tech_info"))

        return self._call_result.SecurityEventNotificationPayload()

    @on(Action.SignCertificate)
    async def on_sign_certificate(self, csr):
        logging.info("csr %s" % csr)

        return self._call_result.SignCertificatePayload(
            status=GenericStatus.accepted
        )

    @on(Action.SignedFirmwareStatusNotification)
    async def on_signed_firmware_status_notification(self, status, request_id):
        logging.info("status %s" % status)
        logging.info("request_id %s" % request_id)

        return self._call_result.SignedFirmwareStatusNotificationPayload()

    @on(Action.StartTransaction)
    async def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp, **kwargs):
        logging.info("connector_id %s" % connector_id)
        logging.info("id_tag %s" % id_tag)
        logging.info("meter_start %s" % meter_start)
        logging.info("timestamp %s" % timestamp)
        logging.info("reservation_id %s" % kwargs.get("reservation_id"))

        return self._call_result.StartTransactionPayload(
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

        return self._call_result.StopTransactionPayload(
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

        return self._call_result.StatusNotificationPayload()

    @on(Action.DataTransfer)
    async def on_data_transfer(self, vendor_id, **kwargs):
        logging.info("vendor_id %s" % vendor_id)
        logging.info("message_id %s" % kwargs.get("message_id"))
        logging.info("data %s" % kwargs.get("data"))

        return self._call_result.DataTransferPayload(
            status=DataTransferStatus.accepted,
            data="data"
        )

    async def send_cancel_reservation(self):
        request = self._call.CancelReservationPayload(
            reservation_id=123
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == CancelReservationStatus.accepted:
            logging.info("Cancel reservation status %s." % response.status)

    async def send_certificate_signed(self):
        request = self._call.CertificateSignedPayload(
            certificate_chain="TEST_CERTIFICATE_CHAIN"
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == CertificateSignedStatus.accepted:
            logging.info("Certificate signed status %s." % response.status)

    async def send_change_availability(self):
        request = self._call.ChangeAvailabilityPayload(
            connector_id=123,
            type=AvailabilityType.inoperative
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == AvailabilityStatus.accepted:
            logging.info("Change availability status %s." % response.status)

    async def send_change_configuration(self):
        request = self._call.ChangeConfigurationPayload(
            key="period",
            value="30"
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == ConfigurationStatus.accepted:
            logging.info("Change configuration status %s." % response.status)

    async def send_clear_cache(self):
        request = self._call.ClearCachePayload()
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == ClearCacheStatus.accepted:
            logging.info("Clear cache status %s." % response.status)

    async def send_clear_charging_profile(self):
        request = self._call.ClearChargingProfilePayload(
            id=123,
            connector_id=456,
            charging_profile_purpose=ChargingProfilePurposeType.charge_point_max_profile,
            stack_level=789,
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == ClearChargingProfileStatus.accepted:
            logging.info("Clear charging profile status %s." % response.status)

    async def send_delete_certificate(self):
        request = self._call.DeleteCertificatePayload(
            certificate_hash_data=CertificateHashData(
                hash_algorithm=HashAlgorithm.sha256,
                issuer_name_hash="issuer_name_hash",
                issuer_key_hash="issuer_key_hash",
                serial_number="serial_number",
            )
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == DeleteCertificateStatus.accepted:
            logging.info("Delete certificate status %s." % response.status)

    async def send_extended_trigger_message(self):
        request = self._call.ExtendedTriggerMessagePayload(
            requested_message=MessageTrigger.boot_notification,
            connector_id=123,
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == TriggerMessageStatus.accepted:
            logging.info("Extended trigger message status %s." % response.status)

    async def send_get_composite_schedule(self):
        request = self._call.GetCompositeSchedulePayload(
            connector_id=123,
            duration=10,
            charging_rate_unit=ChargingRateUnitType.watts,
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == GetCompositeScheduleStatus.accepted:
            logging.info("Extended trigger message status %s." % response.status)
            logging.info(
                "connector_id %s, schedule_start %s, charging_schedule %s" % (
                    response.connector_id, response.schedule_start, response.charging_schedule
                )
            )

    async def send_get_configuration(self):
        request = self._call.GetConfigurationPayload(
            key=["Config1", "Config2", "Config3"]
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.GetConfigurationPayload):
            logging.info("configuration_key %s." % response.configuration_key)
            logging.info("unknown_key %s." % response.unknown_key)

    async def send_get_diagnostics(self):
        request = self._call.GetDiagnosticsPayload(
            location="location",
            retries=10,
            retry_interval=10,
            start_time=datetime.utcnow().isoformat(),
            stop_time=datetime.utcnow().isoformat(),
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.GetDiagnosticsPayload):
            logging.info("file_name %s." % response.file_name)

    async def send_get_installed_certificate_ids(self):
        request = self._call.GetInstalledCertificateIdsPayload(
            certificate_type=CertificateUse.central_system_root_certificate
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if response.status == GetInstalledCertificateStatus.accepted:
            logging.info("certificate_hash_data %s." % response.certificate_hash_data)

    async def send_get_local_list_version(self):
        request = self._call.GetLocalListVersionPayload()
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.GetLocalListVersionPayload):
            logging.info("list_version %s." % response.list_version)

    async def send_get_log(self):
        request = self._call.GetLogPayload(
            log=LogParameters(
                remote_location="remote_location",
                oldest_timestamp=datetime.utcnow().isoformat(),
                latest_timestamp=datetime.utcnow().isoformat()
            ),
            log_type=Log.diagnostics_log,
            request_id=123,
            retries=3,
            retry_interval=10,
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.GetLogPayload):
            logging.info("status %s." % response.status)
            logging.info("filename %s." % response.filename)

    async def send_install_certificate(self):
        request = self._call.InstallCertificatePayload(
            certificate_type=CertificateUse.central_system_root_certificate,
            certificate="certificate"
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.InstallCertificatePayload):
            logging.info("status %s." % response.status)

    async def send_remote_start_transaction(self):
        request = self._call.RemoteStartTransactionPayload(
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
                    start_schedule=datetime.utcnow().isoformat(),
                    min_charging_rate=20.0
                ),
                transaction_id=789,
                recurrency_kind=RecurrencyKind.daily,
                valid_from=datetime.utcnow().isoformat(),
                valid_to=datetime.utcnow().isoformat(),
            ),
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.RemoteStartTransactionPayload):
            logging.info("status %s." % response.status)

    async def send_remote_stop_transaction(self):
        request = self._call.RemoteStopTransactionPayload(
            transaction_id=123,
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.RemoteStopTransactionPayload):
            logging.info("status %s." % response.status)

    async def send_reserve_now(self):
        request = self._call.ReserveNowPayload(
            connector_id=123,
            expiry_date=datetime.utcnow().isoformat(),
            id_tag="id_tag",
            reservation_id=456,
            parent_id_tag="parent_id_tag",
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.ReserveNowPayload):
            logging.info("status %s." % response.status)

    async def send_reset(self):
        request = self._call.ResetPayload(
            type=ResetType.hard
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.ResetPayload):
            logging.info("status %s." % response.status)

    async def send_send_local_list(self):
        request = self._call.SendLocalListPayload(
            list_version=123,
            update_type=UpdateType.differential,
            local_authorization_list=[
                AuthorizationData(
                    id_tag="id_tag",
                    id_tag_info=IdTagInfo(
                        status=AuthorizationStatus.accepted,
                        parent_id_tag="parent_id_tag",
                        expiry_date=datetime.utcnow().isoformat()
                    )
                ),
                AuthorizationData(
                    id_tag="id_tag",
                    id_tag_info=IdTagInfo(
                        status=AuthorizationStatus.accepted,
                        parent_id_tag="parent_id_tag",
                        expiry_date=datetime.utcnow().isoformat()
                    )
                ),
            ],
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.SendLocalListPayload):
            logging.info("status %s." % response.status)

    async def send_set_charging_profile(self):
        request = self._call.SetChargingProfilePayload(
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
                    start_schedule=datetime.utcnow().isoformat(),
                    min_charging_rate=20.0
                ),
                transaction_id=789,
                recurrency_kind=RecurrencyKind.daily,
                valid_from=datetime.utcnow().isoformat(),
                valid_to=datetime.utcnow().isoformat(),
            )
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.SetChargingProfilePayload):
            logging.info("status %s." % response.status)

    async def send_signed_update_firmware(self):
        request = self._call.SignedUpdateFirmwarePayload(
            request_id=123,
            firmware=Firmware(
                location="location",
                retrieve_date_time=datetime.utcnow().isoformat(),
                signing_certificate="signing_certificate",
                signature="signature",
                install_date_time=datetime.utcnow().isoformat()
            ),
            retries=3,
            retry_interval=10
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.SignedUpdateFirmwarePayload):
            logging.info("status %s." % response.status)

    async def send_trigger_message(self):
        request = self._call.TriggerMessagePayload(
            requested_message=MessageTrigger.boot_notification,
            connector_id=123
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.TriggerMessagePayload):
            logging.info("status %s." % response.status)

    async def send_unlock_connector(self):
        request = self._call.UnlockConnectorPayload(
            connector_id=123
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.UnlockConnectorPayload):
            logging.info("status %s." % response.status)

    async def send_update_firmware(self):
        request = self._call.UpdateFirmwarePayload(
            location="http://www.quectel.com",
            retrieve_date=datetime.utcnow().isoformat(),
            retries=3,
            retry_interval=10,
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.UpdateFirmwarePayload):
            logging.info("response %s." % response)

    async def send_data_transfer(self):
        request = self._call.DataTransferPayload(
            vendor_id="vendor_id",
            message_id="message_id",
            data="data"
        )
        response = await self.call(request)
        logging.info("response %s" % response)

        if isinstance(response, self._call_result.DataTransferPayload):
            logging.info("status %s." % response.status)
            logging.info("data %s." % response.data)

    async def test_send_msg(self):
        send_opt = [k for k in dir(self) if k.startswith("send_")]
        logging.info("Server send_opt %s" % repr(send_opt))
        for i in send_opt:
            await getattr(self, i)()
            asyncio.sleep(0.5)
            break


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

    await asyncio.gather(cp.start(), cp.test_send_msg())


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
