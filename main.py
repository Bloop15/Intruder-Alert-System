import cv2
import os
import traceback
from datetime import datetime
from Alerts.telegram_alert import send_telegram_image, send_telegram_video
from config import BOT_TOKEN, CHAT_ID
from Logs.log_handler import log_intrusion

FACE_CASCADE__PATH= cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade= cv2.CascadeClassifier(FACE_CASCADE__PATH)

FPS= 20
VIDEO_DURATION_SEC= 5

def print_error(e, context=""):
    print(f"[ERROR] {context}: {e}")
    traceback.print_exc()


def capture_intruder():
    
    BASE_DIR= os.path.dirname(os.path.abspath(__file__))
    capture_dir= os.path.join(BASE_DIR, "Capture", "Webcam_Capture")
    image_dir= os.path.join(capture_dir, "Images")
    video_dir= os.path.join(capture_dir, "Videos")
    
    for folder in [capture_dir, image_dir, video_dir]:
        os.makedirs(folder, exist_ok=True)

    timestamp= datetime.now().strftime("%Y-%m-%d_%H-%M_%S")
    image_path=os.path.join(image_dir, f"intruder_{timestamp}.jpg")
    video_name= f"intruder_{timestamp}.mp4"
    video_path= os.path.join(video_dir, video_name)

    cap= None
    try:
        cap= cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Failed to open webcam!")
    
        ret, frame= cap.read()
        if not ret:
            log_intrusion("No Image", "Failed to capture image!")
            raise RuntimeError("Image capture failed!")
        
        gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces= face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30)
        )

        if len(faces)==0:
            log_intrusion("No Face", "No face detected in the frame")
            print("No face detected in the captured image")
        else:
            print(f"Detected {len(faces)} face(s).")

        for(x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

        cv2.imwrite(image_path, frame)
        print(f"Image saved to: {image_path}")

        try:
            status= send_telegram_image(BOT_TOKEN, CHAT_ID, image_path)
            print(status)
            log_intrusion(os.path.basename(image_path), status)

        except Exception as e:
            log_intrusion(os.path.basename(image_path), f"Image send Failed: {e}")
            print_error(e, "Sending image to Telegram")

        try:
            fourcc= cv2.VideoWriter_fourcc(*"mp4v")
            out= cv2.VideoWriter(video_path, fourcc, FPS,
                         (int(cap.get(3)), int(cap.get(4))))
            
            for _ in range(FPS*VIDEO_DURATION_SEC):
                ret, frame= cap.read()
                if not ret:
                    break

                gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces= face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=5
                )

                for(x,y,w,h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                
                out.write(frame)
            out.release()

            print(f"Video saved: {video_path}")

        except Exception as e:
            log_intrusion(video_name, f"Video capture failed: {e}")
            print_error(e, "Capturing video")


        try:
            status= send_telegram_video(BOT_TOKEN, CHAT_ID, video_path)
            print(status)
            log_intrusion(video_name, status)
    
        except Exception as e:
            log_intrusion(video_name, f"Video Send Failed: {e}")
            print_error(e, "Sending video to Telegram")

    except Exception as e:
        print_error(e, "Critical error in capture_intruder")

    finally:
        if cap is not None:
            cap.release()


if __name__ == "__main__":
    capture_intruder()