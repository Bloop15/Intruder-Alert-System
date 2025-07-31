import cv2
import os
from datetime import datetime
from Alerts.telegram_alert import send_telegram_image, send_telegram_video
from config import BOT_TOKEN, CHAT_ID
from Logs.log_handler import log_intrusion



def capture_intruder():

    capture_dir= os.path.join(os.getcwd(), "Capture", "Webcam_Capture")
    os.makedirs(capture_dir, exist_ok= True)
    image_dir= os.path.join(capture_dir, "Images")
    os.makedirs(image_dir, exist_ok= True)
    video_dir= os.path.join(capture_dir, "Videos")
    os.makedirs(video_dir, exist_ok= True)

    timestamp= datetime.now().strftime("%Y-%m-%d_%H-%M_%S")
    image_path=os.path.join(image_dir, f"intruder_{timestamp}.jpg")

    cap= cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcam")
        return
    
    ret, frame= cap.read()

    if ret:
        cv2.imwrite(image_path, frame)
        print(f"Image saved to: {image_path}")

        try:
            status= send_telegram_image(BOT_TOKEN, CHAT_ID, image_path)
            print(status)
            log_intrusion(os.path.basename(image_path), status)
        
        except Exception as e:
            log_intrusion(os.path.basename(image_path), f"Image send Failed: {str(e)}")
   
    else:
        print(f"Failed to capture image")
        log_intrusion("No Image", "Failed to Capture")
        cap.release()
        return

    video_name= f"intruder_{timestamp}.mp4"
    video_path= os.path.join(video_dir, video_name)

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

    cap.release()
    out.release()

    print(f"Video saved: {video_path}")
    try:
        status= send_telegram_video(BOT_TOKEN, CHAT_ID, video_path)
        print(status)
        log_intrusion(video_name, status)
    
    except Exception as e:
        log_intrusion(video_name, f"Video Send Failed: {str(e)}")


if __name__ == "__main__":
    capture_intruder()