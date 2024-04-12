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

_OCPPErrorSubClasses_ = []


class OCPPError(Exception):
    """Base class for all OCPP errors. It shouldn't be raised, only it
    subclasses.
    """

    default_description = ""

    def __init__(self, *args):
        self.description = args[0] if len(args) > 0 and args[0] else self.default_description
        self.details = args[1] if len(args) > 1 and args[1] else {}

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.description, self.details) == (
                other.description,
                other.details,
            )

        return NotImplemented

    def __repr__(self):
        return (
            "<{} - description={}, details={}>".format(
                self.__class__.__name__, self.description, self.details
            )
        )

    def __str__(self):
        return "{}: {}, {}".format(
            self.__class__.__name__, self.description, self.details
        )

    @staticmethod
    def __subclasses__():
        return _OCPPErrorSubClasses_


class NotImplementedError(OCPPError):
    code = "NotImplemented"
    default_description = (
        "Request Action is recognized but not supported by the receiver"
    )


class NotSupportedError(OCPPError):
    code = "NotSupported"
    default_description = "Requested Action is not known by receiver"


class InternalError(OCPPError):
    code = "InternalError"
    default_description = (
        "An internal error occurred and the receiver was "
        "able to process the requested Action successfully"
    )


class ProtocolError(OCPPError):
    code = "ProtocolError"
    default_description = "Payload for Action is incomplete"


class SecurityError(OCPPError):
    code = "SecurityError"
    default_description = (
        "During the processing of Action a security issue "
        "occurred preventing receiver from completing the "
        "Action successfully"
    )


class FormatViolationError(OCPPError):
    """
    Not strict OCPP 1.6 - see FormationViolationError
    Valid OCPP 2.0.1
    """

    code = "FormatViolation"
    default_description = (
        "Payload for Action is syntactically incorrect or " "structure for Action"
    )


class FormationViolationError(OCPPError):
    """
    To allow for strict OCPP 1.6 compliance
        5. Known issues that will not be fixed
        5.2. Page 14, par 4.2.3. CallError: incorrect name in enum: FormationViolation
        Incorrect name in enum: FormationViolation
    """

    code = "FormationViolation"
    default_description = (
        "Payload for Action is syntactically incorrect or structure for Action"
    )


class PropertyConstraintViolationError(OCPPError):
    code = "PropertyConstraintViolation"
    default_description = (
        "Payload is syntactically correct but at least "
        "one field contains an invalid value"
    )


class OccurenceConstraintViolationError(OCPPError):
    """
    To allow for strict OCPP 1.6 compliance
    ocpp-j-1.6-errata-sheet.pdf
        5. Known issues that will not be fixed
        5.1. Page 14, par 4.2.3: CallError: Typo in enum
        Typo in enum: OccurenceConstraintViolation
    Valid in 2.0.1
    """

    code = "OccurenceConstraintViolation"
    default_description = (
        "Payload for Action is syntactically correct but "
        "at least one of the fields violates occurence "
        "constraints"
    )


class OccurrenceConstraintViolationError(OCPPError):
    """
    Not strict OCPP 1.6 - see OccurenceConstraintViolationError
    Not valid OCPP 2.0.1
    Valid in OCPP 2.1
    """

    code = "OccurrenceConstraintViolation"
    default_description = (
        "Payload for Action is syntactically correct but "
        "at least one of the fields violates occurence "
        "constraints"
    )


class TypeConstraintViolationError(OCPPError):
    code = "TypeConstraintViolation"
    default_description = (
        "Payload for Action is syntactically correct but "
        "at least one of the fields violates data type "
        "constraints (e.g. “somestring”: 12)"
    )


class GenericError(OCPPError):
    code = "GenericError"
    default_description = "Any other error not all other OCPP defined errors"


class ValidationError(Exception):
    """ValidationError should be raised if validation a message payload fails.

    Note this isn't an official OCPP error!
    """

    pass


class UnknownCallErrorCodeError(Exception):
    """Raised when a CALLERROR is received with unknown error code."""

    pass


class TimeoutError(Exception):
    pass


class SchemaValidationError(Exception):

    def __init__(self, *args):
        self.validator = args[0] if len(args) > 0 and args[0] else ""
        self.message = args[1] if len(args) > 1 and args[1] else ""

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.validator, self.message) == (
                other.validator,
                other.message,
            )

        return NotImplemented

    def __repr__(self):
        return (
            "<{} - validator={}, message={}>".fotmat(
                self.__class__.__name__, self.validator, self.message
            )
        )

    def __str__(self):
        return "{}: {}, {}".format(
            self.__class__.__name__, self.validator, self.message
        )


_OCPPErrorSubClasses_ = [cls for _, cls in locals().items() if _.endswith("Error") and issubclass(cls, OCPPError)]
