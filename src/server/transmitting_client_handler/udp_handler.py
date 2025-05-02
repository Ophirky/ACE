"""
    Will hold the class in charge of communications
"""
# Imports #
import socket
import logging
import cv2
import numpy as np
from src.server.transmitting_client_handler.rtp_parser import RTPPacketDecoder
from src.server.utils.consts.udp_consts import CommunicationConsts
from src.server.utils.consts.logging_messages import *


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
        self.bind_address = CommunicationConsts.HOST.value
        self.bind_port = CommunicationConsts.PORT.value
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.bind_address, self.bind_port))
        logging.info(SuccessMessages.SERVER_LISTENING.value.format(self.bind_address, self.bind_port))

    def receive_video(self):
        """
        Receives RTP packets from the client, decodes them, and displays the video frames.
        """
        while True:
            try:
                # Receive RTP packet
                packet, _ = self.sock.recvfrom(CommunicationConsts.BUFFER_SIZE.value)

                # Decode the RTP packet
                decoder = RTPPacketDecoder(packet)
                frame_data = decoder.payload  # Extract the payload from the RTP packet

                # Decode the frame data and reshape it into a frame
                # Assuming a standard resolution (e.g., 640x480) and 3 channels for RGB
                array = np.frombuffer(frame_data, dtype=np.uint8)
                frame = array.reshape((480, 640, 3))

                # Display the frame using OpenCV
                cv2.imshow("Received Video", frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                logging.exception(ErrorMessages.VIDEO_RECEIVING_ERROR.value, e)
                break

        # Cleanup OpenCV windows after exiting the loop
        cv2.destroyAllWindows()


if __name__ == '__main__':
    UDPServerHandler().receive_video()
