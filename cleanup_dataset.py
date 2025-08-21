import cv2
import os
import shutil

RAW_IMAGES_DIR= "Capture/Webcam_Capture/Images"
DATASET_DIR= "Dataset"

FACE_CASCADE_PATH= cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade= cv2.CascadeClassifier(FACE_CASCADE_PATH)


os.makedirs(DATASET_DIR, exist_ok=True)

def cleanup_images():
    kept=0
    removed=0

    for filename in os.listdir(RAW_IMAGES_DIR):
        file_path= os.path.join(RAW_IMAGES_DIR, filename)

        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        img= cv2.imread(file_path)
        if img is None:
            continue

        gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces= face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(faces)==1:
            shutil.copy(file_path, os.path.join(DATASET_DIR, filename))
            kept+=1

        else:
            removed+=1

    print(f"Cleanup Complete: {kept} images kept, {removed} images discarded")

if __name__=="__main__":
    cleanup_images()