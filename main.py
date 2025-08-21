import cv2
import os
import json
import traceback
from datetime import datetime
from Alerts.telegram_alert import send_telegram_image, send_telegram_video
from config import BOT_TOKEN, CHAT_ID
from Logs.log_handler import log_intrusion
from trainer import train_recognizer
from cleanup import cleanup_folder

FACE_CASCADE__PATH= cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade= cv2.CascadeClassifier(FACE_CASCADE__PATH)

FPS= 20
VIDEO_DURATION_SEC= 5

BASE_DIR= os.path.dirname(os.path.abspath(__file__))
MODEL_PATH= os.path.join(BASE_DIR, "face_model.yml")

capture_dir= os.path.join(BASE_DIR, "Capture", "Webcam_Capture")
image_dir= os.path.join(capture_dir, "Images")
video_dir= os.path.join(capture_dir, "Videos")
dataset_dir= os.path.join(BASE_DIR, "Dataset")
    
for folder in [capture_dir, image_dir, video_dir]:
    os.makedirs(folder, exist_ok=True)

STATE_PATH= os.path.join(BASE_DIR, "retrain_state.json")
RETRAIN_THRESHOLD= 10

def load_state():
    try:
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    except:
        return {"new_images_since_train": 0}


def save_state(state):
    tmp= STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_PATH)


state= load_state()

recognizer= cv2.face.LBPHFaceRecognizer_create()
if os.path.exists(MODEL_PATH):
    recognizer.read(MODEL_PATH)
    print(f"[INFO] LBPH model loaded from {MODEL_PATH}")

else:
    print("[WARNING] No trained model found! Run train_recognizer.py first.")


def print_error(e, context=""):
    print(f"[ERROR] {context}: {e}")
    traceback.print_exc()


def capture_intruder():

    global state, recognizer

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

        timestamp= datetime.now().strftime("%Y-%m-%d_%H-%M_%S")
        image_path=os.path.join(image_dir, f"intruder_{timestamp}.jpg")
        video_name= f"intruder_{timestamp}.mp4"
        video_path= os.path.join(video_dir, video_name)

        authorized= False

        if len(faces)==0:
            log_intrusion("No Face", "No face detected in the frame")
            print("No face detected in the captured image")

        else:
            print(f"Detected {len(faces)} face(s).")
            for(x,y,w,h) in faces:
                roi_gray= gray[y:y+h, x:x+w]

                try:
                    label, confidence= recognizer.predict(roi_gray)

                    if confidence<70:
                        text= f"Authorized (ID {label}, Conf {round(confidence,2)})"
                        color= (0,255,0)
                        authorized= True

                        dataset_path= os.path.join(dataset_dir, f"user1_{timestamp}.jpg")
                        cv2.imwrite(dataset_path, roi_gray)
                        cleanup_folder(dataset_dir, max_files=400)

                        state["new_images_since_train"]= state.get("new_images_since_train", 0) + 1
                        print(f"[INFO] New authorised image saved. Count since last train= {state['new_images_since_train']}")

                        if state["new_images_since_train"] >= RETRAIN_THRESHOLD:
                            print("[INFO] Retraining recognizer....")
                            if train_recognizer():
                                recognizer.read(MODEL_PATH)
                                print("[INFO] Model reloaded after training")
                                state["new_images_since_train"]= 0

                            else:
                                print("[WARNING] Retraining failed or no images; Keeping the current model")

                        save_state(state)

                    else:
                        text= f"Intruder (Conf {round(confidence,2)})"
                        color= (0,0,255)
            
                    cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
                    cv2.putText(frame, text, (x,y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                except Exception as e:
                    print_error(e, "Face Recongnition Failed")
        
        cv2.imwrite(image_path, frame)
        print(f"Image saved to: {image_path}")
        cleanup_folder(image_dir, max_files=200)

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
                    roi_gray= gray[y:y+h, x:x+w]

                    try:
                        label, confidence= recognizer.predict(roi_gray)
                        if confidence<70:
                            text= "Authorized"
                            color= (0,255,0)
                        
                        else:
                            text= f"Intruder"
                            color= (0,0,255)

                        cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
                        cv2.putText(frame, text, (x,y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    
                    except:
                        pass

                
                out.write(frame)
            out.release()
            print(f"Video saved: {video_path}")
            cleanup_folder(video_dir, max_files=200)

        except Exception as e:
            log_intrusion(video_name, f"Video capture failed: {e}")
            print_error(e, "Capturing video")


        if authorized:
            print("[INFO] Authorized person detected. Not sending alert")
        else:
            try:
                status= send_telegram_image(BOT_TOKEN, CHAT_ID, image_path)
                print(status)
                log_intrusion(os.path.basename(image_path), status)

            except Exception as e:
                log_intrusion(os.path.basename(image_path), f"Image send Failed: {e}")
                print_error(e, "Sending image to Telegram")

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