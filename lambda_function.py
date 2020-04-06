import requests
import json
import os

TOKEN = os.getenv('TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        first_name = data["message"]["chat"]["first_name"]
        chat_id = data["message"]["chat"]["id"]

        response = {"chat_id": chat_id, }

        # Reagiere auf die Eingabe
        # Fallunterscheidung
        if message.startswith('/start'):
            response['text'] = f"Hello {first_name}".encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)

        elif message.startswith('/dog'):
            contents = requests.get('https://random.dog/woof.json').json()
            response['photo'] = contents['url']
            requests.post(f"{BASE_URL}/sendPhoto", response)

        elif message.startswith('/cat'):
            response['photo'] = f'https://cataas.com/cat/says/Hello%20{first_name}'
            requests.post(f"{BASE_URL}/sendPhoto", response)

        # Hier können jetzt noch weitere Kommandos eingetragen werden

        else:
            response['text'] = f"Please /start, {first_name}".encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)

    except Exception as e:
        print(e)

    return {"statusCode": 200}