import base64
import cv2
import numpy as np
from face_recognition_service import recognize_faces
from db_service import mark_present
from datetime import datetime

def process_frame(frame_base64: str):
    # Remove base64 header
    header, encoded = frame_base64.split(",", 1)

    # Decode image
    image_bytes = base64.b64decode(encoded)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None:
        return []

    # Recognize faces
    names = recognize_faces(frame)

    # Mark attendance in DB
    marked = []
    for name in names:
        mark_present(name)
        marked.append(name)

    return marked
