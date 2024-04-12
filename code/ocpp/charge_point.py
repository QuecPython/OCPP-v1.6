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
@file      :charge_point.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2024-03-22 13:57:11
@copyright :Copyright (c) 2024
"""

import ure
import utime
import queue
import osTimer
import _thread

from usr.tools import uuid
from usr.tools import logging

from usr.ocpp.dataclasses import asdict
from usr.ocpp.messages import Call, MessageType, unpack, validate_payload
from usr.ocpp.exceptions import (
    NotImplementedError,
    NotSupportedError,
    OCPPError,
    TimeoutError
)

LOGGER = logging.getLogger(__name__)


def camel_to_snake_items(data):
    codes = []
    _code_ = ""
    for index, item in enumerate(data):
        if ure.match(r"[A-Z]", item):
            if index + 1 < len(data):
                if not ure.match(r"[A-Z]", data[index + 1]):
                    if index != 0:
                        codes.append(_code_)
                        _code_ = ""
                else:
                    if ure.match(r"[A-Z]*([a-z0-9]+)", _code_):
                        codes.append(_code_)
                        _code_ = ""
        _code_ += item

    if _code_:
        codes.append(_code_)

    return codes


def camel_to_snake_case(data):
    """
    Convert all keys of all dictionaries inside the given argument from
    camelCase to snake_case.

    Inspired by: https://stackoverflow.com/a/1176023/1073222

    """
    if isinstance(data, dict):
        return {"_".join(camel_to_snake_items(key)).lower(): camel_to_snake_case(value) for key, value in data.items()}

    if isinstance(data, list):
        return [camel_to_snake_case(value) for value in data]

    return data


def snake_to_camel_case(data):
    """
    Convert all keys of all dictionaries inside given argument from
    snake_case to camelCase.

    Inspired by: https://stackoverflow.com/a/19053800/1073222
    """
    if isinstance(data, dict):
        camel_case_dict = {}
        for key, value in data.items():
            components = key.replace("soc", "SoC").replace("_v2x", "V2X").split("_")
            key = components[0] + "".join(x[:1].upper() + x[1:] for x in components[1:])
            camel_case_dict[key] = snake_to_camel_case(value)

        return camel_case_dict

    if isinstance(data, list):
        return [snake_to_camel_case(value) for value in data]

    return data


def remove_nones(data):
    if isinstance(data, dict):
        return {k: remove_nones(v) for k, v in data.items() if v is not None}

    elif isinstance(data, list):
        return [remove_nones(v) for v in data if v is not None]

    return data


def _raise_key_error(action, version):
    """
    Checks whether a keyerror returned by _handle_call
    is supported by the OCPP version or is simply
    not implemented by the server/client and raises
    the appropriate error.
    """

    from ocpp.v16.enums import Action as v16_Action
    # from ocpp.v201.enums import Action as v201_Action

    if version == "1.6":
        if hasattr(v16_Action, action):
            raise NotImplementedError(
                None, {"cause": "No handler for {action} registered.".format(action=action)}
            )
        else:
            raise NotSupportedError(
                None, {"cause": "{action} not supported by OCPP{version}.".format(action=action, version=version)}
            )
    else:
        # elif version in ["2.0", "2.0.1"]:
        #     if hasattr(v201_Action, action):
        #         raise NotImplementedError(
        #             None, {"cause": f"No handler for {action} registered."}
        #         )
        #     else:
        raise NotSupportedError(
            None, {"cause": "{action} not supported by OCPP{version}.".format(action=action, version=version)}
        )

    return


class Queue(queue.Queue):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timer = osTimer()
        self._timeout_tag = 0

    def _timeout(self, args):
        self._timeout_tag = 1
        super().put(args)

    def get(self, timeout):
        self._timeout_tag = 0
        self._timer.start(timeout * 1000, 0, self._timeout)
        data = super().get()
        self._timer.stop()
        if data is None and self._timeout_tag == 1:
            raise TimeoutError
        return data


class ChargePoint:
    """
    Base Element containing all the necessary OCPP1.6J messages for messages
    initiated and received by the Central System
    """

    def __init__(self, id, connection, response_timeout=30):
        """

        Args:

            charger_id (str): ID of the charger.
            connection: Connection to CP.
            response_timeout (int): When no response on a request is received
                within this interval, a asyncio.TimeoutError is raised.

        """
        self.id = id

        # The maximum time in seconds it may take for a CP to respond to a
        # CALL. An asyncio.TimeoutError will be raised if this limit has been
        # exceeded.
        self._response_timeout = response_timeout

        # A connection to the client. Currently this is an instance of gh
        self._connection = connection

        self._call_lock = _thread.allocate_lock()

        # A queue used to pass CallResults and CallErrors from
        # the self.serve() task to the self.call() task.
        self._response_queue = Queue()

        # Function used to generate unique ids for CALLs. By default
        # uuid.uuid4() is used, but it can be changed. This is meant primarily
        # for testing purposes to have predictable unique ids.
        self._unique_id_generator = uuid.uuid4

    def start(self):
        while True:
            message = self._connection.recv()
            LOGGER.info("%s: receive message %s" % (self.id, message))

            self.route_message(message)

    def route_message(self, raw_msg):
        """
        Route a message received from a CP.

        If the message is a of type Call the corresponding hooks are executed.
        If the message is of type CallResult or CallError the message is passed
        to the call() function via the response_queue.
        """
        if raw_msg:
            try:
                msg = unpack(raw_msg)
            except OCPPError as e:
                LOGGER.error(
                    "Unable to parse message: '%s', it doesn't seem "
                    "to be valid OCPP: %s" % (raw_msg, e)
                )
                return

            if msg.message_type_id in [MessageType.CallResult, MessageType.CallError]:
                self._response_queue.put(msg)

    def call(self, payload, suppress=True, unique_id=None):
        """
        Send Call message to client and return payload of response.

        The given payload is transformed into a Call object by looking at the
        type of the payload. A payload of type BootNotificationPayload will
        turn in a Call with Action BootNotification, a HeartbeatPayload will
        result in a Call with Action Heartbeat etc.

        A timeout is raised when no response has arrived before expiring of
        the configured timeout.

        When waiting for a response no other Call message can be send. So this
        function will wait before response arrives or response timeout has
        expired. This is in line the OCPP specification

        Suppress is used to maintain backwards compatibility. When set to True,
        if response is a CallError, then this call will be suppressed. When
        set to False, an exception will be raised for users to handle this
        CallError.

        """
        camel_case_payload = asdict(payload)

        unique_id = (
            unique_id if unique_id is not None else str(self._unique_id_generator())
        )

        call = Call(
            unique_id=unique_id,
            action=payload.__class__.__name__[:-7],
            payload=remove_nones(camel_case_payload),
        )

        validate_payload(call, self._ocpp_version)

        call.payload = snake_to_camel_case(call.payload)
        # Use a lock to prevent make sure that only 1 message can be send at a
        # a time.
        with self._call_lock:
            self._send(call.to_json())
            try:
                response = self._get_specific_response(
                    call.unique_id, self._response_timeout
                )
            except TimeoutError:
                raise TimeoutError(
                    "Waited {}s for response on "
                    "{}.".format(self._response_timeout, call.to_json())
                )

        if response.message_type_id == MessageType.CallError:
            LOGGER.warn("Received a CALLError: %s'" % response)
            if suppress:
                return
            raise response.to_exception()
        else:
            response.action = call.action
            response.payload = camel_to_snake_case(response.payload)
            validate_payload(response, self._ocpp_version)

        # Create the correct Payload instance based on the received payload. If
        # this method is called with a call.BootNotificationPayload, then it
        # will create a call_result.BootNotificationPayload. If this method is
        # called with a call.HeartbeatPayload, then it will create a
        # call_result.HeartbeatPayload etc.
        cls = getattr(self._call_result, payload.__class__.__name__)  # noqa
        return cls(**response.payload)

    def _get_specific_response(self, unique_id, timeout):
        """
        Return response with given unique ID or raise an asyncio.TimeoutError.
        """
        wait_until = utime.time() + timeout
        try:
            # Wait for response of the Call message.
            response = self._response_queue.get(wait_until)
        except TimeoutError:
            raise

        if hasattr(response, "unique_id") and response.unique_id == unique_id:
            return response

        LOGGER.error("Ignoring response with unknown unique id: %s" % response)
        timeout_left = wait_until - utime.time()

        if timeout_left < 0:
            raise TimeoutError

        return self._get_specific_response(unique_id, timeout_left)

    def _send(self, message):
        LOGGER.info("%s: send %s" % (self.id, message))
        self._connection.send(message)
