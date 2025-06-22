"""
    This file holds the MediaProcessor class.
"""
# TODO: SEND TO RC
# Imports #
import multiprocessing
import cv2
from numpy import ndarray

from src.server.transcriptor.merger import Merger
from src.server.transcriptor.transcript import Transcriptor
from src.server.utils.consts.global_consts import Queues


class MediaProcessor:
    """
    Handles real-time processing of video frames and audio transcription.
    """

    def __init__(self, synced_queue: multiprocessing.Queue, transcribed_queue: multiprocessing.Queue) -> None:
        """
        Initializes the MediaProcessor class.

        :param synced_queue: (multiprocessing.Queue) The synced frames queue.
        :param transcribed_queue: (multiprocessing.Queue) The transcribed frames queue.
        :return: None
        """
        self._transcriptor = Transcriptor()
        self._synced_queue = synced_queue
        self._transcribed_queue = transcribed_queue

    def _process_media(self, frame: ndarray, audio_chunk: bytes) -> ndarray:
        """
        Receives a video frame and audio chunk, then overlays subtitles.

        :param frame: (numpy.ndarray) The video frame to process.
        :param audio_chunk: (bytes) The corresponding audio data.
        :return numpy.ndarray: The final frame with subtitles.
        """
        audio_data = audio_chunk
        if not audio_chunk:
            audio_data = b""

        transcribed_text = self._transcriptor.transcript_chunk(audio_data)
        processed_frame = Merger.overlay_text(frame, transcribed_text)

        return processed_frame

    def transcript_frames(self) -> None:
        """
        Transcribing text and putting it on frames.
        :return: None
        """
        while True:
            if not self._synced_queue.empty():
                frame, audio_chunk = self._synced_queue.get()
                processed = self._process_media(frame, audio_chunk)

                cv2.imshow("transcripted", processed)
                self._transcribed_queue.put(processed)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Allows user to close window gracefully

        cv2.destroyAllWindows()  # Cleans up when loop exits
