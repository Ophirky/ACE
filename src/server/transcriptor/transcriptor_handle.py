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

    def __init__(self) -> None:
        """
        Initiates the TranscriptorHandle class.
        :return: None
        """
        self._mp_process = Process(target=self._mp_process_handle, args=[Queues.SYNCED_QUEUE])
        self._mp_process.start()

    @staticmethod
    def _mp_process_handle(synced_queue: Queue) -> None:
        """
        Handle MediaProcessor init.

        :param synced_queue: (multiprocessing.Queue) The synced frames queue.
        :return: None
        """
        MediaProcessor(synced_queue).transcript_frames()

    def transcriptor_join(self) -> None:
        """
        Handles transcriptor init.
        :return: None
        """
        self._mp_process.join()
