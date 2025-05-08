"""
    Will hold the class in charge of communications
"""
# Imports #
import logging
import socket
import struct
import zlib

import cv2
import numpy as np

from src.server.transmitting_client_handler.rtp_parser import RTPPacketDecoder
from src.server.utils.consts.logging_messages import *
from src.server.utils.consts.udp_consts import CommunicationConsts


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
        logging.info(SuccessMessages.SERVER_LISTENING.format(self.bind_address, self.bind_port))

    def __receive_packet(self, buffer: int) -> bytes:
        """
        Will receive a packet using a UDP connection
        :param buffer: the buffer to receive
        :return: the received packet
        """
        packet = b''
        try:
            packet, _ = self.sock.recvfrom(buffer)
        except socket.error as e:
            logging.exception("NETWORK ERROR: ", e)

        return packet

    def assemble_frame(self, seq_start, seq_end):
        """
        #TODO: ADD DOCS (P.S. EAT DICK)
        :param seq_start:
        :param seq_end:
        :return:
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
        while True:
            try:
                packet = self.__receive_packet(CommunicationConsts.BUFFER_SIZE)
                if not packet:
                    logging.debug("Got a None Packet")
                    continue
                else:
                    decoded_packet = RTPPacketDecoder(packet)

                # decoded_packet = RTPPacketDecoder(self.__receive_packet(CommunicationConsts.BUFFER_SIZE))
                if len(self._uncompleted_frame_packets) > 0 and \
                        next(iter(self._uncompleted_frame_packets.values())).timestamp < decoded_packet.timestamp:
                    self._uncompleted_frame_packets = dict()

                self._uncompleted_frame_packets[decoded_packet.sequence_number] = decoded_packet

                if decoded_packet.marker != CommunicationConsts.EXPECT_ANOTHER_FRAGMENT:
                    seq_start = decoded_packet.sequence_number - \
                                struct.unpack('!I', decoded_packet.extension_data)[0] + 1
                    # print(self._uncompleted_frame_packets.keys())
                    frame_data = self.assemble_frame(seq_start, decoded_packet.sequence_number)
                    if frame_data is None:
                        continue

                    # Decode the frame data and reshape it into a frame
                    # Assuming a standard resolution (e.g., 640x480) and 3 channels for RGB
                    array = np.frombuffer(frame_data, dtype=np.uint8)
                    # frame = array.reshape((480, 640, 3))
                    frame = np.resize(array, (240, 320, 3))

                    frame = cv2.resize(frame, (640, 480))

                    # Display the frame using OpenCV
                    cv2.imshow("Received Video", frame)

                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            except socket.error as e:
                logging.exception(ErrorMessages.VIDEO_RECEIVING_ERROR, e)
                break

        # Cleanup OpenCV windows after exiting the loop
        cv2.destroyAllWindows()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
        datefmt="%Y-%m-%d %H:%M:%S"  # Date format
    )

    logging.debug("Software is awake.")
    UDPServerHandler().receive_video()
