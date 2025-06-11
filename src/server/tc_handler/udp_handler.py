"""
    Will hold the class in charge of communications
"""
# Imports #
import logging
import zlib
import socket

import struct
import cv2
import numpy as np

from src.server.tc_handler.rtp_parser import RTPPacketDecoder
from src.server.utils.consts.logging_consts import *
from src.server.utils.consts.tc_consts import CommunicationConsts
from src.server.utils.logger import Logger


class UDPServerHandler:
    """
    This class represents the video receiving server using UDP.
    It initializes a UDP socket to listen for incoming packets and
    uses RTPacketDecoder to decode the received RTP packets.
    """

    def __init__(self):
        """
        Initializes the Server instance.

        :return: None
        """
        self.bind_address = CommunicationConsts.HOST
        self.bind_port = CommunicationConsts.PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.bind_address, self.bind_port))

        self._uncompleted_frame_packets = dict()

        self.sock.settimeout(CommunicationConsts.FRAGMENT_RECEIVE_TIMEOUT)

        self.logger = Logger("UDP-logger").logger

        self.logger.info(SuccessMessages.SERVER_LISTENING.format(self.bind_address, self.bind_port))

    def _receive_packet(self, buffer: int) -> bytes | None:
        """
        Will receive a packet using a UDP connection
        :param buffer: (int) the buffer to receive
        :return bytes | None: The received packet if one was received
        """
        packet = b''
        try:
            packet, _ = self.sock.recvfrom(buffer)
        except socket.timeout:
            self.logger.debug("Got a None packet")
            return None
        except socket.error as e:
            self.logger.exception("NETWORK ERROR: ", e)

        return packet

    def assemble_frame(self, seq_start: int, seq_end: int) -> bytes | None:
        """
        Assembles / Discards frames
        :param seq_start: (int) fragment sequence start
        :param seq_end: (int) fragment sequence end
        :return bytes | None: bytes if a frame was assembled, None if frame was dropped
        """
        frame = b''
        for seq in range(seq_start, seq_end + 1):
            packet = self._uncompleted_frame_packets.get(seq)
            if not packet:
                self._uncompleted_frame_packets = dict()
                return None
            assert isinstance(packet, RTPPacketDecoder)

            frame += packet.payload
        self._uncompleted_frame_packets = dict()

        return zlib.decompress(frame)

    def receive_video(self):
        """
        Receives RTP packets from the client, decodes them, and displays the video frames.
        """
        fps = 0
        import time
        start = time.time()
        while True:
            try:
                packet = self._receive_packet(CommunicationConsts.BUFFER_SIZE)
                if not packet:
                    self.logger.debug("Got a None Packet")
                    continue
                else:
                    decoded_packet = RTPPacketDecoder(packet)
                    self.logger.debug("Got a good packet")

                if len(self._uncompleted_frame_packets) > 0 and \
                        next(iter(self._uncompleted_frame_packets.values())).timestamp < decoded_packet.timestamp:
                    self._uncompleted_frame_packets = dict()

                self._uncompleted_frame_packets[decoded_packet.sequence_number] = decoded_packet

                if decoded_packet.marker != CommunicationConsts.EXPECT_ANOTHER_FRAGMENT:
                    seq_start = decoded_packet.sequence_number - \
                                struct.unpack('!I', decoded_packet.extension_data)[0] + 1

                    frame_data = self.assemble_frame(seq_start, decoded_packet.sequence_number)
                    if frame_data is None:
                        continue

                    array = np.frombuffer(frame_data, dtype=np.uint8)
                    # frame = array.reshape((480, 640, 3))
                    frame = np.resize(array, (240, 320, 3))

                    frame = cv2.resize(frame, (640, 480))

                    # Display the frame using OpenCV
                    cv2.imshow("Received Video", frame)

                    # Count fps #
                    fps += 1
                    if time.time() - start >= 1:
                        self.logger.info(f"FPS: {fps}")
                        fps = 0
                        start = time.time()

                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            except socket.error as e:
                self.logger.exception(ErrorMessages.VIDEO_RECEIVING_ERROR, e)
                break

        # Cleanup OpenCV windows after exiting the loop
        cv2.destroyAllWindows()


if __name__ == '__main__':
    UDPServerHandler().receive_video()
