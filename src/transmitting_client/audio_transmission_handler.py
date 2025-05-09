"""
    This file holds the AudioTransmission class.
"""
# Imports #
import logging

from audio_capture import AudioCapture
from rtp_handler import RTPHandler
from udp_handler import UDPClientHandler
from utils.consts import CommunicationConsts
from utils.payload_types import PayloadTypes
from utils.logger import Logger


class AudioTransmissionHandler:
    """
    Handles real-time audio transmission via RTP over UDP.
    """

    def __init__(self):
        """
        Initializes the full audio streaming pipeline.
        """
        self.logger = Logger("audio-logger").logger
        self.audio_capture = AudioCapture(self.logger)
        self.rtp_handler = RTPHandler(PayloadTypes.AUDIO.value)
        self.udp_handler = UDPClientHandler(CommunicationConsts.AUDIO_PORT)

        self.logger.info("AudioTransmissionHandler initialized.")

    def start_streaming(self):
        """
        Begins live audio transmission.
        """
        self.logger.info("Starting live audio stream...")

        while True:
            try:
                # Capture live audio chunk
                audio_chunk = self.audio_capture.get_audio_chunk()

                # Wrap chunk in RTP packets
                rtp_packets = self.rtp_handler.create_packets(audio_chunk)

                # Send packets via UDP
                self.udp_handler.send_packets(rtp_packets)

            except Exception as e:
                self.logger.exception(f"Error during audio transmission: {e}")
                break

        self.stop_streaming()

    def stop_streaming(self):
        """ Cleans up resources after transmission stops. """
        self.logger.info("Stopping audio transmission...")
        self.audio_capture.release()
