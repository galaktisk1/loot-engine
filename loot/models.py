# loot/models.py

"""
Data structures for the loot engine.

Contains:
- D&D-style rarity definitions
- Broad item categories
- Equipment slots
- BaseItem: static item templates
- RolledItem: final generated loot drops
"""

# Some parts of the file was created with the help of ChatGPT, then reviewed and modified by me.
# I reviewed the code for accuracy and learning the purposes of the modules used within.

from dataclasses import dataclass
# dataclass is used for simple data structures
from enum import Enum, auto
# enum is used for defining enumerated types
# when 'auto()' is used, it automatically assigns values to enum members
from typing import List, Optional, Set, Dict
# typing is used for type hinting complex data structures



class Rarity(Enum):
    """D&D-style item rarities."""
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    VERY_RARE = auto()
    LEGENDARY = auto()
    ARTIFACT = auto()

class ItemType(Enum):
    """Broad categories of items."""
    WEAPON = auto()
    ARMOR = auto()
    ARTIFACT = auto()
    CONSUMABLE = auto()
    OTHER = auto()

class EquipmentSlot(Enum):
    """Possible equipment slots for items."""
    MAIN_HAND = auto()
    OFF_HAND = auto()
    HEAD = auto()
    CHEST = auto()
    LEGS = auto()
    HANDS = auto()
    FEET = auto()
    RING = auto()
    NECK = auto()
    NONE = auto()  # For items that are not equippable like potions or scrolls



@dataclass
class BaseItem:
    """
    A template for an item type in the database.
    
    Examples: 'Longsword', 'Chain Mail', 'Potion of Healing'
    """
    id: str # Unique identifier, e.g., 'longsword_001'
    name: str # e.g., 'Longsword'
    item_type: ItemType # Broad category of the item
    slot: EquipmentSlot # Equipment slot the item occupies
    min_level: int # Minimum character level to use the item
    max_level: int # Maximum character level to use the item
    allowed_classes: Optional[Set[str]] = None  # e.g., {'Fighter', 'Paladin'}
    tags: Set[str] = None  # e.g., {'melee', 'slashing'}
    

@dataclass
class RolledItem:
    """
    A specific drop result
    What the generator will output
    """
    base: BaseItem # Reference to the BaseItem template
    rarity: Rarity # Rarity of the rolled item
    level: int # Level of the item when rolled
    stats: Dict[str, float] # e.g., {'damage': 12.5, 'armor_class': 15}
    affixes: List[str]  # e.g., ['of Strength', 'of the Bear'], simple strings for now
    source: Optional[str] = None  # e.g., 'Goblin_Boss', 'ancient_chest', etc.