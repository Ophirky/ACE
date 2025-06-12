"""
    This uses the HTTPro library to create the server
"""
# Imports #
import base64
import struct
from multiprocessing import Queue

import cv2

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

    @app.websocket_handle
    def ws_handle():

        if not transcribed_queue.empty():
            print("innnnnn")
            _, buffer = cv2.imencode('.jpg', transcribed_queue.get())
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
            return header + message_bytes

    @app.route(b"/")
    def ws(request: http_parser.HttpParser) -> http_message.HttpMsg:
        return httpro.http_message.HttpMsg(error_code=200,
                                           body=httpro.read_file("./rc/index.html"),
                                           content_type=httpro.consts.MIME_TYPES[".html"])

    httpro.http_setup()
    app.run()
