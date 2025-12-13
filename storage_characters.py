"""
storage_characters.py
"""

import csv
from loot_model import Character

CHARACTERS_FILE = "characters.csv"

def load_characters() -> list[Character]:
    """Load characters from the CSV file and return a list of Character objects."""
    characters = []
    try:
        with open(CHARACTERS_FILE, newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                if len(row) != 3:
                    continue
                name, char_class, level_str = row
                try:
                    level = int(level_str)
                except ValueError:
                    continue
                characters.append(Character(name=name, char_class=char_class, level=level))
    except FileNotFoundError:
        print(f"File {CHARACTERS_FILE} not found.")
    return characters

def save_characters(characters: list[Character]) -> None:
    """Save a list of Character objects to the CSV file."""
    try:
        with open(CHARACTERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["name", "char_class", "level"])  # Write the header row
            for c in characters:
                writer.writerow([c.name, c.char_class, c.level])
    except IOError as e:
        print(f"Error writing to file {CHARACTERS_FILE}: {e}")

def modify_character(characters: list[Character], character: Character) -> None:
    """Modify an existing character in the list based on the character's name."""
    for existing in characters:
        if existing.name == character.name and existing.char_class == character.char_class:
            existing.level = character.level
            return
    characters.append(character)