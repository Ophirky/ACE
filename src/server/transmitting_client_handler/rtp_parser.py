"""
    This file contains the RTPPacketDecoder class, which handles incoming RTP packets and parses them into a usable object.
"""

import logging
# Imports #
import struct


class RTPPacketDecoder:
    """
    Decodes RTP packets into header fields and payload.
    """

    def __init__(self, packet: bytes) -> None:
        """
        Initializes the RTPPacketDecoder instance with the given RTP packet.

        :param packet: (bytes) The raw RTP packet.
        """
        self.packet = packet
        self.version = None
        self.padding = None
        self.extension = None
        self.csrc_count = None
        self.marker = None
        self.payload_type = None
        self.sequence_number = None
        self.timestamp = None
        self.ssrc = None
        self.csrcs = []
        self.extension_data = None
        self.payload = None

        self.decode_packet()

    def decode_packet(self) -> None:
        """
        Decodes the RTP packet, extracting its header and payload.
        """
        try:
            if len(self.packet) < 12:
                raise ValueError("RTP packet too short to contain a valid header.")

            # Parse the fixed header (12 bytes)
            header = struct.unpack('!BBHII', self.packet[:12])
            self.version = (header[0] >> 6) & 0b11
            self.padding = (header[0] >> 5) & 0b1
            self.extension = (header[0] >> 4) & 0b1
            self.csrc_count = header[0] & 0b1111
            self.marker = (header[1] >> 7) & 0b1
            self.payload_type = header[1] & 0b01111111
            self.sequence_number = header[2]
            self.timestamp = header[3]
            self.ssrc = header[4]

            # Calculate header size and extract CSRCs if present
            header_size = 12
            if self.csrc_count > 0:
                csrc_end = header_size + 4 * self.csrc_count
                if len(self.packet) < csrc_end:
                    raise ValueError("RTP packet too short to contain all CSRCs.")
                self.csrcs = struct.unpack(f'!{self.csrc_count}I', self.packet[header_size:csrc_end])
                header_size = csrc_end

            # Handle extension header if present
            if self.extension:
                print("Entered the if")
                if len(self.packet) < header_size + 4:
                    raise ValueError("RTP packet too short to contain the extension header.")
                ext_header = struct.unpack('!HH', self.packet[header_size:header_size + 4])
                ext_length = ext_header[1] * 4  # Length in 32-bit words
                ext_end = header_size + 8 + ext_length
                if len(self.packet) < ext_end:
                    raise ValueError("RTP packet too short to contain extension data.")
                self.extension_data = self.packet[header_size + 8:ext_end]
                header_size = ext_end
                print(ext_header, ext_length, ext_end)

            # Extract payload
            self.payload = self.packet[header_size:]

            logging.info("RTP packet successfully decoded.")

        except struct.error as e:
            logging.exception("Failed to unpack RTP packet: %s", e)
            raise ValueError("Invalid RTP packet structure.") from e
        except Exception as e:
            logging.exception("Error decoding RTP packet: %s", e)
            raise

    def get_header_info(self) -> dict:
        """
        Returns the RTP header fields as a dictionary.

        :return: dict: Header fields with their values.
        """
        return {
            "version": self.version,
            "padding": self.padding,
            "extension": self.extension,
            "csrc_count": self.csrc_count,
            "marker": self.marker,
            "payload_type": self.payload_type,
            "sequence_number": self.sequence_number,
            "timestamp": self.timestamp,
            "ssrc": self.ssrc,
            "csrcs": self.csrcs,
            "extension_data": self.extension_data,
        }

    def get_payload(self) -> bytes:
        """
        Returns the payload from the RTP packet.

        :return: bytes: The raw payload data.
        """
        return self.payload
