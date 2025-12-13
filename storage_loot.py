"""
storage_loot.py
Loading base items and saving loot history.
"""

import csv
from pathlib import Path
from loot_model import Character, Item

BASE_ITEMS_FILE = Path(__file__).parent / "base_items.txt"
LOOT_HISTORY_FILE =  Path(__file__).parent / "loot_history.csv"

def load_base_items() -> dict[str, list[str]]:
    """Load base items from a text file and return a dictionary by character class."""
    base_items: dict[str, list[str]] = {}
    try:
        with open(BASE_ITEMS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "|" not in line:
                    continue
                char_class, item_name = line.split("|", 1)
                char_class = char_class.strip()
                item_name = item_name.strip()
                base_items.setdefault(char_class, []).append(item_name)
    except FileNotFoundError:
        print(f"Error: {BASE_ITEMS_FILE} not found.")
    return base_items

def save_loot_history(character: Character, item: Item) -> None:
    """Save a loot entry to the CSV loot history file."""
    try:
        with open(LOOT_HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([character.name,
                character.char_class,
                character.level,
                item.base_item,
                item.full_name,
                ", ".join(item.modifiers),
                item.power,
            ])
    except Exception as e:
        print(f"Error saving loot history: {e}")