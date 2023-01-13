import whisper

# Description
# This module is used to transcribe speech to text.
# It uses the Whisper API to transcribe speech.
# Saves the transcript to a file if the user wants to.


def count_characters(text):
    return len(text)


def create_file(output_file, res):
    print("Writing trancription to file...")

    try:
        with open(f'transcripts/{output_file}', 'wb') as f:
            f.write(res.encode('utf-8'))

    except ValueError as e:
        raise ValueError(f'Error writing trancription to file: {e}')


def init(model_size, audio_file, lang, save, transcript_file):

    print("Loading whisper model...")
    model = whisper.load_model(model_size)

    print("Transcribing speech file...")
    try:
        result = model.transcribe(
            audio_file,
            fp16=False,
            language=lang)

        transcript = result["text"]

    except ValueError as e:
        raise ValueError(f'Error transcribing speech: {e}')

    print("Transcription:")
    print(transcript)
    print(f'\nNumber of characters: {count_characters(transcript)}\n')

    if save == True:
        create_file(transcript_file, transcript)

    return transcript
