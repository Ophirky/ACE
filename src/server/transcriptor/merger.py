"""
    This file holds the Merger class
"""
# Imports #
import cv2
from numpy import ndarray

from src.server.transcriptor.transcriptor_consts import MergerConsts

class Merger:
    """
    Handles video and transcription merging
    """
    @staticmethod
    def overlay_text(frame: ndarray, text: str) -> ndarray:
        """
        Center subtitles and adjust width automatically.
        
        :param frame: (numpy.ndarray) The video frame that text will be placed on.
        :param text: (str) The subtitles to be placed on the text.
        :return numpy.ndarray: The final frame
        """
        frame_height, frame_width = frame.shape[:2]

        # Calculate text size dynamically
        text_size = cv2.getTextSize(text, MergerConsts.FONT, MergerConsts.FONT_SCALE, MergerConsts.FONT_THICKNESS)[0]
        centered_text_x = (frame_width - text_size[0]) // 2
        text_y = frame_height - MergerConsts.BG_BOTTOM_OFFSET  # Position near bottom
        
        # Add background box to improve visibility
        cv2.rectangle(frame, (centered_text_x - MergerConsts.TEXT_HORIZONTAL_OFFSET,
                              text_y - MergerConsts.TEXT_BOTTOM_OFFSET), 
                    (centered_text_x + text_size[0] + 10, text_y + 10), 
                    MergerConsts.TEXT_BG_COLOR, -1)

        # Overlay the text in white
        cv2.putText(frame,
                    text,
                    (centered_text_x, text_y),
                    MergerConsts.FONT,
                    MergerConsts.FONT_SCALE,
                    MergerConsts.FONT_COLOR,
                    MergerConsts.FONT_THICKNESS)

        return frame
