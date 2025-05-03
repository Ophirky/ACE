"""
    This file holds the RTP handler class -
"""
# Imports #
import logging
import math
import random
import struct
import time

import numpy as np

from src.transmitting_client.utils import consts
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
        self.timestamp = None
        self._update_timestamp()

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
            print(extension_length)
            extension_header = consts.CommunicationConsts.RTP_EXTENSION_HEADER
            extension_bytes = extension_profile_id + extension_length + extension_header + extension_data

        # print(header_bytes + ssrc_bytes + csrc_bytes + extension_bytes)

        return header_bytes + ssrc_bytes + csrc_bytes + extension_bytes

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

    @staticmethod
    def __assert_max_resolution(payload: bytes) -> None:
        """
        TODO: ADD DOCS
        :param payload: 
        :return: 
        """
        assert len(payload) <= consts.CommunicationConsts.MAX_FRAME_SIZE

    def create_packets(self, csrcs: list[int] = None) -> list[bytes]:
        """
        Creates an RTP packet by combining the header and payload.

        :param csrcs: (list[int]) List of contributing source identifiers.
        :return: bytes: The complete RTP packet.
        """
        try:
            current_frame_data = self.get_frame()[1]
            payload = self.encode_frame(current_frame_data)
            # self.__assert_max_resolution(payload)
            required_frames_number = math.ceil(len(payload) / consts.CommunicationConsts.MAX_RTP_PAYLOAD_SIZE)

            self._update_timestamp()

            payloads = []
            payload_pointer = 0
            header_len = len(self.build_header(0, csrcs, extension_data=struct.pack('!I', len(payloads))))
            is_last_frag = 0
            while payload_pointer < len(payload):
                payload_read_end_index = payload_pointer + consts.CommunicationConsts.MAX_UDP_PAYLOAD_SIZE - header_len
                payloads.append(payload[payload_pointer:payload_read_end_index])
                payload_pointer = payload_read_end_index

            ext_data = struct.pack('!I', len(payloads))

            packets = []
            for i in range(len(payloads)):
                is_last_frag = i == len(payloads) - 1
                header = self.build_header(int(is_last_frag), csrcs, extension_data=ext_data)
                packets.append(header + payloads[i])

            logging.info("RTP packets created successfully.")

        except Exception as e:
            logging.exception("Error while creating RTP packet: %s", e)
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
