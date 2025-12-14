"""
loot_model.py
Simple data models for the loot generator.
"""

from dataclasses import dataclass
# This dataclasses library was recommended from AI
# rest of the code is my writing

@dataclass
class Character:
    """Represents a player character."""
    name: str
    char_class: str
    level: int


@dataclass
class Item:
    """Represents a generated loot item."""
    base_item: str
    full_name: str
    modifiers: list[str]
    power_text: str
    power_score: int