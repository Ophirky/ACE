"""
    Audio Handling
"""
# TODO: Add Logger
# Imports #
from multiprocessing import Queue
import pyaudio
import time

from src.server.tc_handler.udp_handler_generic import UDPServerHandler
from src.server.utils.consts.tc_consts import Ports, AudioConsts


class AudioReceiveHandler:
    """
    Handles real-time UDP audio reception with delta time synchronization.
    """

    @staticmethod
    def recv_audio(audio_queue: Queue) -> None:
        """
        Receives RTP audio packets and plays audio in real-time using delta time for better timing.

        :param audio_queue: (multiprocessing.Queue) queue to send the packets to
        :return: None
        """
        udp_handler = UDPServerHandler(Ports.AUDIO_PORT)  # Use correct port

        audio = pyaudio.PyAudio()
        stream = audio.open(format=AudioConsts.FORMAT,
                            channels=AudioConsts.CHANNELS,
                            rate=AudioConsts.SAMPLE_RATE,
                            output=True,
                            frames_per_buffer=AudioConsts.CHUNK_SIZE)

        expected_interval = 0.005  # 20ms expected interval
        timer = prev_time = time.time()
        packets_per_second = 0

        while True:
            try:
                audio_data = udp_handler.receive_rtp_message()
                if not audio_data or not audio_data[1]:
                    continue

                # print(type(audio_data))
                audio_queue.put(audio_data)

                packets_per_second += 1
                if time.time() - timer > 1:
                    # TODO: Add log
                    timer = time.time()
                    packets_per_second = 0

                current_time = time.time()
                delta_time = current_time - prev_time  # Time since last packet

                # If the server is ahead of schedule, wait
                if delta_time < expected_interval:
                    time.sleep(expected_interval - delta_time)

                prev_time = current_time  # Update last received timestamp

            except KeyboardInterrupt:
                break

        # Cleanup
        stream.stop_stream()
        stream.close()
        audio.terminate()
