import cv2
import os
from datetime import datetime
from Alerts.telegram_alert import send_telegram_image
from config import BOT_TOKEN, CHAT_ID



def capture_intruder():

    capture_dir= os.path.join(os.getcwd(), "Capture")
    os.makedirs(capture_dir, exist_ok= True)

    timestamp= datetime.now().strftime("%Y-%m-%d_%H-%M_%S")
    image_path=os.path.join(capture_dir, f"intruder_{timestamp}.jpg")

    cap= cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcam")
        return
    
    ret, frame= cap.read()
    cap.release()

    if ret:
        cv2.imwrite(image_path, frame)
        print(f"Image saved to: {image_path}")

        send_telegram_image(BOT_TOKEN, CHAT_ID, image_path)
    else:
        print(f"Failed to capture image")


if __name__ == "__main__":
    capture_intruder()