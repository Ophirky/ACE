"""
    main file of the transmitting client
"""
import multiprocessing

from src.server.tc_handler.audio_receive_handler import AudioReceiveHandler
from src.server.utils.consts.global_consts import Queues
from src.server.tc_handler.syncer import FrameSyncer
from src.server.tc_handler.video_receive_handler import VideoReceiveHandler


class TCHandle:
    """
    Handles TC reception run
    """

    def __init__(self) -> None:
        """
        Initiates the TCHandle class.
        :return: None
        """
        self._video_process = multiprocessing.Process(target=VideoReceiveHandler.recv_video, args=[Queues.VIDEO_QUEUE])
        self._audio_process = multiprocessing.Process(target=AudioReceiveHandler.recv_audio, args=[Queues.AUDIO_QUEUE])
        self._syncer_process = multiprocessing.Process(target=self._syncer_handle, args=(Queues.VIDEO_QUEUE,
                                                                                         Queues.AUDIO_QUEUE,
                                                                                         Queues.SYNCED_QUEUE))

        # Start processes
        self._video_process.start()
        self._audio_process.start()
        self._syncer_process.start()

    @staticmethod
    def _syncer_handle(video_queue: multiprocessing.Queue,
                       audio_queue: multiprocessing.Queue,
                       synced_queue: multiprocessing.Queue) -> None:
        """
        Handling the init of the syncer process.

        :param video_queue: (multiprocessing.Queue) The video frames queue
        :param audio_queue: (multiprocessing.Queue) The audio chunks queue
        :param synced_queue: (multiprocessing.Queue) The synced audio and frames queue
        :return: None
        """
        FrameSyncer(video_queue, audio_queue, synced_queue).sync_frames()

    def tc_join(self) -> None:
        """
        Starts streaming
        :return: None
        """
        self._video_process.join()
        self._audio_process.join()
        self._syncer_process.join()
