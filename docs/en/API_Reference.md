# OCPP API Reference

[中文](../zh/API参考手册.md) | English

The protocol function of this module is based on websocket and uses json format data for data interaction.

This module designs the `ocpp.charge_point.ChargePoint` abstract class, which is used as a base class. Users need to conduct secondary development according to the actual situation of their own projects. Based on this abstract class, they encapsulate the corresponding versions that their own projects need to use and send and receiving functions.

Currently, the project only supports OCPP v1.6, and support will continue to be expanded in the future.

This article is mainly divided into two modules:

1. Introduction and usage instructions of the relevant interfaces and associated decorators of the `ChargePoint` base class.
2. Secondary development example of implementing data sending and receiving interface based on `ChargePoint` base class.

## Charging Station / Charging Point Abstract Class

### `ChargePoint`

- `ocpp.charge_point.ChargePoint` is a charging station/charging point abstract class.
- This abstract class encapsulates the [`call`](#cp-call) interface for sending data based on the websocket protocol and the [`start`](#cp-start) interface for receiving and processing server messages.
- The secondary development of this abstract class requires the use of [`ocpp.routing.on`](#routing-on) and [`ocpp.routing.atfer`](#routing-after) decorators to encapsulate the receiving message processing function.
- This abstract class is usually inherited in the corresponding version, such as: `ocpp.v16.ChargePoint`, adding [`_call`](#cp-_call), [`_call_result`](#cp-_call_result), [`_ocpp_version`](#cp-_ocpp_version) attribute value.
- This module is based on the websocket protocol and requires the use of the [QuecPython uwebscoket](https://python.quectel.com/doc/API_reference/zh/networklib/uwebsocket.html "QuecPython uwebsocket module usage instructions") module.

#### Initialization

```python
from usr.tools import uwebsocket
from usr.ocpp.v16 import ChargePoint as cp

# It is recommended to use the device IMEI or device MAC address as the unique identifier of the device.
IMEI = "XXXX"
# Corresponding server IP address.
host = "xxx.xxx.xxx.xxx"
# Corresponding server port number.
port = "xxxx"
# Instantiate a uwebsocket object.
ws = uwebsocket.Client.connect(
    "ws://{host}:{port}/{IMEI}",
    # Add the corresponding OCPP version number in the header for identification by the server. Different servers have different requirements, so fill in the information according to the actual situation.
    headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
    debug=False
)

# Instantiate a ChargePoint object.
cp = ChargePoint(IMEI, ws)
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|id|str|Device ID|
|connection|obj|uwebsocket object|
|response_timeout|int|Request response timeout, unit: seconds, default: 30|

**Return Value Description:**

|Type|Description|
|:---|:---|
|obj|ChargePoint object|

#### <span id="cp-start">`ChargePoint.start`</span>

- Start a loop to receive server data, usually start a separate thread to run this method.

```python
import _thread

# Set the thread stack size according to actual usage.
_thread.stack_size(0x4000)
# Start a thread to receive and parse data sent by the server.
_thread.start_new_thread(cp.start, ())
```

#### <span id="cp-call">`ChargePoint.call`</span>

- Sends a Call message to the server and returns the response payload.
- This method is usually used in secondary encapsulated functions.

```python
class ChargePoint(cp):

    # The client sends a request to the authentication interface.
    def send_authorize(self):
        # Use the AuthorizePayload class to generate the data structure of the client request authentication interface.
        request = self._call.AuthorizePayload(
            id_tag="xxx",
        )
        # Call the call method to send a message and wait for a response.
        response = self.call(request)
        logger.info("response %s" % response)

        # Determine whether the parsed response is the response data structure of the request authentication interface, and if so, process the response data.
        if isinstance(response, self._call_result.AuthorizePayload):
            logger.info("id_tag_info %s." % response.id_tag_info)
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|payload|obj|`vxx.call.xxx` Request message data structure object|
|suppress|bool|Whether an exception will be thrown when a request returns CallError<br>`True` - Skip the exception and return directly<br>`False` - Throw an exception<br>Default: `True`|
|unique_id|str|The unique identifier of the message. When not transmitted, a uuid4 value is automatically generated as the unique identifier. Default: None|

**Return Value Description:**

|Type|Description|
|:---|:---|
|obj|`vxx.call_result.xxx` Response message data structure object|

#### <span id="cp-_call">`ChargePoint._call`</span>

- When this class is imported from the corresponding version module, there will be this attribute, which is the corresponding version of the `call` module. For example: `ocpp.v16.ChargePoint._call` is equivalent to `ocpp.v16.call`.
- This attribute is mainly used for secondary development and is convenient for encapsulating interfaces.
- [OCPP v1.6 Request Message Data Structure](./Request_and_Response_Message_Data_Structure_Description_V16.md#request-message-structure)

#### <span id="cp-_call_result">`ChargePoint._call_result`</span>

- When this class is imported from the corresponding version module, there will be this attribute, which is the corresponding version of the `call_result` module. For example: `ocpp.v16.ChargePoint._call_result` is equivalent to `ocpp.v16.call_result`.
- This attribute is mainly used for secondary development and is convenient for encapsulating interfaces.
- [OCPP v1.6 Response message Data Structure](./Request_and_Response_Message_Data_Structure_Description_V16.md#response-message-structure)

#### <span id="cp-_ocpp_version">`ChargePoint._ocpp_version`</span>

- When this class is imported from the corresponding version module, there will be this attribute, which is the corresponding ocpp protocol version number.

## Decorator For Functions That Handle Server Messages

### <span id="routing-on">`ocpp.routing.on`</span>

- This decorator is used to process the encapsulation function of the message sent by the corresponding server.
- The input parameter of the decorated function is the data structure information of the received message, and returns the data structure information of the response corresponding to the message, which is used to send it to the server for message response.

```python
class ChargePoint(cp):

    # The client receives the cancellation message processing interface
    # and uses the ocpp.routing.on decorator to register the processing function corresponding to
    # the received message. This function is used to receive the message body data of
    # the corresponding message and needs to return the response data structure of the corresponding message.
    @on(Action.CancelReservation)
    def on_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))

        # After receiving the message, you can perform business function processing here,
        # or respond first, and then perform business processing in the function decorated by ocpp.routing.after.

        # This function must return the response message body of the corresponding message,
        # which is used to respond to server messages.
        return self._call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|action|str|For the corresponding message type, you can directly use the data in the `ocpp.vxx.enums.Actions` enumeration value.|
|skip_schema_validation|bool|Whether to skip request or response message body data verification<br>`True` - skip verification<br>`False` - do not skip verification<br>Default: `False`|
|call_unique_id_required|bool|Whether to pass the message unique identifier as a parameter into the decorated function<br>`True` - Yes<br>`False` - No<br>Default: `False`|

### <span id="routing-after">`ocpp.routing.after`</span>

- This decorator is used to process the encapsulated function corresponding to the message sent by the server, which is called after the function decorated by `ocpp.routing.on` is called.
- The input parameters of the decorated function are the data structure information of the received message, and there are no special requirements for the return value.

```python
class ChargePoint(cp):

    # After the client receives the cancellation message,
    # after the response is completed or after no response is required,
    # the client can use the ocpp.routing.after decorator to register
    # the processing function corresponding to the received message
    # if it needs to perform business processing functions.
    @after(Action.CancelReservation, call_unique_id_required=True)
    def after_cancel_reservation(self, reservation_id, call_unique_id):
        logger.info("reservation_id %s, call_unique_id %s" % (reservation_id, call_unique_id))
        # The corresponding business function can be processed here.
        # This function has no special requirements for the return value.
        return
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|action|str|For the corresponding message type, you can directly use the data in the `ocpp.vxx.enums.Actions` enumeration value.|
|call_unique_id_required|bool|Whether to pass the message unique identifier as a parameter into the decorated function<br>`True` - Yes<br>`False` - No<br>Default: `False`|

## Secondary Development Example Based On `ChargePoint`

- This abstract class encapsulates the websocket-based protocol and needs to instantiate the `uwebsocket` object as a parameter to initialize the `ChargePoint` module.
- When using it, import the `ChargePoint` class from the corresponding version, such as: `from usr.ocpp.v16 import ChargePoint as cp`.

**Note:**

The following only lists examples of processing functions for a client to send messages and a client to receive messages for reference. Which request messages and receive messages need to be used in the actual project need to be developed according to the actual requirements of the project.

```python
import utime
import _thread
# Import the uwebsocket module and instantiate objects for the ChargePoint class.
from usr.tools import uwebsocket, logging
# Import the v16 version of ChargePoint as the project base class.
from usr.ocpp.v16 import ChargePoint as cp


# Secondary development based on the v16 version of the project base class,
# encapsulating the client sending interface and message receiving interface that need to be used.
class ChargePoint(cp):

    # The client sends a request to the authentication interface.
    def send_authorize(self):
        # Use the AuthorizePayload class to generate the data structure of the client request authentication interface.
        request = self._call.AuthorizePayload(
            id_tag="xxx",
        )
        # Call the call method to send a message and wait for a response.
        response = self.call(request)
        logger.info("response %s" % response)

        # Determine whether the parsed response is the response data structure of
        # the request authentication interface, and if so, process the response data.
        if isinstance(response, self._call_result.AuthorizePayload):
            logger.info("id_tag_info %s." % response.id_tag_info)

    # The client receives the cancellation message processing interface and
    # uses the ocpp.routing.on decorator to register the processing function corresponding to the received message.
    # This function is used to receive the message body data of the corresponding message and needs to
    # return the response data structure of the corresponding message.
    @on(Action.CancelReservation)
    def on_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))

        # After receiving the message, you can perform business function processing here,
        # or respond first, and then perform business processing in the function decorated by ocpp.routing.after.

        # This function must return the response message body of the corresponding message,
        # which is used to respond to server messages.
        return self._call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )

    # After the client receives the cancellation message,
    # after the response is completed or after no response is required,
    # the client can use the ocpp.routing.after decorator to register the processing function
    # corresponding to the received message if it needs to perform business processing functions.
    @after(Action.CancelReservation)
    def after_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))
        # The corresponding business function can be processed here.
        # This function has no special requirements for the return value.
        return

# It is recommended to use device IMEI or device MAC address as device identification.
IMEI = "XXXX"
# Corresponding server IP address.
host = "xxx.xxx.xxx.xxx"
# Corresponding server port number.
port = "xxxx"
# Instantiate a uwebsocket object.
ws = uwebsocket.Client.connect(
    "ws://{host}:{port}/{IMEI}",
    # Add the corresponding OCPP version number in the header for identification by the server.
    # Different servers have different requirements, so fill in the information according to the actual situation.
    headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
    debug=False
)

# Instantiate a secondary developed ChargePoint object containing specific business functions.
cp = ChargePoint(IMEI, ws)

# Start a thread to receive data sent by the server.
_thread.start_new_thread(cp.start, ())

# Send request authentication message.
cp.send_authorize()

# Waiting to receive server data.
utime.sleep(10)
```
