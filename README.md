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
│-- Alerts/              # Handles sending alerts (Telegram)
│-- Capture/             # Webcam photo & video capture
│-- Logs/                # Intrusion logs storage
│-- config.py            # Stores bot token & chat ID
│-- main.py              # Main program entry
│-- requirements.txt     # Dependencies
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
