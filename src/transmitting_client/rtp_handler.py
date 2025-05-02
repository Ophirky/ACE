"""
    This file holds the RTP handler class -
"""

# Imports #
import struct
import logging
import time
import random
import numpy as np
import zlib

from src.transmitting_client.video_capture import VideoCapture


class RTPHandler(VideoCapture):
    """
    This class handles the RTP protocol, including creating and parsing RTP packets.
    """

    def __init__(self, payload_type: int, video_capture_source: int) -> None:
        """
        Initializes the RTPHandler instance.

        :param payload_type: (int) The payload type for the RTP stream.
        :param video_capture_source: (int) The camera / capture device.
        :return: None
        """
        super(RTPHandler, self).__init__(video_capture_source)

        self.payload_type = payload_type
        self.ssrc = random.randint(0, 2 ** 32 - 1)  # Generate a random 32-bit SSRC
        self.sequence_number = 0
        self.timestamp = int(time.time() * 1000) % (2 ** 32)  # Initialize with current time in milliseconds & 32 bit

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

    def encode_frame(self, frame: np.ndarray) -> bytes:
        """
        Encodes a NumPy video frame into bytes.

        :param frame: (np.ndarray) The video frame.
        :return: bytes: The encoded frame data.
        """
        try:
            return frame.tobytes()  # Convert NumPy array to bytes
        except Exception as e:
            logging.exception("Failed to encode video frame: %s", e)
            raise

    def create_packet(self, marker: int = 0, csrcs: list[int] = None) -> bytes:
        """
        Creates an RTP packet by combining the header and payload.

        :param marker: (int) The marker bit.
        :param csrcs: (list[int]) List of contributing source identifiers.
        :return: bytes: The complete RTP packet.
        """
        try:
            payload = self.encode_frame(self.get_frame()[1])
            header = self.build_header(marker, csrcs)
            packet = header + zlib.compress(payload)

            print(len(packet))

            logging.info("RTP packet created successfully.")

        except Exception as e:
            logging.exception("Error while creating RTP packet: %s", e)
            raise

        return packet

    def get_ssrc(self) -> int:
        """
        Returns the SSRC for the RTP stream.

        :return: int: The SSRC value.
        """
        return self.ssrc
