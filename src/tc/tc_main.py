"""
    main file of the transmitting client
"""
import multiprocessing
import time
import pyaudio

from audio_transmission_handler import AudioTransmissionHandler
from video_transmission_handler import VideoTransmission


def audio_handle(start_stamp, input_port) -> None:
    AudioTransmissionHandler(start_stamp, input_port).start_streaming()


def video_handle(start_stamp) -> None:
    VideoTransmission(start_stamp).transmit_video()


def tc_main() -> None:
    """
    Starts streaming
    :return: None
    """
    start_timestamp = int(time.time() * 1000) % (2 ** 32)

    # choose microphone
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        if device_info['maxInputChannels'] != 0 and device_info['hostApi'] == 0:
            print('Device ' + str(i) + ': ' + device_info['name'])
    inp = int(input("> "))

    video_process = multiprocessing.Process(target=video_handle, args=[start_timestamp])
    audio_process = multiprocessing.Process(target=audio_handle, args=(start_timestamp, inp))

    # Start processes
    video_process.start()
    audio_process.start()

    # Keep the main program running
    video_process.join()
    audio_process.join()


if __name__ == '__main__':
    tc_main()
