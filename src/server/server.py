"""
    main file of the server client
"""
# Imports #
import multiprocessing

from rc.rc_server import websocket_process
from tc_handler.tc_handle import TCHandle
from transcriptor.transcriptor_handle import TranscriptorHandle
from utils.consts.global_consts import Queues


def main() -> None:
    """
    Starts streaming
    :return: None
    """
    TRANSCRIBED_QUEUE = multiprocessing.Queue()
    SYNCED_QUEUE = multiprocessing.Queue()

    # Starting processes
    ws_process = multiprocessing.Process(target=websocket_process, args=(TRANSCRIBED_QUEUE,))
    ws_process.start()

    tc_handle = TCHandle(SYNCED_QUEUE)
    transcriptor_handle = TranscriptorHandle(transcribed_queue=TRANSCRIBED_QUEUE, synced_queue=SYNCED_QUEUE)

    # Joining processes to main process
    ws_process.join()
    tc_handle.tc_join()
    transcriptor_handle.transcriptor_join()


if __name__ == '__main__':
    main()
