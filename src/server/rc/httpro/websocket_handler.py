"""
    AUTHOR: Ophir Nevo Michrowski
    DESCRIPTION: Handling websocket connections and messages.
"""
# Imports #
import hashlib
import base64
import socket as sock
from socket import socket

import src.server.rc.httpro as httpro
import src.server.rc.httpro.constants as consts
from src.server.rc.httpro import http_parser

class WebsocketHandler:
    def __init__(self) -> None:
        """
        Inits WebscoketHandler Objects
        :return: None
        """
        self.websocket_clients: set[socket] = set()
        self._WEBSOCKET_GUID = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    
    def __send_client(self, client_sock: socket, client_msg: bytes) -> None:
        """
        Sends a message via the client socket.
        :param client_sock: the client socket
        :param client_msg: the msg to send to the client
        :return: None
        """
        try:
            client_sock.send(client_msg)
        except Exception as e:
            consts.HTTP_LOGGER.error("Could not send websocket message")

    def __handle_websocket(self, client_socket: socket, ws_handle) -> None:
        """
        Handle websocket communication
        :param ws_handle: The function that will give the websocket broadcast message
        :param client_socket: the client socket
        :return: None
        """
        while True:
            self.__send_client(client_socket, ws_handle())

    def upgrade_to_websocket(self, request: http_parser.HttpParser, client_socket: sock.socket, ws_handle) -> None:
        """
        This will perform the websocket handshake.
        :param request: The upgrade request
        :param client_socket: socket requesting upgrade
        :param ws_handle: The function that will give the websocket broadcast message
        :return: None
        """
        sec_websocket_key = request.HEADERS.get(b'Sec-WebSocket-Key')
        if not sec_websocket_key:
            consts.HTTP_LOGGER.info("WebSocket key missing! Cannot upgrade connection.")
            return

        # Compute Sec-WebSocket-Accept response
        accept_key = base64.b64encode(
            hashlib.sha1(sec_websocket_key + self._WEBSOCKET_GUID).digest()
        ).decode()

        # Create WebSocket handshake response using HttpMsg
        handshake_response = httpro.http_message.HttpMsg(
            error_code=101,
            upgrade="websocket",
            connection="Upgrade",
            sec_webSocket_accept=accept_key
        )

        # Send the formatted handshake response
        self.__send_client(client_socket, handshake_response.build_message_bytes())
        consts.HTTP_LOGGER.info("WebSocket Handshake Completed! Connection upgraded.")

        # Store WebSocket client and start processing WebSocket frames
        self.websocket_clients.add(client_socket)
        self.__handle_websocket(client_socket, ws_handle)
