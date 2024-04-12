#!/usr/bin/python3

# Import CSV into Anki
# from https://superuser.com/a/1663910/951608
# Prerequisites:
# pip3 install genanki

DECK_NAME = '20240318 Kinai'
FILE_NAME = '{}.anki2'.format(DECK_NAME)
# Change this to the path of your CSV file
INPUT_CSV_NAME = '20240318-kinai.csv'
# Change this to your desired deck name
OUTPUT_APKG_NAME = '{}.apkg'.format(DECK_NAME)
# Character which separates the question from the answer within a row
DELIMITER = '\t'

import csv
import genanki
import random

# Define the model for Anki cards
model_id = random.randrange(1 << 30, 1 << 31)  # Change this to your desired model ID
model_name = 'HSK'
# model_fields = [
#     {'name': 'Question'},
#     {'name': 'Answer'}
# ]
model_fields = [
    {'name': 'Hanzi'},
    {'name': 'Pinyin'}
]
model_templates = [
    {
        'name': 'Card 1',
        'qfmt': '{{Hanzi}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Pinyin}}',
    },
]
style = """
.card {
 font-family: "Sans Forgetica", arial, serif;
 font-size: 80px;
 text-align: center;
 color: black;
 background-color: white;
}
.hanzi {
 font-size: 200px;
 font-family: arial, serif;
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
def create_notes(csv_file):
    notes = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=DELIMITER)
        for row in csv_reader:
            question = row[0]
            answer = row[1]
            note = genanki.Note(
                model=anki_model,
                fields=[question, answer]
            )
            notes.append(note)
    return notes

# Define a function to create Anki deck
def create_deck(csv_file, deck_name):
    deck_id = hash(deck_name)
    anki_deck = genanki.Deck(deck_id, deck_name)
    notes = create_notes(csv_file)
    for note in notes:
        anki_deck.add_note(note)
    print("Created deck with {} flashcards".format(len(anki_deck.notes)))
    return anki_deck

# Define the main function
def main():
    csv_file = INPUT_CSV_NAME
    deck_name = DECK_NAME
    deck = create_deck(csv_file, deck_name)
    anki_package = genanki.Package(deck)
    anki_package.write_to_file(OUTPUT_APKG_NAME)

if __name__ == '__main__':
    main()

