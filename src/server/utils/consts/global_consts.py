"""
    This file holds the global constants that are used in more than one component
"""
# Imports #
from multiprocessing import Queue

class Queues:
    """
    Queues that are used to transfer data between processes
    """
    AUDIO_QUEUE = Queue()
    VIDEO_QUEUE = Queue()
    SYNCED_QUEUE = Queue()
    TRANSCRIBED_QUEUE = Queue()
