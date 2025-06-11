from cv2 import FONT_HERSHEY_SIMPLEX

class TranscriptorConsts:
    MODEL_PATH = r"./transcriptor/model"
    SAMPLE_RATE_HZ = 16000

class MergerConsts:
    FONT = FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 1
    FONT_THICKNESS = 2
    FONT_COLOR = (255, 255, 255)
    
    TEXT_BG_COLOR = (0, 0, 0)
    BG_BOTTOM_OFFSET = 50
    TEXT_BOTTOM_OFFSET = 30
    TEXT_HORIZONTAL_OFFSET = 10
