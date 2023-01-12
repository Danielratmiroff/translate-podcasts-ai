# LOVO API Implementation
# Onhold for now since it's not free
import json
import requests


def validate_speech_length(text):
    return len(text) <= 500


def lovo_tss(self, key, text):

    if validate_speech_length(text) != True:
        raise ValueError(
            f"Text is too long for text-to-speech API. Max length is 500 characters. Current length is {count_characters(self.translated_text)}.")

    url = 'https://api.lovo.ai/v1/conversion'
    data = json.dumps({
        "text": self.translated_text,
        "speaker_id": "Alonso Mairal",
        "emphasis": '[0, 5]',
        "speed": 1,
        "pause": 0,
        "encoding": "mp3"
    })
    headers = {
        'apiKey': key,
        'Content-Type': 'application/json; charset=utf-8'
    }

    print("Calling text-to-speech API...")

    try:
        res = requests.post(url, headers=headers, data=data)
        if res.status_code != 200:
            raise ValueError(
                f'Error calling text-to-speech API: {res.text}, {res.status_code}, {res.reason}')

    except ValueError as e:
        raise ValueError(f'Error calling text-to-speech API: {e}')

    print("Writing audio content to file...")

    with open(self.output_file, 'wb') as f:
        f.write(res.content)

    print("\n" + "Done!" + "\n")
    print(f'Audio content written to file "{self.output_file}"')
