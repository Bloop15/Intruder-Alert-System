import cv2
import os
import traceback
from datetime import datetime
from Alerts.telegram_alert import send_telegram_image, send_telegram_video
from config import BOT_TOKEN, CHAT_ID
from Logs.log_handler import log_intrusion



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

    try:
        cap= cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Failed to open webcam!")
    
        ret, frame= cap.read()
        if not ret:
            log_intrusion("No Image", "Failed to capture image!")
            raise RuntimeError("Image capture failed!")

        try:
            cv2.imwrite(image_path, frame)
            print(f"Image saved to: {image_path}")

        except Exception as e:
            log_intrusion("No Image", f"Image save failed: {e}")
            raise

        try:
            status= send_telegram_image(BOT_TOKEN, CHAT_ID, image_path)
            print(status)
            log_intrusion(os.path.basename(image_path), status)
        
        except Exception as e:
            log_intrusion(os.path.basename(image_path), f"Image send Failed: {e}")
            traceback.print_exc()

        try:
            fourcc= cv2.VideoWriter_fourcc(*"mp4v")
            out= cv2.VideoWriter(video_path, fourcc, 20.0,
                         (int(cap.get(3)), int(cap.get(4))))
    
            frame_count= 0
            max_frames= 20*5

            while(frame_count< max_frames):
                ret, frame= cap.read()
                if not ret:
                    break
                out.write(frame)
                frame_count+= 1

            out.release()
            print(f"Video saved: {video_path}")

        except Exception as e:
            log_intrusion(video_name, f"Video capture failed: {e}")
            traceback.print_exc()


        try:
            status= send_telegram_video(BOT_TOKEN, CHAT_ID, video_path)
            print(status)
            log_intrusion(video_name, status)
    
        except Exception as e:
            log_intrusion(video_name, f"Video Send Failed: {e}")
            traceback.print_exc()

        cap.release()

    except Exception as e:
        print(f"Critical error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    capture_intruder()