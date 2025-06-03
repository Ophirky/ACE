import numpy as np
import pyaudio
import time

from src.server.transmitting_client_handler.udp_handler_generic import UDPServerHandler
from src.server.utils.consts.tc_consts import Ports, AudioConsts


class AudioReceiveHandler:
    """
    Handles real-time UDP audio reception with delta time synchronization.
    """

    @staticmethod
    def recv_audio() -> None:
        """
        Receives RTP audio packets and plays audio in real-time using delta time for better timing.
        :return: None
        """
        udp_handler = UDPServerHandler(Ports.AUDIO_PORT)  # Use correct port

        audio = pyaudio.PyAudio()
        stream = audio.open(format=AudioConsts.FORMAT,
                            channels=AudioConsts.CHANNELS,
                            rate=AudioConsts.SAMPLE_RATE,
                            output=True,
                            frames_per_buffer=AudioConsts.CHUNK_SIZE)

        print("Receiving Audio... Press Ctrl+C to stop.")

        prev_time = time.time()  # Track last packet timestamp
        expected_interval = 0.02  # 20ms expected interval for real-time audio

        while True:
            try:
                audio_data = udp_handler.receive_rtp_message()
                if not audio_data:
                    continue

                current_time = time.time()
                delta_time = current_time - prev_time  # Time difference since last packet

                # Adjust playback timing dynamically
                if delta_time < expected_interval:
                    time.sleep(expected_interval - delta_time)  # Compensate for timing drift

                # Convert received data into NumPy array
                audio_array = np.frombuffer(audio_data, dtype=np.int16)

                # Play received audio
                stream.write(audio_array.tobytes())

                prev_time = current_time  # Update last received packet time

            except KeyboardInterrupt:
                break

        # Cleanup
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Audio reception stopped.")


if __name__ == '__main__':
    AudioReceiveHandler.recv_audio()

