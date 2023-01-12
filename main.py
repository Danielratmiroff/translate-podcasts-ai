import argparse
import os
from dotenv import load_dotenv
import modules.voicerss_tts as tts
import modules.transcribe as transcribe
import modules.translate as translate

load_dotenv()

DEEPL_KEY = os.getenv("DEEPL_KEY")
LOVO_KEY = os.getenv("LOVO_KEY")
VOICERSS_KEY = os.getenv("VOICERSS_KEY")


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


def get_file_name(file):
    return file.split('/')[-1].split('.')[0]


class Translate_Podcast():

    def __init__(self):
        # Init argument parser
        parser = argparse.ArgumentParser()
        parser.add_argument("--f",  required=True, help="Path to audio file")

        parser.add_argument(
            "--save",  action=argparse.BooleanOptionalAction, help="Save transcript to file")

        # Parse arguments
        args = parser.parse_args()
        self.speech_file = args.f
        self.save = args.save

    def run_transcribe(self):
        # Model configurations - model sizes: tiny (1GB), base (1GB), small (2GB), medium (5GB), large (10GB)
        model_size = "tiny"
        audio_lang = "English"
        target_lang = "ES"

        # File options
        file_name = get_file_name(self.speech_file)
        output_audio_file = f'{file_name}.mp3'
        save_file = f'{self.file_name}.txt'

        transcript = transcribe.init(
            model_size,
            self.speech_file,
            audio_lang,
            self.save,
            save_file
        )

        if prompt_yes_no("Do you want to continue with translation?") != True:
            return

        translation = translate.init(
            DEEPL_KEY,
            transcript,
            target_lang,
            self.save,
            save_file
        )

        # self.translated_text = '¿Que pasaria si la Tierra dejara de girar durante un segundo? Oh si eso seria desastroso. Desastroso es porque ahora mismo aqui en Nueva York se puede calcular en nuestra latitud. Todos nos estamos moviendo con la tierra a 800 millas por hora. Hacer levadura. Porque la tierra gira. Si detuvieras la tierra y no tuvieras el cinturon de seguridad abrochado a la tierra, te caerias y rodarias a 800 millas por hora, haz levadura. Mataria a todos en la tierra. La gente saldria volando por las ventanas y seria un mal dia en la tierra.'

        tts.voicerss_tts(
            VOICERSS_KEY,
            translation,
            'es-mx',
            output_audio_file
        )


if __name__ == "__main__":
    t = Translate_Podcast()
    t.run_transcribe()
