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

""" Module containing classes that model the several OCPP messages types. It
also contain some helper functions for packing and unpacking messages.  """

import ujson

from usr.ocpp.v16 import call, call_result
from usr.ocpp.dataclasses import asdict, is_dataclass, validate_dataclass

from usr.ocpp.exceptions import (
    FormatViolationError,
    OCPPError,
    PropertyConstraintViolationError,
    ProtocolError,
    TypeConstraintViolationError,
    UnknownCallErrorCodeError,
    ValidationError,
    SchemaValidationError,
)


class MessageType:
    """Number identifying the different types of OCPP messages."""

    #: Call identifies a request.
    Call = 2

    #: CallResult identifies a successful response.
    CallResult = 3

    #: CallError identifies an erroneous response.
    CallError = 4


def unpack(msg):
    """
    Unpacks a message into either a Call, CallError or CallResult.
    """
    try:
        msg = ujson.loads(msg)
    except Exception:
        raise FormatViolationError(
            None, {"cause": "Message is not valid JSON", "ocpp_message": msg}
        )

    if not isinstance(msg, list):
        raise ProtocolError(
            None,
            {
                "cause": (
                    "OCPP message hasn't the correct format. It "
                    "should be a list, but got '{}' "
                    "instead".format(type(msg))
                )
            }
        )

    for cls in [Call, CallResult, CallError]:
        try:
            if msg[0] == cls.message_type_id:
                return cls(*msg[1:])
        except IndexError:
            raise ProtocolError(
                None, {"cause": "Message does not contain MessageTypeId"}
            )
        except TypeError:
            raise ProtocolError(None, {"cause": "Message is missing elements."})

    raise PropertyConstraintViolationError(
        None, {"cause": "MessageTypeId '{}' isn't valid".format(msg[0])}
    )


def pack(msg):
    """
    Returns the JSON representation of a Call, CallError or CallResult.

    It just calls the 'to_json()' method of the message. But it is here mainly
    to complement the 'unpack' function of this module.
    """
    return msg.to_json()


def validate_payload(message, ocpp_version):
    """Validate the payload of the message using JSON schemas."""
    if type(message) not in [Call, CallResult]:
        raise ValidationError(
            None,
            "Payload can't be validated because message "
            "type. It's '{}', but it should "
            "be either 'Call'  or 'CallResult'.".format(type(message))
        )

    try:
        _cls = None
        if type(message) is Call:
            _cls = getattr(call, message.action + "Payload")
        elif type(message) is CallResult:
            _cls = getattr(call_result, message.action + "Payload")
        validate_dataclass(message.payload, _cls)
    except SchemaValidationError as e:
        if e.validator == "type":
            raise TypeConstraintViolationError(
                None, {"cause": e.message, "ocpp_message": message}
            )
        elif e.validator == "additionalProperties":
            raise FormatViolationError(
                None, {"cause": e.message, "ocpp_message": message}
            )
        elif e.validator == "required":
            raise ProtocolError(None, {"cause": e.message})

        elif e.validator == "maxLength":
            raise TypeConstraintViolationError(
                None, {"cause": e.message, "ocpp_message": message}
            ) from e
        else:
            raise FormatViolationError(
                None,
                {
                    "cause": "Payload '{}' for action '{}' is not valid: {}".format(
                        message.payload, message.action, e
                    ),
                    "ocpp_message": message
                }
            )


class Call:
    """A Call is a type of message that initiate a request/response sequence.
    Both central systems and charge points can send this message.

    From the specification:

        A Call always consists of 4 elements: The standard elements
        MessageTypeId and UniqueId, a specific Action that is required on the
        other side and a payload, the arguments to the Action. The syntax of a
        call looks like this:

            [<MessageTypeId>, "<UniqueId>", "<Action>", {<Payload>}]

        ...

        For example, a BootNotification request could look like this:

            [2,
             "19223201",
             "BootNotification",
             {
              "chargePointVendor": "VendorX",
              "chargePointModel": "SingleSocketCharger"
             }
            ]
    """

    message_type_id = 2

    def __init__(self, unique_id, action, payload):
        self.unique_id = unique_id
        self.action = action
        self.payload = payload

        if is_dataclass(payload):
            self.payload = asdict(payload)

    def to_json(self):
        """Return a valid JSON representation of the instance."""
        return ujson.dumps(
            [
                self.message_type_id,
                self.unique_id,
                self.action,
                self.payload,
            ],
            # By default ujson.dumps() adds a white space after every separator.
            # By setting the separator manually that can be avoided.
            # separators=(",", ":"),
        )

    def create_call_result(self, payload):
        _call_result = CallResult(self.unique_id, payload)
        _call_result.action = self.action
        return _call_result

    def create_call_error(self, exception):
        error_code = "InternalError"
        error_description = "An unexpected error occurred."
        error_details = {}

        if isinstance(exception, OCPPError):
            error_code = exception.code
            error_description = exception.description
            error_details = exception.details

        return CallError(
            self.unique_id,
            error_code,
            error_description,
            error_details,
        )

    def __repr__(self):
        return (
            "<Call - unique_id={}, action={}, payload={}>".format(
                self.unique_id, self.action, self.payload
            )
        )


class CallResult:
    """
    A CallResult is a message indicating that a Call has been handled
    successfully.

    From the specification:

        A CallResult always consists of 3 elements: The standard elements
        MessageTypeId, UniqueId and a payload, containing the response to the
        Action in the original Call. The syntax of a call looks like this:

            [<MessageTypeId>, "<UniqueId>", {<Payload>}]

        ...

        For example, a BootNotification response could look like this:

            [3,
             "19223201",
             {
              "status":"Accepted",
              "currentTime":"2013-02-01T20:53:32.486Z",
              "heartbeatInterval":300
             }
            ]

    """

    message_type_id = 3

    def __init__(self, unique_id, payload, action=None):
        self.unique_id = unique_id
        self.payload = payload

        # Strictly speaking no action is required in a CallResult. But in order
        # to validate the message it is needed.
        self.action = action

    def to_json(self):
        return ujson.dumps(
            [
                self.message_type_id,
                self.unique_id,
                self.payload,
            ],
            # By default ujson.dumps() adds a white space after every separator.
            # By setting the separator manually that can be avoided.
            # separators=(",", ":"),
        )

    def __repr__(self):
        return (
            "<CallResult - unique_id={}, action={}, payload={}>".format(
                self.unique_id, self.action, self.payload
            )
        )


class CallError:
    """
    A CallError is a response to a Call that indicates an error.

    From the specification:

        CallError always consists of 5 elements: The standard elements
        MessageTypeId and UniqueId, an errorCode string, an errorDescription
        string and an errorDetails object.

        The syntax of a call looks like this:

            [<MessageTypeId>, "<UniqueId>", "<errorCode>", "<errorDescription>", {<errorDetails>}] # noqa
    """

    message_type_id = 4

    def __init__(self, unique_id, error_code, error_description, error_details=None):
        self.unique_id = unique_id
        self.error_code = error_code
        self.error_description = error_description
        self.error_details = error_details

    def to_json(self):
        return ujson.dumps(
            [
                self.message_type_id,
                self.unique_id,
                self.error_code,
                self.error_description,
                self.error_details,
            ],
            # By default ujson.dumps() adds a white space after every separator.
            # By setting the separator manually that can be avoided.
            # separators=(",", ":"),
        )

    def to_exception(self):
        """Return the exception that corresponds to the CallError."""
        for error in OCPPError.__subclasses__():
            if error.code == self.error_code:
                return error(
                    self.error_description, self.error_details
                )

        raise UnknownCallErrorCodeError(
            None, "Error code '{}' is not defined by the OCPP specification".format(self.error_code)
        )

    def __repr__(self):
        return (
            "<CallError - unique_id={}, error_code={}, error_description={}, error_details={}>".format(
                self.unique_id, self.error_code, self.error_description, self.error_details
            )
        )
