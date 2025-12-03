# loot/rarity.py

"""
Rarity rules and helpers for the loot engine.

This module defines:
- Drop weights based on level
- Affix count ranges per rarity
- Stat multipliers for scaling
"""

from .models import Rarity
from typing import Dict, Tuple


def rarity_drop_weights(level: int) -> Dict[Rarity, float]:
    """Return drop weight distribution for each rarity based on level."""
    if level < 5:
        return {
            Rarity.COMMON:    70,
            Rarity.UNCOMMON:  25,
            Rarity.RARE:       5,
            Rarity.VERY_RARE:  0,
            Rarity.LEGENDARY:  0,
            Rarity.ARTIFACT:   0,
        }
    elif level < 11:
        return {
            Rarity.COMMON:    40,
            Rarity.UNCOMMON:  35,
            Rarity.RARE:      20,
            Rarity.VERY_RARE:  5,
            Rarity.LEGENDARY:  0,
            Rarity.ARTIFACT:   0,
        }
    else:
        return {
            Rarity.COMMON:    25,
            Rarity.UNCOMMON:  35,
            Rarity.RARE:      25,
            Rarity.VERY_RARE: 10,
            Rarity.LEGENDARY:  5,
            Rarity.ARTIFACT:   0,
        }


def affix_count_for_rarity(rarity: Rarity) -> Tuple[int, int]:
    """Return (min_affixes, max_affixes) for the given rarity."""
    # This match, case syntax was written using the help of AI
    match rarity:
        case Rarity.COMMON:    return (0, 0)
        case Rarity.UNCOMMON:  return (1, 2)
        case Rarity.RARE:      return (2, 4)
        case Rarity.VERY_RARE: return (3, 5)
        case Rarity.LEGENDARY: return (4, 6)
        case Rarity.ARTIFACT:  return (5, 8)


RARITY_STAT_MULTIPLIER: Dict[Rarity, float] = {
    Rarity.COMMON:    1.0,
    Rarity.UNCOMMON:  1.2,
    Rarity.RARE:      1.5,
    Rarity.VERY_RARE: 1.8,
    Rarity.LEGENDARY: 2.2,
    Rarity.ARTIFACT:  3.0,
}
