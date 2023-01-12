import urllib
import requests


def create_file(output_file, res):
    print("Writing audio content to file...")

    print(res.content)

    try:
        with open(f'audio/{output_file}', 'wb') as f:
            f.write(res.content)

        print(f'Done!\n')
        print(f'Audio content written to file "{output_file}"')

    except ValueError as e:
        raise ValueError(f'Error writing audio content to file: {e}')


def voicerss_tts(key, text, lang, output_file):
    print(f'Generating audio file...\n')

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    print("Calling text-to-speech API...")

    url = 'https://api.voicerss.org'
    data = urllib.parse.urlencode({
        "key": key,
        "src": text,
        "hl": lang,
        "c": "MP3",
        "f": "48khz_16bit_stereo",
        "ssml": "false",
        "b64": "false"
    })

    try:
        res = requests.post(url, headers=headers, params=data)

        if res.status_code != 200:
            raise ValueError(
                f'Error calling text-to-speech API: {res.text}, {res.status_code}, {res.reason}')

    except ValueError as e:
        raise ValueError(f'Error calling text-to-speech API: {e}')

    create_file(output_file, res)
