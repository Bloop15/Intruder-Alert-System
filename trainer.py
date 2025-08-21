import cv2
import os
import numpy as np

BASE_DIR= os.path.dirname(os.path.abspath(__file__))
DATASET_DIR= os.path.join(BASE_DIR, "Dataset")
MODEL_PATH= os.path.join(BASE_DIR, "face_model.yml")

def train_recognizer():

    recognizer= cv2.face.LBPHFaceRecognizer_create()

    images, labels= [], []
    label= 1

    for filename in os.listdir(DATASET_DIR):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        img_path= os.path.join(DATASET_DIR, filename)
        img= cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue
        images.append(img)
        labels.append(label)

    if len(images)==0:
        print("[ERROR] No images found in the Dataset!")
        return False

    recognizer.train(images, np.array(labels))
    recognizer.save(MODEL_PATH)
    print(f"[INFO] Recognizer trained on {len(images)} images and saved to model {MODEL_PATH}")

    return True
                  
