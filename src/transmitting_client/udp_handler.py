"""
    Will hold the class incharge of communications
"""
import logging
# Imports #
import socket
import time

from rtp_handler import RTPHandler
from utils.consts import CommunicationConsts
from utils.logging_messages import *


class UDPClientHandler:
    """
        This class represents the video transmitting client using UDP.
        It initializes an RTPHandler instance to handle RTP packet creation
        and uses a UDP socket for sending packets.
    """

    def __init__(self, video_capture_source: int):
        """
        Initializes the Client instance.

        :param video_capture_source: (int) The camera / capture device source (given through the gui).
        :return: None
        """
        self.server_address = CommunicationConsts.HOST
        self.server_port = CommunicationConsts.PORT
        self.rtp_handler = RTPHandler(CommunicationConsts.PAYLOAD_TYPE, video_capture_source)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def transmit_video(self):
        """
        Captures video frames, creates RTP packets, and transmits them to the server via UDP.
        """
        while True:
            try:
                # Capture start time
                start_time = time.time()

                # Create RTP packet
                packets = self.rtp_handler.create_packets()

                # Send the packet to the server
                logging.debug("Sending frame, fragmented into {} packets".format(len(packets)))
                for packet in packets:
                    self.sock.sendto(packet, (self.server_address, self.server_port))
                logging.info(SuccessMessages.PACKET_SENT)

                # Handling delta time
                delta_time = time.time() - start_time
                time.sleep(max(0.033 - delta_time, 0))  # ~30 frames per second

            except Exception as e:
                logging.exception(ErrorMessages.VIDEO_TRANSMISSION_ERROR, e)
                break


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
        datefmt="%Y-%m-%d %H:%M:%S"  # Date format
    )
    logging.debug("Software is awake.")
    UDPClientHandler(0).transmit_video()
