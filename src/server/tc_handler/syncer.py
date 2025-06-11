"""
    This file Holds the FrameSyncer class
"""
import multiprocessing
# Imports #
from collections import OrderedDict


class FrameSyncer:
    """Orders & syncs incoming video frames and audio chunks before sending to Transcriptor."""

    def __init__(self,
                 video_queue: multiprocessing.Queue,
                 audio_queue: multiprocessing.Queue,
                 synced_queue: multiprocessing.Queue):
        self.video_queue = video_queue
        self.audio_queue = audio_queue
        self.synced_queue = synced_queue
        self.video_buffer = OrderedDict()  # Stores sorted video frames
        self.audio_buffer = OrderedDict()  # Stores sorted audio chunks

    def sync_frames(self):
        """Continuously sync ordered video frames with their closest audio chunks."""
        while True:
            # Store incoming audio in sorted buffer
            if not self.audio_queue.empty():
                timestamp, audio_chunk = self.audio_queue.get()
                self.audio_buffer[timestamp] = audio_chunk

            # Store incoming video in sorted buffer
            if not self.video_queue.empty():
                timestamp, video_frame = self.video_queue.get()
                self.video_buffer[timestamp] = video_frame

            # Process oldest available video frame
            if self.video_buffer:
                oldest_video_timestamp = next(iter(self.video_buffer))  # Get oldest timestamp
                video_frame = self.video_buffer.pop(oldest_video_timestamp)  # Remove after processing

                # Find the closest matching audio chunk
                if self.audio_buffer:
                    closest_audio_timestamp = min(self.audio_buffer.keys(),
                                                  key=lambda ts: abs(ts - oldest_video_timestamp))
                    synced_audio = self.audio_buffer.pop(closest_audio_timestamp)

                    # Store synced frame in final queue
                    self.synced_queue.put((video_frame, synced_audio))

