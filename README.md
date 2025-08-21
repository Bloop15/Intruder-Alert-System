# Intruder Alert System 🔒

A Python-based security system that uses the webcam to capture intruder photos and videos when unauthorized access is detected (e.g., on screen unlocks).

---

## Features

- Captures photo and video via webcam  
- Sends image to a Telegram bot  
- Logs timestamps of intrusion events  
- Modular design with separate logging, capture, and alert components  
- Includes face detection for better accuracy  

---

## Requirements

Install dependencies with:
``` bash
pip install -r requirements.txt 
```
---

## Setup

 Add your **Telegram Bot Token** and **Chat ID** inside `config.py`:
 ```bash
   BOT_TOKEN = "your_bot_token_here"
   CHAT_ID = "your_chat_id_here"
```
---

## Project Structure
```bash
Intruder-Alert/
|-- Alerts/              # Sends alerts via Telegram
|-- Capture/             # Captures photos & videos via webcam
|-- Logs/                # Stores intrusion logs
|-- Dataset/             # Face recognition dataset
|-- config.py            # Bot token, chat ID, paths
|-- main.py              # Main program
|-- trainer.py           # Model training
|-- cleanup.py           # Remove old files
|--cleanup_dataset.py    # Dataset cleanup
|-- requirements.txt     # Dependencies
```
---

## Usage

Run the program:
```bash
   python main.py
```
When an intruder is detected:
- A photo/video is captured  
- Image/video is sent to your Telegram bot  
- Intrusion event is logged with timestamp  

---
