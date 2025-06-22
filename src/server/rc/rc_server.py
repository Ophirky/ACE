"""
    This uses the HTTPro library to create the server
"""
# Imports #
import base64
import struct
import time
from multiprocessing import Queue

import cv2
import numpy as np

import src.server.rc.httpro as httpro
from src.server.rc.httpro import http_message
from src.server.rc.httpro import http_parser


def websocket_process(transcribed_queue: Queue) -> None:
    """
    Runs the web server
    :param transcribed_queue: queue that holds transcribed frames
    :return: None
    """
    app = httpro.app.App()
    last_frame = None

    def create_placeholder_image(width=640, height=480, message="No Stream Available"):
        """
        Creates a simple placeholder image (e.g., a black frame with text).
        """
        # Create a black image
        img = np.zeros((height, width, 3), dtype=np.uint8)

        # Add text to the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_thickness = 2
        text_color = (255, 255, 255)  # White color

        # Get text size to center it
        text_size = cv2.getTextSize(message, font, font_scale, font_thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2

        cv2.putText(img, message, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
        return img

    # TODO: Prettify
    @app.websocket_handle
    def ws_handle():
        nonlocal last_frame
        if not transcribed_queue.empty():
            last_frame = frame_to_send = transcribed_queue.get()
        elif last_frame is None:
            frame_to_send = create_placeholder_image()
        else:
            frame_to_send = last_frame

        _, buffer = cv2.imencode('.jpg', frame_to_send)
        frame_data = base64.b64encode(buffer).decode()

        message_bytes = frame_data.encode("utf-8")  # Convert message to bytes
        length = len(message_bytes)

        # Build WebSocket frame header
        if length <= 125:
            header = struct.pack("B", 0x81) + struct.pack("B", length)
        elif length < 65536:
            header = struct.pack("B", 0x81) + struct.pack("!BH", 126, length)
        else:
            header = struct.pack("B", 0x81) + struct.pack("!BQ", 127, length)

        # Send the formatted WebSocket frame
        time.sleep(0.002)
        return header + message_bytes

    @app.route(b"/")
    def ws(request: http_parser.HttpParser) -> http_message.HttpMsg:
        return httpro.http_message.HttpMsg(error_code=200,
                                           body=httpro.read_file("./rc/index.html"),
                                           content_type=httpro.consts.MIME_TYPES[".html"])

    httpro.http_setup()
    app.run()
