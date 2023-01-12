import deepl
import unicodedata

# Description: This module is used to translate text from one language to another.
# It uses the DeepL API to translate text.


def create_file(output_file, text):
    print("Writing translation to file...")

    try:
        with open(f'translations/{output_file}', 'wb') as f:
            f.write(text.content.encode('utf-8'))

    except ValueError as e:
        raise ValueError(f'Error writing audio content to file: {e}')


def remove_accents_from_string(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')


def init(key, text, lang, save, file):
    print("initalizing translation...")
    translator = deepl.Translator(key)

    print("Calling translation API...")
    try:
        result = translator.translate_text(
            text, target_lang=lang)

    except ValueError as e:
        raise ValueError(f'Error translating text: {e}')

    valid_text_format = remove_accents_from_string(result.text)

    print(f'Translation: {valid_text_format}\n')

    if save == True:
        create_file(file, valid_text_format)

    return valid_text_format
