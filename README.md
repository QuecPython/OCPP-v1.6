# OCPP

## Introduction

This is based on QuecPython.

Python package implementing the JSON version of the Open Charge Point Protocol (OCPP). Currently OCPP 1.6 (errata v4) is supported.

The purpose of this library is to provide the building blocks to construct a charging station/charge point. **The library does not provide a completed solution, as any implementation is specific for its intended use**. The documents in this library should be inspected, as these documents provided guidance on how best to build a complete solution.

## Quick start

Below you can find examples on how to create a simple OCPP 1.6 Charging Station/Charge Point.

**Note:**

> To run these examples the dependency uwebsocket is required! This file is in `code/tools/uwensocket.py`.

## Charging Station / Charge point

The `v16_client_qpy_demo.py` is Charging Station / Charge point demo.

```python
import modem
import utime
import _thread

from usr.tools import uwebsocket, logging
from usr.ocpp.routing import on
from usr.ocpp.v16 import ChargePoint as cp
from usr.ocpp.v16.enums import RegistrationStatus, Action

logger = logging.getLogger(__name__)

IMEI = modem.getDevImei()


class ChargePoint(cp):

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

    @on(Action.CancelReservation)
    def on_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))

        return self._call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )


if __name__ == "__main__":
    # Init websocket client.
    ws = uwebsocket.Client.connect(
        "ws://xxx.xxx.xxx.xxx:xxxx/%s" % IMEI,
        headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
        debug=True
    )

    # Init ChargePoint.
    cp = ChargePoint(IMEI, ws)

    # Start websocket receiving thread.
    _thread.stack_size(0x2000)
    tid = _thread.start_new_thread(cp.start, ())
    utime.sleep_ms(200)

    # Send boot notification.
    cp.send_boot_notification()
```

## Project Files Description

```
|-- code
    |-- ocpp
        |-- v16
            |-- __init__.py
            |-- call_reasult.py
            |-- call.py
            |-- datatypes.py
            |-- enums.py
        |-- charge_point.py
        |-- dataclasses.py
        |-- exceptions.py
        |-- messages.py
        |-- routing.py
    |-- tools
        |-- logging.py
        |-- uuid.py
        |-- uwebsocket.py
    |-- v16_client_qpy_demo.py
|-- demo
    |-- requirements.txt
    |-- v16_server_demo.py
|-- docs
    |-- OCPP_1.6_documentation_2019_12-2.zip
```

- `code` floder is incloud all OCPP client codes.
    + `code/ocpp` floder is incloud ocpp procotal codes.
        + `code/ocpp/v16/call.py` is incloud all request data format.
        + `code/ocpp/v16/call_result.py` is incloud all response data format.
        + `code/ocpp/v16/datatypes.py` is incloud some data format for part of request data.
        + `code/ocpp/v16/enums.py` is incloud some enumes of request / response data.
        + `code/ocpp/charge_point.py` is charge point class.
    + `code/tools` floder is incloud some auxiliary function module.
        + `code/tools/logging.py` is log module.
        + `code/tools/uuid.py` is uuid module.
        + `code/tools/uwebsocket.py` is client of websocket module.
    + `code/ocpp/v16_client_qpy_demo.py` is incloud all charge point request demo of ocpp.
- `demo` floder is incloud OCPP server demo based on Cpython.
    + `demo/requirements.txt` is incloud dependency packages of OCPP server demo running environment.
    + `demo/v16_server_demo.py` is OCPP server demo code based on Cpython.
- `docs` floder is incloud OCPP protocal documents.
    + `docs/OCPP_1.6_documentation_2019_12-2.zip` is OCPP v1.6 protocal documents.

## How To Use

### Running OCPP Server

> If you have your own OCPP server, you can skip this instruction.

#### 1. Install environments

1. Operating System: Window or Linux.

2. Language: Python (Python-3.11.2).

3. Dependency packages: `pip install -r demo/requirements.txt`.

#### 2. Config server and running demo

1. Change your server port in `demo/v16_server_demo.py`.

```python
async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        31499,  # Change this port value for your own server port.
        subprotocols=['ocpp1.6.0']
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()
```

2. Running `python demo/v16_server_demo.py`. When output `INFO:root:WebSocket Server Started`, the server is started.

```python
>>> python v16_server_demo.py

INFO:websockets.server:server listening on 0.0.0.0:31499
INFO:root:WebSocket Server Started
```

### Running OCPP Client.

#### 1. Running environment

You need to use our QuecPython module.

#### 2. Config client and running demo

1. Config your server host and port in `code/ocpp/v16_client_qpy_demo.py`

```python
if __name__ == "__main__":
    ws = uwebsocket.Client.connect(
        "ws://xxx.xxx.xxx.xxx:xxxx/%s" % IMEI,  #  Use your own server host and port to replace `xxx.xxx.xxx.xxx:xxxx`.
        headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
        debug=True
    )
    cp = ChargePoint(IMEI, ws)

    _thread.stack_size(0x2000)
    tid = _thread.start_new_thread(cp.start, ())
    utime.sleep_ms(200)
```

2. Download code to QuecPython module

**Note:**

> You can find documents in [QuecPython Document Center](https://python.quectel.com/doc/Getting_started/en/index.html) for how to download python code and running python demo in our QuecPython module 

You can download full `code` floder to our QuecPython module and run `v16_client_qpy_demo.py` to test ocpp Charging Station / Charge point.

You can see log `Connected to central system.` in our QPYcom REPL, than the `BootNotification` message is sented to server.

**Note:**

> You can refer to `code.ocpp.v16_client_qpy_demo.py` to write client requests that conform to business logic.
