"""
    Transmitting client main file.
"""
# Imports #
import threading
import time

from video_transmission_handler import VideoTransmission
from audio_transmission_handler import AudioTransmissionHandler


def main() -> None:
    """
    Main run of the transmitting client
    :return: None
    """
    start_timestamp = int(time.time() * 1000) % (2 ** 32)


if __name__ == '__main__':
    main()
