import cv2
from app.dnn_face_detector import DNNFaceDetector

detector = DNNFaceDetector(
    model_path="models/res10_300x300_ssd_iter_140000.caffemodel",
    config_path="models/deploy.prototxt",
    confidence_threshold=0.6
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera not accessible")
    exit()

print("DNN Face Detection running. Press Q to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = detector.detect_faces(frame)

    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imshow("DNN Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Exited safely")
