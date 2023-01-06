import unicodedata
import whisper
import argparse
import deepl
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

DEEPL_KEY = os.getenv("DEEPL_KEY")
LOVO_KEY = os.getenv("LOVO_KEY")


def remove_accents_from_string(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')

# TODO:
# need to find speec to text for more than 500 chars


def prompt_yes_no(question):
    while True:
        try:
            reply = str(input(question + ' (y/n): ')).lower().strip()
            if reply[0] == 'y':
                return True
            if reply[0] == 'n':
                return False
        except:
            pass


def count_characters(text):
    return len(text)


def validate_speech_length(text):
    return len(text) <= 500


class Translate_Podcast:
    translated_text = ''
    transcript = ''

    def __init__(self):
        # Init argument parser
        parser = argparse.ArgumentParser()
        parser.add_argument("--file",  required=True,
                            help="Path to audio file")

        # Parse arguments
        args = parser.parse_args()

        # model sizes: tiny (1GB), base (1GB), small (2GB), medium (5GB), large (10GB)
        self.model_size = "tiny"
        self.audio_lang = "English"
        self.speech_file = args.file
        self.output_file = "audio.mp3"
        self.target_lang = "ES"

    def transcribe(self):
        print("Loading whisper model...")
        model = whisper.load_model(self.model_size)

        print("Transcribing speech file...")
        result = model.transcribe(
            self.speech_file, fp16=False, language=self.audio_lang)
        self.transcript = result["text"]

        print("Transcription:")
        print(self.transcript)
        print(f'\nNumber of characters: {count_characters(self.transcript)}\n')

    def translate(self):
        print("Translating text...")
        translator = deepl.Translator(DEEPL_KEY)

        # TODO: need to catch for errors here
        result = translator.translate_text(
            self.transcript, target_lang=self.target_lang)

        valid_text = remove_accents_from_string(result.text)
        self.translated_text = valid_text

        print(f'Translation: {self.translated_text}\n')

    def text_to_speech(self):
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
            'apiKey': LOVO_KEY,
            'Content-Type': 'application/json; charset=utf-8'
        }
        print("Calling text-to-speech API...")

        try:
            res = requests.post(url, headers=headers, data=data)
            if res.status_code != 200:
                raise Exception(
                    f'Error calling text-to-speech API: {res.text}, {res.status_code}, {res.reason}')
        except Exception as e:
            raise Exception(f'Error calling text-to-speech API: {e}')

        print("Writing audio content to file...")
        with open(self.output_file, 'wb') as f:
            f.write(res.content)

        print("\n" + "Done!" + "\n")
        print(f'Audio content written to file "{self.output_file}"')

    def run_transcribe(self):
        self.transcribe()

        if prompt_yes_no("Do you want to continue with translation?") != True:
            return

        self.translate()

        if validate_speech_length(self.translated_text) != True:
            raise (
                f"Text is too long for text-to-speech API. Max length is 500 characters. Current length is {count_characters(self.translated_text)}.")

        print("Initialising text to speech...")
        self.text_to_speech()


if __name__ == "__main__":
    t = Translate_Podcast()
    t.run_transcribe()
