import time
from audio_capture import AudioCapture
from rtp_handler import RTPHandler
from udp_handler import UDPClientHandler
from utils.consts import Ports
from utils.logger import Logger
from utils.payload_types import PayloadTypes


class AudioTransmissionHandler:
    """
    Handles real-time audio transmission via RTP over UDP with delta time synchronization.
    """

    def __init__(self):
        """
        Initializes the full audio streaming pipeline.
        """
        self.logger = Logger("audio-logger").logger
        self.audio_capture = AudioCapture(self.logger)
        self.rtp_handler = RTPHandler(PayloadTypes.AUDIO)
        self.udp_handler = UDPClientHandler(Ports.AUDIO_PORT.value)

        self.logger.info("AudioTransmissionHandler initialized.")

    def start_streaming(self):
        """
        Begins live audio transmission with delta time control for better synchronization.
        """
        self.logger.info("Starting live audio stream...")

        prev_send_time = time.time()  # Track last packet send time
        send_interval = 0.02  # 20ms expected interval for real-time audio

        while True:
            try:
                # Capture live audio chunk
                audio_chunk = self.audio_capture.get_audio_chunk()

                # Wrap chunk in RTP packets
                rtp_packets = self.rtp_handler.create_packets(audio_chunk)

                # Compute delta time
                current_time = time.time()
                delta_time = current_time - prev_send_time

                # Adjust sending rate dynamically
                if delta_time < send_interval:
                    time.sleep(send_interval - delta_time)  # Smooth out transmission timing

                # Send packets via UDP
                self.udp_handler.send_packets(rtp_packets)

                prev_send_time = current_time  # Update last sent timestamp

            except Exception as e:
                self.logger.exception(f"Error during audio transmission: {e}")
                break

        self.stop_streaming()

    def stop_streaming(self):
        """ Cleans up resources after transmission stops. """
        self.logger.info("Stopping audio transmission...")
        self.audio_capture.release()


if __name__ == '__main__':
    AudioTransmissionHandler().start_streaming()

