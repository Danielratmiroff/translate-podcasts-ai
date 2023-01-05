import whisper
import deepl
import os
from dotenv import load_dotenv

load_dotenv()

DEEPL_KEY = os.getenv("DEEPL_KEY")

# model sizes: tiny (1GB), base (1GB), small (2GB), medium (5GB), large (10GB)
model_size = "tiny"
language = "English"
speech_file = "audio/speech.wav"


def main():
    model = whisper.load_model(model_size)
    result = model.transcribe(speech_file, fp16=False, language=language)

    print(result["text"])


def translate():
    translator = deepl.Translator(DEEPL_KEY)
    result = translator.translate_text("Hello World", target_lang="ES")
    translated_text = result.text
    print(translated_text)


if __name__ == "__main__":
    translate()
    # main()
