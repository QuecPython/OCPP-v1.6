# OCPP v1.6 Version Request and Response Message Data Structure Description

[中文](../zh/请求与应答消息数据结构说明_V16.md) | English

- The relevant data module of OCPP v1.6 version is under the path `ocpp.v16`
- All message data structures are abstracted into classes corresponding to the message names. The parameters for class instantiation are the parameters that need to be included in the message body. Just instantiate the corresponding request message class object or response message class object.

**Example:**

```python
call.CancelReservationPayload(
    reservation_id=123
)

call_result.CancelReservationPayload(
    status=CancelReservationStatus.accepted
)
```

## <span id="request-message-structure">Request Message Structure<span>

- The request message structure file is `ocpp.v16.call`.

### Server Request Message Structure

- Corresponding to the client receiving message structure.

#### `call.CancelReservationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|reservation_id|int||Yes|

#### `call.CertificateSignedPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|certificate_chain|str|The maximum length: 10000|Yes|

#### `call.ChangeAvailabilityPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|connector_id|int||Yes|
|type|str|[`AvailabilityType`](#enums-availabilitytype "AvailabilityType Enumeration Value")|Yes|

#### `call.ChangeConfigurationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|key|str|The maximum length: 50|Yes|
|value|str|The maximum length: 500|Yes|

#### `call.ClearCachePayload`

**Parameter Description:**

- No Parameters

#### `call.ClearChargingProfilePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|id|int||No|
|connector_id|int||No|
|charging_profile_purpose|str|[`ChargingProfilePurposeType`](#enums-chargingprofilepurposetype "ChargingProfilePurposeType Enumeration Value")|No|
|stack_level|int||No|

#### `call.DeleteCertificatePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|certificate_hash_data|obj|[`CertificateHashData`](#datatypes-certificatehashdata "CertificateHashData Structured Data")|Yes|

#### `call.ExtendedTriggerMessagePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|requested_message|str|[`MessageTrigger`](#enums-messagetrigger "MessageTrigger Enumeration Value")|Yes|
|connector_id|int||No|

#### `call.GetCompositeSchedulePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|connector_id|int||Yes|
|duration|int||Yes|
|charging_rate_unit|str|[`ChargingRateUnitType`](#enums-chargingrateunittype "ChargingRateUnitType Enumeration Value")|Yes|

#### `call.GetConfigurationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|key|list|List element `str`, Maximum length of a single string: 50|No|

#### `call.GetDiagnosticsPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|location|str|uri|Yes|
|retries|int||No|
|retry_interval|int||No|
|start_time|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|
|stop_time|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|

#### `call.GetInstalledCertificateIdsPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|certificate_type|str|[`CertificateUse`](#enums-certificateuse "CertificateUse Enumeration Value")|Yes|

#### `call.GetLocalListVersionPayload`

**Parameter Description:**

- No Parameters

#### `call.GetLogPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|log|obj|[`LogParameters`](#datatypes-logparameters "LogParameters Structured Data")|Yes|
|log_type|str|[`Log`](#enums-log "Log Enumeration Value")|Yes|
|request_id|int||Yes|
|retries|int||No|
|retry_interval|int||No|

#### `call.InstallCertificatePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|certificate_type|str|[`CertificateUse`](#enums-certificateuse "CertificateUse Enumeration Value")|Yes|
|certificate|str|The maximum length: 5500|Yes|

#### `call.RemoteStartTransactionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|id_tag|str|The maximum length: 20|Yes|
|connector_id|int||No|
|charging_profile|obj|[`ChargingProfile`](#datatypes-chargingprofile "ChargingProfile Structured Data")|No|

#### `call.RemoteStopTransactionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|transaction_id|int||Yes|

#### `call.ReserveNowPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|connector_id|int||Yes|
|expiry_date|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|id_tag|str|The maximum length: 20|Yes|
|reservation_id|int||Yes|
|parent_id_tag|str|The maximum length: 20|No|

#### `call.ResetPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|type|str|[`ResetType`](#enums-resettype "ResetType Enumeration Value")|Yes|

#### `call.SendLocalListPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|list_version|int||Yes|
|update_type|str|[`UpdateType`](#enums-updatetype "UpdateType Enumeration Value")|Yes|
|local_authorization_list|list|List element is [`AuthorizationData`](#datatypes-authorizationdata "AuthorizationData Structured Data")|No|

#### `call.SetChargingProfilePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|connector_id|int||Yes|
|cs_charging_profiles|obj|[`ChargingProfile`](#datatypes-chargingprofile "ChargingProfile Structured Data")|Yes|

#### `call.SignedUpdateFirmwarePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|request_id|int||Yes|
|firmware|obj|[`Firmware`](#datatypes-firmware "Firmware Structured Data")|Yes|
|retries|int||No|
|retry_interval|int||No|

#### `call.TriggerMessagePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|requested_message|str|[`MessageTrigger`](#enums-messagetrigger "MessageTrigger Enumeration Value")|Yes|
|connector_id|int||No|

#### `call.UnlockConnectorPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|connector_id|int||Yes|

#### `call.UpdateFirmwarePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|location|str|uri|Yes|
|retrieve_date|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|retries|int||No|
|retry_interval|int||No|

### Client Request Message Structure

- Corresponding to the message structure received by the server.

#### `call.AuthorizePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|id_tag|str|The maximum length: 20|Yes|

#### `call.BootNotificationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|charge_point_model|str|The maximum length: 20|Yes|
|charge_point_vendor|str|The maximum length: 20|Yes|
|charge_box_serial_number|str|The maximum length: 25|No|
|charge_point_serial_number|str|The maximum length: 25|No|
|firmware_version|str|The maximum length: 50|No|
|iccid|str|The maximum length: 20|No|
|imsi|str|The maximum length: 20|No|
|meter_serial_number|str|The maximum length: 25|No|
|meter_type|str|The maximum length: 25|No|

#### `call.DiagnosticsStatusNotificationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`DiagnosticsStatus`](#enums-diagnosticsstatus "DiagnosticsStatus Enumeration Value")|Yes|

#### `call.FirmwareStatusNotificationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`FirmwareStatus`](#enums-firmwarestatus "FirmwareStatus Enumeration Value")|Yes|

#### `call.HeartbeatPayload`

**Parameter Description:**

- No Parameters

#### `call.LogStatusNotificationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`UploadLogStatus`](#enums-uploadlogstatus "UploadLogStatus Enumeration Value")|Yes|
|request_id|int||Yes|

#### `call.MeterValuesPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|connector_id|int||Yes|
|meter_value|list|List element is [`MeterValue`](#datatypes-metervalue "MeterValue Structured Data")|Yes|
|transaction_id|int||No|

#### `call.SecurityEventNotificationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|type|str|The maximum length: 50|Yes|
|timestamp|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|tech_info|str|The maximum length: 255|No|

#### `call.SignCertificatePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|csr|str|The maximum length: 5500|Yes|

#### `call.SignedFirmwareStatusNotificationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`FirmwareStatus`](#enums-firmwarestatus "FirmwareStatus Enumeration Value")|Yes|
|request_id|int||Yes|

#### `call.StartTransactionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|connector_id|int||Yes|
|id_tag|str|The maximum length: 20|Yes|
|meter_start|int||Yes|
|timestamp|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|reservation_id|int||No|

#### `call.StopTransactionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|meter_stop|int||Yes|
|timestamp|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|transaction_id|int||Yes|
|reason|str|[`Reason`](#enums-reason "Reason Enumeration Value")|No|
|id_tag|str|The maximum length: 20|No|
|transaction_data|list|List element is [`MeterValue`](#datatypes-metervalue "MeterValue Structured Data")|No|

#### `call.StatusNotificationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|connector_id|int||Yes|
|error_code|str|[`ChargePointErrorCode`](#enums-chargepointerrorcode "ChargePointErrorCode Enumeration Value")|Yes|
|status|str|[`ChargePointStatus`](#enums-chargepointstatus "ChargePointStatus Enumeration Value")|Yes|
|timestamp|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|info|str|The maximum length: 50|No|
|vendor_id|str|The maximum length: 255|No|
|vendor_error_code|str|The maximum length: 50|No|

### A Message Structure That Both The Server and The Client Can Request

#### `call.DataTransferPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|vendor_id|str|The maximum length: 255|Yes|
|message_id|str|The maximum length: 50|No|
|data|str||No|

## <span id="response-message-structure">Response Message Structure</span>

- The response message structure file is `ocpp.v16.call_result`.

### Server Response Client Request Message Structure

#### `call_result.AuthorizePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|id_tag_info|obj|[`IdTagInfo`](#datatypes-idtaginfo "IdTagInfo Structured Data")|Yes|

#### `call_result.BootNotificationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|current_time|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|interval|int||Yes|
|status|str|[`RegistrationStatus`](#enums-registrationstatus "RegistrationStatus Enumeration Value")|Yes|

#### `call_result.DiagnosticsStatusNotificationPayload`

**Parameter Description:**

- No Parameters

#### `call_result.FirmwareStatusNotificationPayload`

**Parameter Description:**

- No Parameters

#### `call_result.HeartbeatPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|current_time|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|

#### `call_result.LogStatusNotificationPayload`

**Parameter Description:**

- No Parameters

#### `call_result.SecurityEventNotificationPayload`

**Parameter Description:**

- No Parameters

#### `call_result.SignCertificatePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`GenericStatus`](#enums-genericstatus "GenericStatus Enumeration Value")|Yes|

#### `call_result.MeterValuesPayload`

**Parameter Description:**

- No Parameters

#### `call_result.StartTransactionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|transaction_id|int||Yes|
|id_tag_info|obj|[`IdTagInfo`](#datatypes-idtaginfo "IdTagInfo Structured Data")|Yes|

#### `call_result.StatusNotificationPayload`

**Parameter Description:**

- No Parameters

#### `call_result.StopTransactionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|id_tag_info|obj|[`IdTagInfo`](#datatypes-idtaginfo "IdTagInfo Structured Data")|Yes|

### Client Response Server Sequest Message Structure

#### `call_result.CancelReservationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`CancelReservationStatus`](#enums-cancelreservationstatus "CancelReservationStatus Enumeration Value")|Yes|

#### `call_result.CertificateSignedPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`CertificateSignedStatus`](#enums-certificatesignedstatus "CertificateSignedStatus Enumeration Value")|Yes|

#### `call_result.ChangeAvailabilityPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`AvailabilityStatus`](#enums-availabilitystatus "AvailabilityStatus Enumeration Value")|Yes|

#### `call_result.ChangeConfigurationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`ConfigurationStatus`](#enums-configurationstatus "ConfigurationStatus Enumeration Value")|Yes|

#### `call_result.ClearCachePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`ClearCacheStatus`](#enums-clearcachestatus "ClearCacheStatus Enumeration Value")|Yes|

#### `call_result.ClearChargingProfilePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`ClearChargingProfileStatus`](#enums-clearchargingprofilestatus "ClearChargingProfileStatus Enumeration Value")|Yes|

#### `call_result.DeleteCertificatePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`DeleteCertificateStatus`](#enums-deletecertificatestatus "DeleteCertificateStatus Enumeration Value")|Yes|

#### `call_result.ExtendedTriggerMessagePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`TriggerMessageStatus`](#enums-triggermessagestatus "TriggerMessageStatus Enumeration Value")|Yes|

#### `call_result.GetInstalledCertificateIdsPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`GetInstalledCertificateStatus`](#enums-getinstalledcertificatestatus "GetInstalledCertificateStatus Enumeration Value")|Yes|
|certificate_hash_data|list|List element is [`CertificateHashData`](#datatypes-certificatehashdata "CertificateHashData Structured Data")|No|

#### `call_result.GetCompositeSchedulePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`GetCompositeScheduleStatus`](#enums-getcompositeschedulestatus "GetCompositeScheduleStatus Enumeration Value")|Yes|
|connector_id|int||No|
|schedule_start|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|
|charging_schedule|obj|[`ChargingSchedule`](#datatypes-chargingschedule "ChargingSchedule Structured Data")|No|

#### `call_result.GetConfigurationPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|configuration_key|list|List element is [`KeyValue`](#datatypes-keyvalue "KeyValue Structured Data")|No|
|unknown_key|list|List element `str`, Maximum length of a single string: 50|No|

#### `call_result.GetDiagnosticsPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|file_name|str|The maximum length: 255|No|

#### `call_result.GetLocalListVersionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|list_version|int||Yes|

#### `call_result.GetLogPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`LogStatus`](#enums-logstatus "LogStatus Enumeration Value")|Yes|
|file_name|str|The maximum length: 255|No|

#### `call_result.InstallCertificatePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`CertificateStatus`](#enums-certificatestatus "CertificateStatus Enumeration Value")|Yes|

#### `call_result.RemoteStartTransactionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`RemoteStartStopStatus`](#enums-remotestartstopstatus "RemoteStartStopStatus Enumeration Value")|Yes|

#### `call_result.RemoteStopTransactionPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`RemoteStartStopStatus`](#enums-remotestartstopstatus "RemoteStartStopStatus Enumeration Value")|Yes|

#### `call_result.ReserveNowPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`ReservationStatus`](#enums-reservationstatus "ReservationStatus Enumeration Value")|Yes|

#### `call_result.ResetPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`ResetStatus`](#enums-resetstatus "ResetStatus Enumeration Value")|Yes|

#### `call_result.SendLocalListPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`UpdateStatus`](#enums-updatestatus "UpdateStatus Enumeration Value")|Yes|

#### `call_result.SetChargingProfilePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`ChargingProfileStatus`](#enums-chargingprofilestatus "ChargingProfileStatus Enumeration Value")|Yes|

#### `call_result.SignedFirmwareStatusNotificationPayload`

**Parameter Description:**

- No Parameters

#### `call_result.SignedUpdateFirmwarePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`UpdateFirmwareStatus`](#enums-updatefirmwarestatus "UpdateFirmwareStatus Enumeration Value")|Yes|

#### `call_result.TriggerMessagePayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`TriggerMessageStatus`](#enums-triggermessagestatus "TriggerMessageStatus Enumeration Value")|Yes|

#### `call_result.UnlockConnectorPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`UnlockStatus`](#enums-unlockstatus "UnlockStatus Enumeration Value")|Yes|

#### `call_result.UpdateFirmwarePayload`

**Parameter Description:**

- No Parameters

### A Response Message Structure That Both The Server and The Client Can Request

#### `call_result.DataTransferPayload`

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`DataTransferStatus`](#enums-datatransferstatus "DataTransferStatus Enumeration Value")|Yes|
|data|str||No|

## Data Structure In Message Body

- Other data structure corresponding files `ocpp.v16.datatypes`

### <span id="datatypes-idtaginfo">`datatypes.IdTagInfo`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|status|str|[`AuthorizationStatus`](#enums-authorizationstatus "AuthorizationStatus Enumeration Value")|Yes|
|parent_id_tag|str|The maximum length: 20|No|
|expiry_date|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|

### <span id="datatypes-authorizationdata">`datatypes.AuthorizationData`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|id_tag|str||Yes|
|id_tag_info|obj|[`IdTagInfo`](#datatypes-idtaginfo "IdTagInfo Structured Data")|No|

### <span id="datatypes-chargingscheduleperiod">`datatypes.ChargingSchedulePeriod`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|start_period|int||Yes|
|limit|float||Yes|
|number_phases|int||No|

### <span id="datatypes-chargingschedule">`datatypes.ChargingSchedule`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|charging_rate_unit|str|[`ChargingRateUnitType`](#enums-chargingrateunittype "ChargingRateUnitType Enumeration Value")|Yes|
|charging_schedule_period|list|List element is [`ChargingSchedulePeriod`](#datatypes-chargingscheduleperiod "ChargingSchedulePeriod Structured Data")|Yes|
|duration|int||No|
|start_schedule|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|
|min_charging_rate|float||No|

### <span id="datatypes-chargingprofile">`datatypes.ChargingProfile`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|charging_profile_id|int||Yes|
|stack_level|int||Yes|
|charging_profile_purpose|obj|[`ChargingProfilePurposeType`](#enums-chargingprofilepurposetype "ChargingProfilePurposeType Enumeration Value")|Yes|
|charging_profile_kind|obj|[`ChargingProfileKindType`](#enums-chargingprofilekindtype "ChargingProfileKindType Enumeration Value")|Yes|
|charging_schedule|obj|[`ChargingSchedule`](#datatypes-chargingschedule "ChargingSchedule Structured Data")|Yes|
|transaction_id|int||No|
|recurrency_kind|str|[`RecurrencyKind`](#enums-recurrencykind "RecurrencyKind Enumeration Value")|No|
|valid_from|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|
|valid_to|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|

### <span id="datatypes-keyvalue">`datatypes.KeyValue`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|key|str||Yes|
|readonly|bool||Yes|
|value|str||No|

### <span id="datatypes-sampledvalue">`datatypes.SampledValue`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|value|str||Yes|
|context|str|[`ReadingContext`](#enums-readingcontext "ReadingContext Enumeration Value")|No|
|format|str|[`ValueFormat`](#enums-valueformat "ValueFormat Enumeration Value")|No|
|measurand|str|[`Measurand`](#enums-measurand "Measurand Enumeration Value")|No|
|phase|str|[`Phase`](#enums-phase "Phase Enumeration Value")|No|
|location|str|[`Location`](#enums-location "Location Enumeration Value")|No|
|unit|str|[`UnitOfMeasure`](#enums-unitofmeasure "UnitOfMeasure Enumeration Value")|No|

### <span id="datatypes-metervalue">`datatypes.MeterValue`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|timestamp|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|sampled_value|list|List element is [`SampledValue`](#datatypes-sampledvalue "SampledValue Structured Data")|No|

### <span id="datatypes-certificatehashdata">`datatypes.CertificateHashData`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|hash_algorithm|str|[`HashAlgorithm`](#enums-hashalgorithm "HashAlgorithm Enumeration Value")|Yes|
|issuer_name_hash|str|The maximum length: 128|Yes|
|issuer_key_hash|str|The maximum length: 128|Yes|
|serial_number|str|The maximum length: 40|Yes|

### <span id="datatypes-firmware">`datatypes.Firmware`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|location|str|The maximum length: 512|Yes|
|retrieve_date_time|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|Yes|
|signing_certificate|str|The maximum length: 5500|Yes|
|signature|str|The maximum length: 800|Yes|
|install_date_time|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|

### <span id="datatypes-logparameters">`datatypes.LogParameters`</span>

**Parameter Description:**

|Parameter|Type|Description|Required|
|:---|:---|:---|:---|
|remote_location|str|The maximum length: 512|Yes|
|oldest_timestamp|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|
|latest_timestamp|str|UTC time (YYYY-MM-DDTHH:mm:SS.000000)|No|

## Enumeration Value In Message Body

- The enumeration value corresponds to the file `ocpp.v16.enums`.

### <span id="enums-action">`enums.Action`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|Authorize|str|`Authorize`|
|BootNotification|str|`BootNotification`|
|CancelReservation|str|`CancelReservation`|
|CertificateSigned|str|`CertificateSigned`|
|ChangeAvailability|str|`ChangeAvailability`|
|ChangeConfiguration|str|`ChangeConfiguration`|
|ClearCache|str|`ClearCache`|
|ClearChargingProfile|str|`ClearChargingProfile`|
|DataTransfer|str|`DataTransfer`|
|DeleteCertificate|str|`DeleteCertificate`|
|DiagnosticsStatusNotification|str|`DiagnosticsStatusNotification`|
|ExtendedTriggerMessage|str|`ExtendedTriggerMessage`|
|FirmwareStatusNotification|str|`FirmwareStatusNotification`|
|GetCompositeSchedule|str|`GetCompositeSchedule`|
|GetConfiguration|str|`GetConfiguration`|
|GetDiagnostics|str|`GetDiagnostics`|
|GetInstalledCertificateIds|str|`GetInstalledCertificateIds`|
|GetLocalListVersion|str|`GetLocalListVersion`|
|GetLog|str|`GetLog`|
|Heartbeat|str|`Heartbeat`|
|InstallCertificate|str|`InstallCertificate`|
|LogStatusNotification|str|`LogStatusNotification`|
|MeterValues|str|`MeterValues`|
|RemoteStartTransaction|str|`RemoteStartTransaction`|
|RemoteStopTransaction|str|`RemoteStopTransaction`|
|ReserveNow|str|`ReserveNow`|
|Reset|str|`Reset`|
|SecurityEventNotification|str|`SecurityEventNotification`|
|SendLocalList|str|`SendLocalList`|
|SetChargingProfile|str|`SetChargingProfile`|
|SignCertificate|str|`SignCertificate`|
|SignedFirmwareStatusNotification|str|`SignedFirmwareStatusNotification`|
|SignedUpdateFirmware|str|`SignedUpdateFirmware`|
|StartTransaction|str|`StartTransaction`|
|StatusNotification|str|`StatusNotification`|
|StopTransaction|str|`StopTransaction`|
|TriggerMessage|str|`TriggerMessage`|
|UnlockConnector|str|`UnlockConnector`|
|UpdateFirmware|str|`UpdateFirmware`|

### <span id="enums-authorizationstatus">`enums.AuthorizationStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|blocked|str|`Blocked`|
|expired|str|`Expired`|
|invalid|str|`Invalid`|
|concurrent_tx|str|`ConcurrentTx`|

### <span id="enums-availabilitystatus">`enums.AvailabilityStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|
|scheduled|str|`Scheduled`|

### <span id="enums-availabilitytype">`enums.AvailabilityType`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|inoperative|str|`Inoperative`|
|operative|str|`Operative`|

### <span id="enums-cancelreservationstatus">`enums.CancelReservationStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|

### <span id="enums-certificatesignedstatus">`enums.CertificateSignedStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|

### <span id="enums-certificatestatus">`enums.CertificateStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|
|failed|str|`Failed`|

### <span id="enums-certificateuse">`enums.CertificateUse`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|central_system_root_certificate|str|`CentralSystemRootCertificate`|
|manufacturer_root_certificate|str|`ManufacturerRootCertificate`|

### <span id="enums-chargepointerrorcode">`enums.ChargePointErrorCode`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|connector_lock_failure|str|`ConnectorLockFailure`|
|ev_communication_error|str|`EVCommunicationError`|
|ground_failure|str|`GroundFailure`|
|high_temperature|str|`HighTemperature`|
|internal_error|str|`InternalError`|
|local_list_conflict|str|`LocalListConflict`|
|no_error|str|`NoError`|
|other_error|str|`OtherError`|
|over_current_failure|str|`OverCurrentFailure`|
|over_voltage|str|`OverVoltage`|
|power_meter_failure|str|`PowerMeterFailure`|
|power_switch_failure|str|`PowerSwitchFailure`|
|reader_failure|str|`ReaderFailure`|
|reset_failure|str|`ResetFailure`|
|under_voltage|str|`UnderVoltage`|
|weak_signal|str|`WeakSignal`|

### <span id="enums-chargepointstatus">`enums.ChargePointStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|available|str|`Available`|
|preparing|str|`Preparing`|
|charging|str|`Charging`|
|suspended_evse|str|`SuspendedEVSE`|
|suspended_ev|str|`SuspendedEV`|
|finishing|str|`Finishing`|
|reserved|str|`Reserved`|
|unavailable|str|`Unavailable`|
|faulted|str|`Faulted`|

### <span id="enums-chargingprofilekindtype">`enums.ChargingProfileKindType`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|absolute|str|`Absolute`|
|recurring|str|`Recurring`|
|relative|str|`Relative`|

### <span id="enums-chargingprofilepurposetype">`enums.ChargingProfilePurposeType`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|charge_point_max_profile|str|`ChargePointMaxProfile`|
|tx_default_profile|str|`TxDefaultProfile`|
|tx_profile|str|`TxProfile`|

### <span id="enums-chargingprofilestatus">`enums.ChargingProfileStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|
|not_supported|str|`NotSupported`|

### <span id="enums-chargingrateunittype">`enums.ChargingRateUnitType`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|watts|str|`W`|
|amps|str|`A`|

### <span id="enums-cistringtype">`enums.CiStringType`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|ci_string_20|int|`20`|
|ci_string_25|int|`25`|
|ci_string_50|int|`50`|
|ci_string_255|int|`255`|
|ci_string_500|int|`500`|

### <span id="enums-clearcachestatus">`enums.ClearCacheStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|

### <span id="enums-clearchargingprofilestatus">`enums.ClearChargingProfileStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|unknown|str|`Unknown`|

### <span id="enums-configurationstatus">`enums.ConfigurationStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|
|reboot_required|str|`RebootRequired`|
|not_supported|str|`NotSupported`|

### <span id="enums-configurationkey">`enums.ConfigurationKey`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|allow_offline_tx_for_unknown_id|str|`AllowOfflineTxForUnknownId`|
|authorization_cache_enabled|str|`AuthorizationCacheEnabled`|
|authorize_remote_tx_requests|str|`AuthorizeRemoteTxRequests`|
|blink_repeat|str|`BlinkRepeat`|
|clock_aligned_data_interval|str|`ClockAlignedDataInterval`|
|connection_time_out|str|`ConnectionTimeOut`|
|connector_phase_rotation|str|`ConnectorPhaseRotation`|
|connector_phase_rotation_max_length|str|`ConnectorPhaseRotationMaxLength`|
|get_configuration_max_keys|str|`GetConfigurationMaxKeys`|
|heartbeat_interval|str|`HeartbeatInterval`|
|light_intensity|str|`LightIntensity`|
|local_authorize_offline|str|`LocalAuthorizeOffline`|
|local_pre_authorize|str|`LocalPreAuthorize`|
|max_energy_on_invalid_id|str|`MaxEnergyOnInvalidId`|
|meter_values_aligned_data|str|`MeterValuesAlignedData`|
|meter_values_aligned_data_max_length|str|`MeterValuesAlignedDataMaxLength`|
|meter_values_sampled_data|str|`MeterValuesSampledData`|
|meter_values_sampled_data_max_length|str|`MeterValuesSampledDataMaxLength`|
|meter_value_sample_interval|str|`MeterValueSampleInterval`|
|minimum_status_duration|str|`MinimumStatusDuration`|
|number_of_connectors|str|`NumberOfConnectors`|
|reset_retries|str|`ResetRetries`|
|stop_transaction_on_ev_side_disconnect|str|`StopTransactionOnEVSideDisconnect`|
|stop_transaction_on_invalid_id|str|`StopTransactionOnInvalidId`|
|stop_txn_aligned_data|str|`StopTxnAlignedData`|
|stop_txn_aligned_data_max_length|str|`StopTxnAlignedDataMaxLength`|
|stop_txn_sampled_data|str|`StopTxnSampledData`|
|stop_txn_sampled_data_max_length|str|`StopTxnSampledDataMaxLength`|
|supported_feature_profiles|str|`SupportedFeatureProfiles`|
|supported_feature_profiles_max_length|str|`SupportedFeatureProfilesMaxLength`|
|transaction_message_attempts|str|`TransactionMessageAttempts`|
|transaction_message_retry_interval|str|`TransactionMessageRetryInterval`|
|unlock_connector_on_ev_side_disconnect|str|`UnlockConnectorOnEVSideDisconnect`|
|web_socket_ping_interval|str|`WebSocketPingInterval`|
|local_auth_list_enabled|str|`LocalAuthListEnabled`|
|local_auth_list_max_length|str|`LocalAuthListMaxLength`|
|send_local_list_max_length|str|`SendLocalListMaxLength`|
|reserve_connector_zero_supported|str|`ReserveConnectorZeroSupported`|
|charge_profile_max_stack_level|str|`ChargeProfileMaxStackLevel`|
|charging_schedule_allowed_charging_rate_unit|str|`ChargingScheduleAllowedChargingRateUnit`|
|charging_schedule_max_periods|str|`ChargingScheduleMaxPeriods`|
|connector_switch_3to1_phase_supported|str|`ConnectorSwitch3to1PhaseSupported`|
|max_charging_profiles_installed|str|`MaxChargingProfilesInstalled`|
|central_contract_validation_allowed|str|`CentralContractValidationAllowed`|
|certificate_signed_max_chain_size|str|`CertificateSignedMaxChainSize`|
|cert_signing_wait_minimum|str|`CertSigningWaitMinimum`|
|cert_signing_repeat_times|str|`CertSigningRepeatTimes`|
|certificate_store_max_length|str|`CertificateStoreMaxLength`|
|contract_validation_offline|str|`ContractValidationOffline`|
|iso_15118_pnc_enabled|str|`ISO15118PnCEnabled`|
|additional_root_certificate_check|str|`AdditionalRootCertificateCheck`|
|authorization_key|str|`AuthorizationKey`|
|cpo_name|str|`CpoName`|
|security_profile|str|`SecurityProfile`|

### <span id="enums-datatransferstatus">`enums.DataTransferStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|
|unknown_message_id|str|`UnknownMessageId`|
|unknown_vendor_id|str|`UnknownVendorId`|

### <span id="enums-deletecertificatestatus">`enums.DeleteCertificateStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|failed|str|`Failed`|
|not_found|str|`NotFound`|

### <span id="enums-diagnosticsstatus">`enums.DiagnosticsStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|idle|str|`Idle`|
|uploaded|str|`Uploaded`|
|upload_failed|str|`UploadFailed`|
|uploading|str|`Uploading`|

### <span id="enums-firmwarestatus">`enums.FirmwareStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|downloaded|str|`Downloaded`|
|download_failed|str|`DownloadFailed`|
|downloading|str|`Downloading`|
|idle|str|`Idle`|
|installation_failed|str|`InstallationFailed`|
|installing|str|`Installing`|
|installed|str|`Installed`|
|download_scheduled|str|`DownloadScheduled`|
|download_paused|str|`DownloadPaused`|
|install_rebooting|str|`InstallRebooting`|
|install_scheduled|str|`InstallScheduled`|
|install_verification_failed|str|`InstallVerificationFailed`|
|invalid_signature|str|`InvalidSignature`|
|signature_verified|str|`SignatureVerified`|

### <span id="enums-genericstatus">`enums.GenericStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|

### <span id="enums-getcompositeschedulestatus">`enums.GetCompositeScheduleStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|

### <span id="enums-getinstalledcertificatestatus">`enums.GetInstalledCertificateStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|not_found|str|`NotFound`|

### <span id="enums-hashalgorithm">`enums.HashAlgorithm`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|sha256|str|`SHA256`|
|sha384|str|`SHA384`|
|sha512|str|`SHA512`|

### <span id="enums-location">`enums.Location`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|inlet|str|`Inlet`|
|outlet|str|`Outlet`|
|body|str|`Body`|
|cable|str|`Cable`|
|ev|str|`EV`|

### <span id="enums-log">`enums.Log`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|diagnostics_log|str|`DiagnosticsLog`|
|security_log|str|`SecurityLog`|

### <span id="enums-logstatus">`enums.LogStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|
|accepted_canceled|str|`AcceptedCanceled`|

### <span id="enums-measurand">`enums.Measurand`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|current_export|str|`Current.Export`|
|current_import|str|`Current.Import`|
|current_offered|str|`Current.Offered`|
|energy_active_export_register|str|`Energy.Active.Export.Register`|
|energy_active_import_register|str|`Energy.Active.Import.Register`|
|energy_reactive_export_register|str|`Energy.Reactive.Export.Register`|
|energy_reactive_import_register|str|`Energy.Reactive.Import.Register`|
|energy_active_export_interval|str|`Energy.Active.Export.Interval`|
|energy_active_import_interval|str|`Energy.Active.Import.Interval`|
|energy_reactive_export_interval|str|`Energy.Reactive.Export.Interval`|
|energy_reactive_import_interval|str|`Energy.Reactive.Import.Interval`|
|frequency|str|`Frequency`|
|power_active_export|str|`Power.Active.Export`|
|power_active_import|str|`Power.Active.Import`|
|power_factor|str|`Power.Factor`|
|power_offered|str|`Power.Offered`|
|power_reactive_export|str|`Power.Reactive.Export`|
|power_reactive_import|str|`Power.Reactive.Import`|
|rpm|str|`RPM`|
|soc|str|`SoC`|
|temperature|str|`Temperature`|
|voltage|str|`Voltage`|

### <span id="enums-messagetrigger">`enums.MessageTrigger`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|boot_notification|str|`BootNotification`|
|firmware_status_notification|str|`FirmwareStatusNotification`|
|heartbeat|str|`Heartbeat`|
|meter_values|str|`MeterValues`|
|status_notification|str|`StatusNotification`|
|diagnostics_status_notification|str|`DiagnosticsStatusNotification`|
|log_status_notification|str|`LogStatusNotification`|
|sign_charge_point_certificate|str|`SignChargePointCertificate`|

### <span id="enums-phase">`enums.Phase`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|l1|str|`L1`|
|l2|str|`L2`|
|l3|str|`L3`|
|n|str|`N`|
|l1_n|str|`L1-N`|
|l2_n|str|`L2-N`|
|l3_n|str|`L3-N`|
|l1_l2|str|`L1-L2`|
|l2_l3|str|`L2-L3`|
|l3_l1|str|`L3-L1`|

### <span id="enums-readingcontext">`enums.ReadingContext`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|interruption_begin|str|`Interruption.Begin`|
|interruption_end|str|`Interruption.End`|
|other|str|`Other`|
|sample_clock|str|`Sample.Clock`|
|sample_periodic|str|`Sample.Periodic`|
|transaction_begin|str|`Transaction.Begin`|
|transaction_end|str|`Transaction.End`|
|trigger|str|`Trigger`|

### <span id="enums-reason">`enums.Reason`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|emergency_stop|str|`EmergencyStop`|
|ev_disconnected|str|`EVDisconnected`|
|hard_reset|str|`HardReset`|
|local|str|`Local`|
|other|str|`Other`|
|power_loss|str|`PowerLoss`|
|reboot|str|`Reboot`|
|remote|str|`Remote`|
|soft_reset|str|`SoftReset`|
|unlock_command|str|`UnlockCommand`|
|de_authorized|str|`DeAuthorized`|

### <span id="enums-recurrencykind">`enums.RecurrencyKind`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|daily|str|`Daily`|
|weekly|str|`Weekly`|

### <span id="enums-registrationstatus">`enums.RegistrationStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|pending|str|`Pending`|
|rejected|str|`Rejected`|

### <span id="enums-remotestartstopstatus">`enums.RemoteStartStopStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|

### <span id="enums-reservationstatus">`enums.ReservationStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|faulted|str|`Faulted`|
|occupied|str|`Occupied`|
|rejected|str|`Rejected`|
|unavailable|str|`Unavailable`|

### <span id="enums-resetstatus">`enums.ResetStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|

### <span id="enums-resettype">`enums.ResetType`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|hard|str|`Hard`|
|soft|str|`Soft`|

### <span id="enums-triggermessagestatus">`enums.TriggerMessageStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|
|not_implemented|str|`NotImplemented`|

### <span id="enums-unitofmeasure">`enums.UnitOfMeasure`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|wh|str|`Wh`|
|kwh|str|`kWh`|
|varh|str|`varh`|
|kvarh|str|`kvarh`|
|w|str|`W`|
|kw|str|`kW`|
|va|str|`VA`|
|kva|str|`kVA`|
|var|str|`var`|
|kvar|str|`kvar`|
|a|str|`A`|
|v|str|`V`|
|celsius|str|`Celsius`|
|fahrenheit|str|`Fahrenheit`|
|k|str|`K`|
|percent|str|`Percent`|
|hertz|str|`Hertz`|

### <span id="enums-unlockstatus">`enums.UnlockStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|unlocked|str|`Unlocked`|
|unlock_failed|str|`UnlockFailed`|
|not_supported|str|`NotSupported`|

### <span id="enums-updatefirmwarestatus">`enums.UpdateFirmwareStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|rejected|str|`Rejected`|
|accepted_canceled|str|`AcceptedCanceled`|
|invalid_certificate|str|`InvalidCertificate`|
|revoked_certificate|str|`RevokedCertificate`|

### <span id="enums-uploadlogstatus">`enums.UploadLogStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|bad_message|str|`BadMessage`|
|idle|str|`Idle`|
|not_supported_operation|str|`NotSupportedOperation`|
|permission_denied|str|`PermissionDenied`|
|uploaded|str|`Uploaded`|
|upload_failure|str|`UploadFailure`|
|uploading|str|`Uploading`|

### <span id="enums-updatestatus">`enums.UpdateStatus`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|accepted|str|`Accepted`|
|failed|str|`Failed`|
|not_supported|str|`NotSupported`|
|version_mismatch|str|`VersionMismatch`|

### <span id="enums-updatetype">`enums.UpdateType`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|differential|str|`Differential`|
|full|str|`Full`|

### <span id="enums-valueformat">`enums.ValueFormat`</span>

|Enumeration Value|Data Type|Corresponding Value|
|:---|:---|:---|
|raw|str|`Raw`|
|signed_data|str|`SignedData`|
