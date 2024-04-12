#!/usr/bin/python3

# Import CSV into Anki
# from https://superuser.com/a/1663910/951608
# Prerequisites:
# pip3 install genanki

DECK_NAME = 'Basic Cantonese Phrases'
CANTONESE_AUDIO_DIRECTORY = 'cantonese-audio/'
ENGLISH_AUDIO_DIRECTORY = 'english-audio/'
# Change this to the path of your CSV file
INPUT_CSV_NAME = 'basic-english-cantonese-phrases.csv'
# Change this to your desired deck name
OUTPUT_APKG_NAME = '{}.apkg'.format(DECK_NAME).replace(" ", "_")
# Character which separates the question from the answer within a row
DELIMITER = '\t'

import csv
import genanki
import os
import random
from collections import namedtuple

CardData = namedtuple('CardData',
    ['english_phrase',
     'english_pronunciation_audio_file_name', # if you use the full path for the media, it won’t load (even if the media exists at the provided absolute path)
     'cantonese_pronunciation_audio_file_name', # if you use the full path for the media, it won’t load (even if the media exists at the provided absolute path)
     'characters',
     'jyutping'])

# Define the model for Anki cards
model_id = random.randrange(1 << 30, 1 << 31)  # Change this to your desired model ID
model_name = 'Cantonese'
# model_fields = [
#     {'name': 'Question'},
#     {'name': 'Answer'}
# ]

# Note: only put the filename (aka basename) and not the full path in the PronunciationAudioFileName field
model_fields = [
    {'name': 'EnglishPhrase'},
    {'name': 'EnglishPronunciationAudioFileName'},
    {'name': 'CantonesePronunciationAudioFileName'},
    {'name': 'Characters'},
    {'name': 'Jyutping'}
]
model_templates = [
    {
        'name': 'Card 1',
        'qfmt': '{{EnglishPronunciationAudioFileName}}{{EnglishPhrase}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{CantonesePronunciationAudioFileName}}{{Characters}}<br/>{{Jyutping}}',
    },
]

# Determine the root AnkiDroid directory specified under Settings > Advanced > AnkiDroid directory
# Copy _SansForgetica-Regular.ttf to the collection.media folder in that directory
# Be sure to rename the .ttf file to include the underscore prefix

style = """
.card {
 font-family: "Sans Forgetica", sansforgetica, arial, serif;
 font-size: 80px;
 text-align: center;
 color: black;
 background-color: white;
}
.hanzi {
 font-size: 200px;
 font-family: arial, serif;
}
@font-face {
  font-family: sansforgetica;
  src: url('_SansForgetica-Regular.ttf');
}
"""

anki_model = genanki.Model(
    model_id,
    model_name,
    fields=model_fields,
    templates=model_templates,
    css=style
)


# Define a function to read CSV file and create Anki notes
def create_card_data_list(csv_file):
    card_data_list = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=DELIMITER)
        for row in csv_reader:
            english_phrase = row[0]
            english_pronunciation_audio_file_name = row[1]
            cantonese_pronunciation_audio_file_name = row[2]
            characters = row[3]
            jyutping = row[4]
            card_data_list.append(CardData(english_phrase=english_phrase, english_pronunciation_audio_file_name=english_pronunciation_audio_file_name,
                cantonese_pronunciation_audio_file_name=cantonese_pronunciation_audio_file_name, characters=characters, jyutping=jyutping))
    return card_data_list


# Format audio files by appending sound: to format string
def generate_cantonese_audio_file_reference(card_data):
    return '[sound:{}]'.format(card_data.cantonese_pronunciation_audio_file_name)

# Format audio files by appending sound: to format string
def generate_english_audio_file_reference(card_data):
    return '[sound:{}]'.format(card_data.english_pronunciation_audio_file_name)

# Given a list of CardData namedtuples, generate each card
def create_notes(card_data_list):
    notes = []
    for card_data in card_data_list:
        note = genanki.Note(
            model=anki_model,
            fields=[card_data.english_phrase, generate_english_audio_file_reference(card_data),
                generate_cantonese_audio_file_reference(card_data), card_data.characters, card_data.jyutping]
        )
        notes.append(note)
    return notes


# Define a function to create Anki deck
def create_deck(csv_file, deck_name):
    deck_id = hash(deck_name)
    anki_deck = genanki.Deck(deck_id, deck_name)
    card_data_list = create_card_data_list(csv_file)
    notes = create_notes(card_data_list)
    for note in notes:
        anki_deck.add_note(note)
    print("Created deck with {} flashcards".format(len(anki_deck.notes)))
    anki_package = genanki.Package(anki_deck)
    anki_package.media_files = gen_audio_files(card_data_list)
    anki_package.write_to_file(OUTPUT_APKG_NAME)
    return anki_deck


# Define a function to include audio files with paths
def gen_audio_files(card_data_list):
  return list(map(lambda card_data: os.path.join(CANTONESE_AUDIO_DIRECTORY, card_data.cantonese_pronunciation_audio_file_name), card_data_list)) + \
    list(map(lambda card_data: os.path.join(ENGLISH_AUDIO_DIRECTORY, card_data.english_pronunciation_audio_file_name), card_data_list))


# Define the main function
def main():
    csv_file = INPUT_CSV_NAME
    deck_name = DECK_NAME
    deck = create_deck(csv_file, deck_name)


if __name__ == '__main__':
    main()

