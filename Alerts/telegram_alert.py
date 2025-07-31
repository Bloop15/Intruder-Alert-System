import requests

def send_telegram_image(bot_token, chat_id, image_path):
    url=  f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    try:
        with open(image_path, 'rb') as image_file:
            response= requests.post(
                url,
                data={'chat_id': chat_id},
                files={'photo': image_file}
            )

        if response.status_code == 200:
            return "Image sent successfully!"

        else:
            return f"Failed to send image: {response.status_code}, {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Error sending image: {e}"


def send_telegram_video(bot_token, chat_id, video_path):
    url= f"https://api.telegram.org/bot{bot_token}/sendVideo"

    try:
        with open(video_path, "rb") as video:
            response= requests.post(
                url,
                data={'chat_id': chat_id},
                files={'video': video}
            )
        
        if response.status_code ==200:
            return "Video sent successfully"
        else:
            return f"Failed to send video: {response.status_code}, {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Error sending video: {e}"