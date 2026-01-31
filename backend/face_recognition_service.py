# face_recognition_service.py

def recognize_faces(frame_base64: str):
    """
    DEMO MODE:
    Simulates face recognition.
    Later, this will:
    - decode base64
    - detect faces
    - compare embeddings
    """

    print("🧠 Face recognition invoked")
    print("📸 Frame size:", len(frame_base64))

    # TEMP: Always recognize Rohan
    return ["rohan"]
