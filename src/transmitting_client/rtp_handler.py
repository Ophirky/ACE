"""
    This file holds the RTP handler class -
"""

# Imports #
import struct
import logging
import time
import random


class RTPHandler:
    """
    This class handles the RTP protocol, including creating and parsing RTP packets.
    """

    def __init__(self, payload_type: int) -> None:
        """
        Initializes the RTPHandler instance.

        :param payload_type: (int) The payload type for the RTP stream.
        :return: None
        """
        self.payload_type = payload_type
        self.ssrc = random.randint(0, 2 ** 32 - 1)  # Generate a random 32-bit SSRC
        self.sequence_number = 0
        self.timestamp = int(time.time() * 1000)  # Initialize with current time in milliseconds

    def build_header(self, marker: int = 0, csrcs: list[int] = None) -> bytes:
        """
        Constructs the RTP header.

        :param marker: (int) The marker bit.
        :param csrcs: (list[int]) List of contributing source identifiers.
        :return: bytes: The RTP header as a byte string.
        """
        if csrcs is None:
            csrcs = []

        cc = len(csrcs)
        version = 2
        padding = 0
        extension = 0

        header = (
                (version << 30) |
                (padding << 29) |
                (extension << 28) |
                (cc << 24) |
                (marker << 23) |
                (self.payload_type << 16) |
                (self.sequence_number & 0xFFFF)
        )
        self.sequence_number += 1

        header_bytes = struct.pack('!II', header, self.timestamp)
        ssrc_bytes = struct.pack('!I', self.ssrc)
        csrc_bytes = b''.join(struct.pack('!I', csrc) for csrc in csrcs)

        return header_bytes + ssrc_bytes + csrc_bytes

    def create_packet(self, payload: bytes, marker: int = 0, csrcs: list[int] = None) -> bytes:
        """
        Creates an RTP packet by combining the header and payload.

        :param payload: (bytes) The payload data to include in the packet.
        :param marker: (int) The marker bit.
        :param csrcs: (list[int]) List of contributing source identifiers.
        :return: bytes: The complete RTP packet.
        """
        try:
            header = self.build_header(marker, csrcs)
            packet = header + payload
            logging.info("RTP packet created successfully.")
            return packet
        except Exception as e:
            logging.exception("Error while creating RTP packet: %s", e)
            raise

    def get_ssrc(self) -> int:
        """
        Returns the SSRC for the RTP stream.

        :return: int: The SSRC value.
        """
        return self.ssrc
