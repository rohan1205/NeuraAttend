import os
import sys
import cv2
import pickle
import torch
import numpy as np
from PIL import Image
from facenet_pytorch import InceptionResnetV1
from scipy.spatial.distance import euclidean

# ---------------- PATH SETUP ----------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.append(BASE_DIR)

from app.dnn_face_detector import DNNFaceDetector
from app.supabase_db import mark_attendance

# ---------------- CONFIG ----------------
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "models", "embeddings.pkl")
RECOGNITION_THRESHOLD = 0.9
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ---------------- LOAD MODELS ----------------
detector = DNNFaceDetector(
    model_path=os.path.join(
        BASE_DIR, "models", "res10_300x300_ssd_iter_140000.caffemodel"
    ),
    config_path=os.path.join(
        BASE_DIR, "models", "deploy.prototxt"
    ),
    confidence_threshold=0.6
)

facenet = InceptionResnetV1(pretrained="vggface2").eval().to(DEVICE)

with open(EMBEDDINGS_PATH, "rb") as f:
    known_embeddings = pickle.load(f)

print("Loaded identities:", list(known_embeddings.keys()))
print("Smart Attendance System (Supabase) running. Press Q to exit.")

# ---------------- HELPER ----------------
def get_embedding(face_img):
    face_img = cv2.resize(face_img, (160, 160))
    face_img = Image.fromarray(face_img).convert("RGB")

    tensor = torch.tensor(np.array(face_img)).permute(2, 0, 1)
    tensor = tensor.unsqueeze(0).float() / 255.0
    tensor = tensor.to(DEVICE)

    with torch.no_grad():
        embedding = facenet(tensor)

    return embedding.cpu().numpy()[0]

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = detector.detect_faces(frame)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        if face.size == 0:
            continue

        emb = get_embedding(face)

        best_match = "Unknown"
        best_distance = float("inf")

        for name, embeddings in known_embeddings.items():
            for known_emb in embeddings:
                dist = euclidean(emb, known_emb)
                if dist < best_distance:
                    best_distance = dist
                    best_match = name

        if best_distance < RECOGNITION_THRESHOLD:
            if mark_attendance(best_match):
                print(f"[ATTENDANCE] {best_match} marked")
        else:
            best_match = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{best_match} ({best_distance:.2f})",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Session ended.")
