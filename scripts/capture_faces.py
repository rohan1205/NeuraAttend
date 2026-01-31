import cv2
import os

# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACES_DIR = os.path.join(BASE_DIR, "data", "faces")

os.makedirs(FACES_DIR, exist_ok=True)

# ================= INPUT =================
person_name = input("Enter student name: ").strip().lower()

SAVE_DIR = os.path.join(FACES_DIR, person_name)
os.makedirs(SAVE_DIR, exist_ok=True)

print(f"[INFO] Saving face images to: {SAVE_DIR}")

# ================= CAMERA =================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not accessible")
    exit()

count = 0
MAX_IMAGES = 30

print("[INFO] Camera started. Press 'q' to quit early.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture Faces", frame)

    if count < MAX_IMAGES:
        img_path = os.path.join(SAVE_DIR, f"{count}.jpg")
        cv2.imwrite(img_path, frame)
        count += 1
        print(f"[INFO] Captured image {count}/{MAX_IMAGES}")

    if count >= MAX_IMAGES:
        print("[INFO] Face capture completed")
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("[INFO] Capture stopped manually")
        break

cap.release()
cv2.destroyAllWindows()
