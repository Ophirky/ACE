"""
    main file of the server client
"""

from tc_handler.tc_handle import TCHandle
from transcriptor.transcriptor_handle import TranscriptorHandle


def main() -> None:
    """
    Starts streaming
    :return: None
    """
    # Starting processes
    tc_handle = TCHandle()
    transcriptor_handle = TranscriptorHandle()

    # Joining processes to main process
    tc_handle.tc_join()
    transcriptor_handle.transcriptor_join()


if __name__ == '__main__':
    main()
