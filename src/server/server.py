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
    # Starting processes

    ws_process = multiprocessing.Process(target=websocket_process, args=[Queues.TRANSCRIBED_QUEUE])
    ws_process.start()

    tc_handle = TCHandle()
    transcriptor_handle = TranscriptorHandle()

    # Joining processes to main process
    ws_process.join()
    tc_handle.tc_join()
    transcriptor_handle.transcriptor_join()


if __name__ == '__main__':
    main()
