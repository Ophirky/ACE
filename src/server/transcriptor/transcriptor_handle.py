"""
    This file handles the transcription and display of the final frames
"""
# Imports #
from multiprocessing import Process, Queue
from src.server.utils.consts.global_consts import Queues

from src.server.transcriptor.media_processor import MediaProcessor


class TranscriptorHandle:
    """
    Handles transcriptor run
    """

    def __init__(self, synced_queue: Queue, transcribed_queue: Queue) -> None:
        """
        Initiates the TranscriptorHandle class.
        :return: None
        """
        self._mp_process = Process(target=self._mp_process_handle, args=(synced_queue, transcribed_queue))
        self._mp_process.start()

    @staticmethod
    def _mp_process_handle(synced_queue: Queue, transcribed_queue: Queue) -> None:
        """
        Handle MediaProcessor init.

        :param synced_queue: (multiprocessing.Queue) The synced frames queue.
        :param transcribed_queue: (multiprocessing.Queue) The transcribed frames queue.
        :return: None
        """
        MediaProcessor(synced_queue, transcribed_queue).transcript_frames()

    def transcriptor_join(self) -> None:
        """
        Handles transcriptor init.
        :return: None
        """
        self._mp_process.join()
