import logging
import numpy as np
import cv2  # OpenCV for image display
from src.transmitting_client.rtp_handler import RTPHandler
from src.server.transmitting_client_handler.rtp_parser import RTPPacketDecoder

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)


def main():
    try:
        # Initialize the RTPHandler with payload type 96 and your camera's device index
        rtp_handler = RTPHandler(payload_type=96, video_capture_source=0)

        logging.info("Starting video test...")

        while True:
            # Capture a frame using the camera
            ret, frame = rtp_handler.get_frame()  # Assuming `get_frame` in `VideoCapture` is implemented
            if not ret:
                logging.warning("Failed to capture frame.")
                break

            # Create an RTP packet with the captured frame
            packet = rtp_handler.create_packet(marker=1)

            # Decode the RTP packet using RTPPacketDecoder
            rtp_decoder = RTPPacketDecoder(packet)
            payload = rtp_decoder.get_payload()

            # Convert the payload back to a NumPy array (assuming it was encoded as raw image data)
            try:
                decoded_frame = np.frombuffer(payload, dtype=np.uint8).reshape((480, 640, 3))  # Adjust dimensions
            except ValueError as e:
                logging.error("Error decoding payload into frame: %s", e)
                break

            # Show the decoded frame
            cv2.imshow("Decoded Frame", decoded_frame)

            # Break if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info("Video test stopped by user.")
                break

    except Exception as e:
        logging.error("An error occurred: %s", e)

    finally:
        # Ensure all OpenCV windows are closed properly
        logging.info("Closing video test...")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
