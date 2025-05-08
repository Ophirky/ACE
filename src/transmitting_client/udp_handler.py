"""
    Will hold the class incharge of communications
"""
# Imports #
import logging
import socket
import time

from rtp_handler import RTPHandler
from utils.consts import CommunicationConsts
from utils.logging_messages import *
from utils.payload_types import PayloadTypes


class UDPClientHandler:
    """
        This class represents the video transmitting client using UDP.
        It initializes an RTPHandler instance to handle RTP packet creation
        and uses a UDP socket for sending packets.
    """

    def __init__(self, port: int):
        """
        Initializes the Client instance.

        :param port: (int) the port to send the data through
        :return: None
        """
        self.server_address = CommunicationConsts.HOST
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_packets(self, packets: list[bytes]) -> bool:
        """
        Captures video frames, creates RTP packets, and transmits them to the server via UDP.
        :param packets: (list[bytes]) packets to send
        :return bool: whether operation was successful
        """
        success = True
        try:
            # Send the packet to the server
            logging.debug("Sending frame, fragmented into {} packets".format(len(packets)))
            for packet in packets:
                self.sock.sendto(packet, (self.server_address, self.server_port))
                # Handling shit computers TODO: fix comment
                time.sleep(0.01)
            logging.info(SuccessMessages.PACKET_SENT)

        except Exception as e:
            logging.exception(ErrorMessages.VIDEO_TRANSMISSION_ERROR, e)
            success = False

        return success
