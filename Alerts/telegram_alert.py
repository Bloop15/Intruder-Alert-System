import requests

def send_telegram_image(bot_token, chat_id, image_path):
    url=  f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    with open(image_path, 'rb') as image_file:
        response= requests.post(
            url,
            data={'chat_id': chat_id},
            files={'photo': image_file}
        )

    if response.status_code == 200:
        print("Image sent successfully!")

    else:
        print("Failed to send image: {response.status_code}, {resposne.text}")
