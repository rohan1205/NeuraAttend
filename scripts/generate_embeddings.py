import os
import sys
import pickle
import torch
import numpy as np
from PIL import Image
from facenet_pytorch import InceptionResnetV1

# ---------------- PATH SETUP ----------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.append(BASE_DIR)

print("BASE_DIR:", BASE_DIR)

# ---------------- CONFIG ----------------
FACES_DIR = os.path.join(BASE_DIR, "data", "faces")
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "models", "embeddings.pkl")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", DEVICE)

# ---------------- LOAD FACENET ----------------
model = InceptionResnetV1(pretrained="vggface2").eval().to(DEVICE)

embeddings = {}
total_images = 0

# ---------------- PROCESS DATASET ----------------
for person_name in os.listdir(FACES_DIR):
    person_dir = os.path.join(FACES_DIR, person_name)

    if not os.path.isdir(person_dir):
        continue

    person_embeddings = []

    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)

        img = Image.open(img_path).convert("RGB")
        img = img.resize((160, 160))

        img_tensor = torch.tensor(np.array(img)).permute(2, 0, 1)
        img_tensor = img_tensor.unsqueeze(0).float() / 255.0
        img_tensor = img_tensor.to(DEVICE)

        with torch.no_grad():
            embedding = model(img_tensor)

        person_embeddings.append(embedding.cpu().numpy()[0])
        total_images += 1

    embeddings[person_name] = person_embeddings
    print(f"Processed {len(person_embeddings)} images for {person_name}")

# ---------------- SAVE EMBEDDINGS ----------------
with open(EMBEDDINGS_PATH, "wb") as f:
    pickle.dump(embeddings, f)

print("\nEmbeddings generation completed.")
print("Total images processed:", total_images)
print("Saved to:", EMBEDDINGS_PATH)
