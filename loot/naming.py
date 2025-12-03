# loot/naming.py

"""
Item naming logic.

Builds item display names from base item, rarity, and affixes.
"""

from .models import RolledItem, Rarity

AFFIX_NAME_MAP = {
    "FROST_DAMAGE": "Frost",
    "ARMOR_PEN": "Piercing",
    "STR_BOOST": "Mighty",
    "LIFESTEAL": "Vampiric",
    "CRIT_CHANCE": "Keen",
    "FIRE_DAMAGE": "Flaming",
    "LIGHTNING_DAMAGE": "Shocking",
    "HEALTH_BOOST": "Sturdy",
    "SPEED_BOOST": "Swift",
}

RARITY_SUFFIX_MAP = {
    Rarity.UNCOMMON: "",
    Rarity.RARE: "",
    Rarity.VERY_RARE: "of the Mountain",
    Rarity.LEGENDARY: "of the Lion",
    Rarity.ARTIFACT: "of Eternal Fury",
}

def build_item_name(rolled: RolledItem) -> str:
    """Construct a long, absurd, rarity-scaled item name."""
    # map affix ids -> prefix words, ignore ones we don't know
    prefixes = [AFFIX_NAME_MAP[a] for a in rolled.affixes if a in AFFIX_NAME_MAP]

    # maybe cut or limit based on rarity if you want
    suffix = RARITY_SUFFIX_MAP.get(rolled.rarity, "")

    parts = []
    if prefixes:
        parts.append(" ".join(prefixes))
    parts.append(rolled.base.name)
    if suffix:
        parts.append(suffix)

    return " ".join(parts)
