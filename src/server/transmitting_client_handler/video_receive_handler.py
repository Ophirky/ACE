"""
    This file holds the VideoReceiveHandler class
"""
# Imports #
import cv2
import numpy as np

from src.server.transmitting_client_handler.udp_handler_generic import UDPServerHandler
from src.server.utils.consts.tc_consts import Ports


class VideoReceiveHandler:
    """
    Handles real-time UDP video reception
    """

    # TODO: Handle sending video to merger
    @staticmethod
    def recv_video() -> None:
        """
        Receives video and presents it
        :return: None
        """
        udp_handler = UDPServerHandler(Ports.VIDEO_PORT)

        while True:
            frame = udp_handler.receive_rtp_message()
            array = np.frombuffer(frame, dtype=np.uint8)
            # frame = array.reshape((480, 640, 3))
            frame = np.resize(array, (240, 320, 3))

            frame = cv2.resize(frame, (640, 480))

            # Display the frame using OpenCV
            cv2.imshow("Received Video", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup OpenCV windows after exiting the loop
        cv2.destroyAllWindows()


if __name__ == '__main__':
    VideoReceiveHandler.recv_video()
