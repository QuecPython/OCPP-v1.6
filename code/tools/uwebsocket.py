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

"""
@file      : uwebsocket.py
@author    : Jack Sun (jack.sun@quectel.com)
@brief     : <Description>
@version   : v1.0.0
@date      : 2024-03-27 09:02:33
@copyright : Copyright (c) 2024
"""

import log
import ure as re
import usocket as socket
import urandom as random
import ustruct as struct
import ubinascii as binascii
from ucollections import namedtuple

LOGGER = log.getLogger(__name__)

# Opcodes
OP_CONT = 0x0
OP_TEXT = 0x1
OP_BYTES = 0x2
OP_CLOSE = 0x8
OP_PING = 0x9
OP_PONG = 0xa

# Close codes
CLOSE_OK = 1000
CLOSE_GOING_AWAY = 1001
CLOSE_PROTOCOL_ERROR = 1002
CLOSE_DATA_NOT_SUPPORTED = 1003
CLOSE_BAD_DATA = 1007
CLOSE_POLICY_VIOLATION = 1008
CLOSE_TOO_BIG = 1009
CLOSE_MISSING_EXTN = 1010
CLOSE_BAD_CONDITION = 1011

URL_RE = re.compile(r'(wss|ws)://([A-Za-z0-9-\.]+)(?:\:([0-9]+))?(/.+)?')
URI = namedtuple('URI', ('protocol', 'hostname', 'port', 'path'))


def urlparse(uri):
    """Parse ws:// URLs"""
    match = URL_RE.match(uri)
    if match:
        protocol = match.group(1)
        host = match.group(2)
        port = match.group(3)
        path = match.group(4)

        if protocol == 'wss':
            if port is None:
                port = 443
        elif protocol == 'ws':
            if port is None:
                port = 80
        else:
            raise ValueError('Scheme {} is invalid'.format(protocol))

        return URI(protocol, host, int(port), path)


class NoDataException(Exception):
    pass


class ConnectionClosed(Exception):
    pass


class Websocket(object):
    """
    Basis of the Websocket protocol.

    This can probably be replaced with the C-based websocket module, but
    this one currently supports more options.
    """
    is_client = False

    def __init__(self, sock, debug=False):
        self.sock = sock
        self.open = True
        self.debug = debug

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def settimeout(self, timeout):
        self.sock.settimeout(timeout)

    def read_frame(self, max_size=None):
        """
        Read a frame from the socket.
        See https://tools.ietf.org/html/rfc6455#section-5.2 for the details.
        """

        # Frame header
        two_bytes = self.sock.read(2)

        if not two_bytes:
            raise NoDataException

        byte1, byte2 = struct.unpack('!BB', two_bytes)

        # Byte 1: FIN(1) _(1) _(1) _(1) OPCODE(4)
        fin = bool(byte1 & 0x80)
        opcode = byte1 & 0x0f

        # Byte 2: MASK(1) LENGTH(7)
        mask = bool(byte2 & (1 << 7))
        length = byte2 & 0x7f

        if length == 126:  # Magic number, length header is 2 bytes
            length, = struct.unpack('!H', self.sock.read(2))
        elif length == 127:  # Magic number, length header is 8 bytes
            length, = struct.unpack('!Q', self.sock.read(8))

        if mask:  # Mask is 4 bytes
            mask_bits = self.sock.read(4)

        try:
            data = self.sock.read(length)
        except MemoryError:
            # We can't receive this many bytes, close the socket
            if self.debug:
                LOGGER.info("Frame of length %s too big. Closing", length)
            self.close(code=CLOSE_TOO_BIG)
            return True, OP_CLOSE, None

        if mask:
            data = bytes(b ^ mask_bits[i % 4]
                         for i, b in enumerate(data))

        return fin, opcode, data

    def write_frame(self, opcode, data=b''):
        """
        Write a frame to the socket.
        See https://tools.ietf.org/html/rfc6455#section-5.2 for the details.
        """
        fin = True
        mask = self.is_client  # messages sent by client are masked

        length = len(data)

        # Frame header
        # Byte 1: FIN(1) _(1) _(1) _(1) OPCODE(4)
        byte1 = 0x80 if fin else 0
        byte1 |= opcode

        # Byte 2: MASK(1) LENGTH(7)
        byte2 = 0x80 if mask else 0

        if length < 126:  # 126 is magic value to use 2-byte length header
            byte2 |= length
            self.sock.write(struct.pack('!BB', byte1, byte2))

        elif length < (1 << 16):  # Length fits in 2-bytes
            byte2 |= 126  # Magic code
            self.sock.write(struct.pack('!BBH', byte1, byte2, length))

        elif length < (1 << 64):
            byte2 |= 127  # Magic code
            self.sock.write(struct.pack('!BBQ', byte1, byte2, length))

        else:
            raise ValueError()

        if mask:  # Mask is 4 bytes
            mask_bits = struct.pack('!I', random.getrandbits(32))
            self.sock.write(mask_bits)

            data = bytes(b ^ mask_bits[i % 4]
                         for i, b in enumerate(data))

        self.sock.write(data)

    def recv(self):
        """
        Receive data from the websocket.

        This is slightly different from 'websockets' in that it doesn't
        fire off a routine to process frames and put the data in a queue.
        If you don't call recv() sufficiently often you won't process control
        frames.
        """
        assert self.open

        while self.open:
            try:
                fin, opcode, data = self.read_frame()
            except NoDataException:
                self._close()
                raise ConnectionClosed()
                # return ""
            except ValueError:
                if self.debug:
                    LOGGER.info("Failed to read frame. Socket dead.")
                self._close()
                raise ConnectionClosed()

            if not fin:
                raise NotImplementedError()

            if opcode == OP_TEXT:
                return data.decode('utf-8')
            elif opcode == OP_BYTES:
                return data
            elif opcode == OP_CLOSE:
                self._close()
                return
            elif opcode == OP_PONG:
                # Ignore this frame, keep waiting for a data frame
                continue
            elif opcode == OP_PING:
                # We need to send a pong frame
                if self.debug:
                    LOGGER.info("Sending PONG")
                self.write_frame(OP_PONG, data)
                # And then wait to receive
                continue
            elif opcode == OP_CONT:
                # This is a continuation of a previous frame
                raise NotImplementedError(opcode)
            else:
                raise ValueError(opcode)

    def send(self, buf):
        """Send data to the websocket."""

        assert self.open

        if isinstance(buf, str):
            opcode = OP_TEXT
            buf = buf.encode('utf-8')
        elif isinstance(buf, bytes):
            opcode = OP_BYTES
        else:
            raise TypeError()

        self.write_frame(opcode, buf)

    def close(self, code=CLOSE_OK, reason=''):
        """Close the websocket."""
        if not self.open:
            return

        buf = struct.pack('!H', code) + reason.encode('utf-8')

        self.write_frame(OP_CLOSE, buf)
        self._close()

    def _close(self):
        if self.debug:
            LOGGER.info("Connection closed")
        self.open = False
        self.sock.close()


class WebsocketClient(Websocket):
    is_client = True


class Client(object):

    @staticmethod
    def connect(uri, headers=None, debug=False):
        """
        Connect a websocket.
        :param uri: example ws://172.16.185.123/
        :param headers: k, v of header
        :param debug: allow output log
        :return:
        """
        if not headers:
            headers = dict()
        if not isinstance(headers, dict):
            raise Exception("headers must be dict type but {} you given.".format(type(headers)))

        uri = urlparse(uri)
        assert uri

        if debug:
            LOGGER.info("open connection %s:%s", uri.hostname, uri.port)

        sock = socket.socket()
        addr = socket.getaddrinfo(uri.hostname, uri.port)
        sock.connect(addr[0][4])

        if uri.protocol == 'wss':
            import ussl
            sock = ussl.wrap_socket(sock)

        def send_header(header, *args):
            if debug:
                LOGGER.info(str(header), *args)
            sock.write(header % args + '\r\n')

        # Sec-WebSocket-Key is 16 bytes of random base64 encoded
        key = binascii.b2a_base64(bytes(random.getrandbits(8) for _ in range(16)))[:-1]
        send_header(b'GET %s HTTP/1.1', uri.path or '/')
        send_header(b'Host: %s:%s', uri.hostname, uri.port)
        send_header(b'Connection: Upgrade')
        send_header(b'Upgrade: websocket')
        send_header(b'Sec-WebSocket-Key: %s', key)
        send_header(b'Sec-WebSocket-Version: 13')
        send_header(b'Origin: http://{hostname}:{port}'.format(
            hostname=uri.hostname,
            port=uri.port)
        )
        for k, v in headers.items():
            send_header('{}:{}'.format(k, v).encode())
        send_header(b'')

        header = sock.readline()[:-2]
        assert header.startswith(b'HTTP/1.1 101 '), header

        # We don't (currently) need these headers
        # FIXME: should we check the return key?
        while header:
            if debug:
                LOGGER.info(str(header))
            header = sock.readline()[:-2]

        return WebsocketClient(sock, debug)
