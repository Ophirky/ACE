"""
    This file Holds the FrameSyncer class
"""
# Imports #
import multiprocessing
import time
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
        # while True:
        #     # self.synced_queue.put((self.video_queue.get()[1], self.audio_queue.get()[1]))
        #     # Store incoming audio in sorted buffer
        #     if not self.audio_queue.empty():
        #         timestamp, audio_chunk = self.audio_queue.get()
        #         self.audio_buffer[timestamp] = audio_chunk
        #
        #     # Store incoming video in sorted buffer
        #     if not self.video_queue.empty():
        #         timestamp, video_frame = self.video_queue.get()
        #         self.video_buffer[timestamp] = video_frame
        #
        #     # Process oldest available video frame
        #     if self.video_buffer:
        #         oldest_video_timestamp = next(iter(self.video_buffer))  # Get oldest timestamp
        #         video_frame = self.video_buffer.pop(oldest_video_timestamp)  # Remove after processing
        #
        #         # Find the closest matching audio chunk
        #         if self.audio_buffer:
        #             closest_audio_timestamp = min(self.audio_buffer.keys(),
        #                                           key=lambda ts: abs(ts - oldest_video_timestamp))
        #             synced_audio = self.audio_buffer.pop(closest_audio_timestamp)
        #
        #             # Store synced frame in final queue
        #             self.synced_queue.put((video_frame, synced_audio))

        MAX_SYNCED_QUEUE_SIZE = 10  # Adjust based on your needs
        MAX_AUDIO_BUFFER_SIZE = 50  # Prevent audio buffer from growing too large
        MAX_VIDEO_BUFFER_SIZE = 50  # Prevent video buffer from growing too large

        while True:
            try:
                # Store incoming audio in sorted buffer
                if not self.audio_queue.empty():
                    timestamp, audio_chunk = self.audio_queue.get_nowait()
                    self.audio_buffer[timestamp] = audio_chunk

                    # Trim old audio if buffer gets too large
                    if len(self.audio_buffer) > MAX_AUDIO_BUFFER_SIZE:
                        oldest_audio = min(self.audio_buffer.keys())
                        self.audio_buffer.pop(oldest_audio)

                # Store incoming video in sorted buffer
                if not self.video_queue.empty():
                    timestamp, video_frame = self.video_queue.get_nowait()
                    self.video_buffer[timestamp] = video_frame

                    # Trim old video if buffer gets too large
                    if len(self.video_buffer) > MAX_VIDEO_BUFFER_SIZE:
                        oldest_video = min(self.video_buffer.keys())
                        self.video_buffer.pop(oldest_video)

                # Process frames if we have video and synced queue has space
                if (self.video_buffer and
                        self.synced_queue.qsize() < MAX_SYNCED_QUEUE_SIZE):

                    oldest_video_timestamp = next(iter(self.video_buffer))
                    video_frame = self.video_buffer.pop(oldest_video_timestamp)

                    # Find matching audio or use None if no audio available
                    synced_audio = None
                    if self.audio_buffer:
                        closest_audio_timestamp = min(self.audio_buffer.keys(),
                                                      key=lambda ts: abs(ts - oldest_video_timestamp))
                        synced_audio = self.audio_buffer.pop(closest_audio_timestamp)

                    # Always send the frame, even without audio
                    self.synced_queue.put((video_frame, synced_audio))

                # Small sleep to prevent CPU spinning
                time.sleep(0.001)

            except Exception as e:
                print(f"Syncer error: {e}")
                time.sleep(0.01)  # Longer sleep on error

