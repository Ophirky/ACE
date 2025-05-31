"""
    This file holds the RTP handler class -
"""
# Imports #
import math
import random
import struct
import time
import zlib

from utils import consts
from utils.payload_types import PayloadTypes
from utils.logger import Logger


class RTPHandler:
    """
    This class handles the RTP protocol, including creating and parsing RTP packets.
    """

    def __init__(self, payload_type: PayloadTypes, start_timestamp=(int(time.time() * 1000) % (2 ** 32))) -> None:
        """
        Initializes the RTPHandler instance.

        :param start_timestamp: (int) The start_timestamp for the object
        :param payload_type: (PayloadTypes) The payload type for the RTP stream.
        :return: None
        """

        self.payload_type = payload_type.value
        self.ssrc = random.randint(0, 2 ** 32 - 1)  # Generate a random 32-bit SSRC
        self.sequence_number = 0
        self.timestamp = start_timestamp
        self._update_timestamp()

        self.logger = Logger("rtp-logger").logger

    def build_header(self, marker: int = 0, csrcs: list[int] = None, extension_data: bytes = None) -> bytes:
        """
        Constructs the RTP header.

        :param extension_data:
        :param marker: (int) The marker bit.
        :param csrcs: (list[int]) List of contributing source identifiers.
        :return: bytes: The RTP header as a byte string.
        """
        if csrcs is None:
            csrcs = []

        cc = len(csrcs)
        version = 2
        padding = 0
        extension = extension_data is not None
        self.sequence_number += 1

        header = (
                (version << 30) |
                (padding << 29) |
                (extension << 28) |
                (cc << 24) |
                (marker << 23) |
                (self.payload_type << 16) |
                (self.sequence_number & 0xFFFF)
        )
        header_bytes = struct.pack('!II', header, self.timestamp)
        ssrc_bytes = struct.pack('!I', self.ssrc)
        csrc_bytes = b''.join(struct.pack('!I', csrc) for csrc in csrcs)
        extension_bytes = b''
        if extension_data:
            extension_profile_id = consts.CommunicationConsts.RTP_EXTENSION_PROFILE_ID
            extension_length = struct.pack('!I', math.ceil(len(extension_data) / 4))[2:]
            extension_header = consts.CommunicationConsts.RTP_EXTENSION_HEADER
            extension_bytes = extension_profile_id + extension_length + extension_header + extension_data

        return header_bytes + ssrc_bytes + csrc_bytes + extension_bytes

    def create_packets(self, payload: bytes ,csrcs: list[int] = None) -> list[bytes]:
        """
        Creates an RTP packet by combining the header and payload.

        :param payload: (bytes) payload to put in the rtp packet
        :param csrcs: (list[int]) List of contributing source identifiers.
        :return: bytes: The complete RTP packet.
        """
        try:
            payload = zlib.compress(payload)

            self._update_timestamp()

            payloads = []
            payload_pointer = 0
            header_len = len(self.build_header(0, csrcs, extension_data=struct.pack('!I', len(payloads))))
            while payload_pointer < len(payload):
                payload_read_end_index = payload_pointer + consts.CommunicationConsts.MAX_UDP_PAYLOAD_SIZE - header_len
                # payload_read_end_index = payload_pointer + 1500 - header_len
                payloads.append(payload[payload_pointer:payload_read_end_index])
                payload_pointer = payload_read_end_index

            ext_data = struct.pack('!I', len(payloads))

            packets = []
            for i in range(len(payloads)):
                is_last_frag = i == len(payloads) - 1
                header = self.build_header(int(is_last_frag), csrcs, extension_data=ext_data)
                packets.append(header + payloads[i])

            self.logger.info("RTP packets created successfully.")

        except Exception as e:
            self.logger.exception("Error while creating RTP packet: %s", e)
            raise

        return packets

    def get_ssrc(self) -> int:
        """
        Returns the SSRC for the RTP stream.

        :return: int: The SSRC value.
        """
        return self.ssrc

    def _update_timestamp(self) -> None:
        """
        :return:
        """
        self.timestamp = int(time.time() * 1000) % (2 ** 32)  # Initialize with current time in milliseconds & 32 bit
