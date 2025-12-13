"""
loot_service.py
Loot generation logic: modifiers, chances, and name building.
"""

import random

from loot_model import Character, Item
from storage_loot import load_base_items

class LootService:
    """Handles loot generation,
    including applying modifiers, 
    how many, based on level,
    how they affect the item
    """
    def __init__(self):
        self._base_items_by_class = load_base_items()
        
        # this will be a huge list of item modifiers
        # it will be a long list of dictionaries
        self._modifiers = [
        # Power texts are modeled after D&D5e. Prefix/suffix controls name position.
        # Level 1
        {
            "name": "Flaming",
            "min_level": 1,
            "chance": 0.3,
            "power_text": "+1d4 fire damage",
            "position": "prefix",
        },
        {
            "name": "of the Flame",
            "min_level": 1,
            "chance": 0.2,
            "power_text": "grants resistance to fire damage",
            "position": "suffix",
        },
        {
            "name": "Sharp",
            "min_level": 1,
            "chance": 0.25,
            "power_text": "+1 to attack rolls",
            "position": "prefix",
        },
        {
            "name": "Sturdy",
            "min_level": 1,
            "chance": 0.2,
            "power_text": "while wielded, +1 AC",
            "position": "prefix",
        },

        # Level 2
        {
            "name": "Freezing",
            "min_level": 2,
            "chance": 0.2,
            "power_text": "+1d4 cold damage",
            "position": "prefix",
        },
        {
            "name": "Silent",
            "min_level": 2,
            "chance": 0.15,
            "power_text": "reduces noise, granting advantage on Stealth checks while wielded",
            "position": "prefix",
        },
        {
            "name": "of Focus",
            "min_level": 2,
            "chance": 0.2,
            "power_text": "+1 to concentration checks",
            "position": "suffix",
        },
        {
            "name": "Tempest-Touched",
            "min_level": 2,
            "chance": 0.15,
            "power_text": "weapon crackles faintly: +1 lightning damage",
            "position": "prefix",
        },
        {
            "name": "of the Owl",
            "min_level": 2,
            "chance": 0.18,
            "power_text": "+1 to Wisdom (Perception) checks",
            "position": "suffix",
        },

        # Level 3
        {
            "name": "Poisoned",
            "min_level": 3,
            "chance": 0.25,
            "power_text": "on hit: target makes a DC 12 Con save or take 1d6 poison damage",
            "position": "prefix",
        },
        {
            "name": "of Venom",
            "min_level": 3,
            "chance": 0.15,
            "power_text": "adds 1d4 poison damage on hit",
            "position": "suffix",
        },
        {
            "name": "Draining",
            "min_level": 3,
            "chance": 0.2,
            "power_text": "on hit: regain 1 hit point",
            "position": "prefix",
        },
        {
            "name": "of Weakening",
            "min_level": 3,
            "chance": 0.15,
            "power_text": "on hit: target makes DC 12 Str save or gets -1 on attack rolls next turn",
            "position": "suffix",
        },

        # Level 4
        {
            "name": "of Jolting",
            "min_level": 4,
            "chance": 0.2,
            "power_text": "on hit: target must make a DC 12 Con save or be stunned until the end of its next turn",
            "position": "suffix",
        },
        {
            "name": "of Windstep",
            "min_level": 4,
            "chance": 0.18,
            "power_text": "your jump distance is doubled",
            "position": "suffix",
        },
        {
            "name": "Serrated",
            "min_level": 4,
            "chance": 0.2,
            "power_text": "critical hits deal +1d4 bleeding damage",
            "position": "prefix",
        },

        # Level 5
        {
            "name": "of the Unseen",
            "min_level": 5,
            "chance": 0.2,
            "power_text": "You are lightly obscured while in dim light or darkness",
            "position": "suffix",
        },
        {
            "name": "of Swiftness",
            "min_level": 5,
            "chance": 0.2,
            "power_text": "increases movement speed by 10 feet",
            "position": "suffix",
        },
        {
            "name": "Runic",
            "min_level": 5,
            "chance": 0.15,
            "power_text": "+1 to spell attack rolls",
            "position": "prefix",
        },
        {
            "name": "of the Turtle",
            "min_level": 5,
            "chance": 0.15,
            "power_text": "gain +2 temporary HP after a short rest",
            "position": "suffix",
        },

        # Level 6
        {
            "name": "Infernal",
            "min_level": 6,
            "chance": 0.18,
            "power_text": "+2d4 fire damage, resistance to fire",
            "position": "prefix",
        },
        {
            "name": "Soulbound",
            "min_level": 6,
            "chance": 0.14,
            "power_text": "cannot be disarmed while wielding this item",
            "position": "prefix",
        },
        {
            "name": "of Echoes",
            "min_level": 6,
            "chance": 0.12,
            "power_text": "spells cast while holding this item produce faint whispers",
            "position": "suffix",
        },

        # Level 7
        {
            "name": "Glacial",
            "min_level": 7,
            "chance": 0.18,
            "power_text": "+2d4 cold damage, target's speed is reduced by 10 feet until end of next turn",
            "position": "prefix",
        },
        {
            "name": "of Teleportation",
            "min_level": 7,
            "chance": 0.15,
            "power_text": "cast Misty Step as a bonus action (recharge 5-6)",
            "position": "suffix",
        },
        {
            "name": "Shocking",
            "min_level": 7,
            "chance": 0.15,
            "power_text": "+1d6 lightning damage",
            "position": "prefix",
        },
        {
            "name": "Ethereal",
            "min_level": 7,
            "chance": 0.12,
            "power_text": "grants the ability to slightly hover (cosmetic)",
            "position": "prefix",
        },

        # Level 8
        {
            "name": "Radiant",
            "min_level": 8,
            "chance": 0.15,
            "power_text": "+2d6 radiant damage, emits bright light in a 10-foot radius",
            "position": "prefix",
        },
        {
            "name": "of Clarity",
            "min_level": 8,
            "chance": 0.12,
            "power_text": "+2 to Arcana checks",
            "position": "suffix",
        },
        {
            "name": "Vampiric",
            "min_level": 8,
            "chance": 0.08,
            "power_text": "on crit: regain 1d4 hit points",
            "position": "prefix",
        },

        # Level 9
        {
            "name": "of Regeneration",
            "min_level": 9,
            "chance": 0.12,
            "power_text": "regain 5 hit points at the start of your turn if you have at least 1 hit point",
            "position": "suffix",
        },
        {
            "name": "of the Leviathan",
            "min_level": 9,
            "chance": 0.1,
            "power_text": "you can breathe underwater",
            "position": "suffix",
        },

        # Level 10
        {
            "name": "of Void Walking",
            "min_level": 10,
            "chance": 0.1,
            "power_text": "cast Greater Invisibility once per day",
            "position": "suffix",
        },
        {
            "name": "Arcaneforged",
            "min_level": 10,
            "chance": 0.1,
            "power_text": "weapon counts as magical for overcoming resistance",
            "position": "prefix",
        },

        # Level 11
        {
            "name": "of Thunder",
            "min_level": 11,
            "chance": 0.1,
            "power_text": "on hit: target must make a DC 15 Con save or take 2d6 thunder damage",
            "position": "prefix",
        },
        {
            "name": "Howling",
            "min_level": 11,
            "chance": 0.08,
            "power_text": "emits eerie wails when swung; Intimidation checks +2",
            "position": "prefix",
        },

        # Level 12
        {
            "name": "of the Phoenix",
            "min_level": 12,
            "chance": 0.08,
            "power_text": "once per day, regain 10 hit points when reduced to 0 hit points",
            "position": "suffix",
        },
        {
            "name": "of the Dragon's Eye",
            "min_level": 12,
            "chance": 0.07,
            "power_text": "you can detect magic at will",
            "position": "suffix",
        },

        # Level 13
        {
            "name": "of the Storm",
            "min_level": 13,
            "chance": 0.07,
            "power_text": "on hit: target must make a DC 15 Dex save or take 3d6 lightning damage",
            "position": "prefix",
        },
        {
            "name": "Worldshaker",
            "min_level": 13,
            "chance": 0.05,
            "power_text": "on hit: small shockwave pushes creatures 5 feet",
            "position": "prefix",
        },

        # Level 14
        {
            "name": "of the Abyss",
            "min_level": 14,
            "chance": 0.05,
            "power_text": "grants the ability to cast Darkness once per day",
            "position": "suffix",
        },
        {
            "name": "Astral",
            "min_level": 14,
            "chance": 0.05,
            "power_text": "your form flickers, granting +1 AC",
            "position": "prefix",
        },

        # Level 15
        {
            "name": "of the Titan",
            "min_level": 15,
            "chance": 0.03,
            "power_text": "increases strength score by 2 while wielded",
            "position": "prefix",
        },
        {
            "name": "of the Horizon",
            "min_level": 15,
            "chance": 0.04,
            "power_text": "vision range is doubled",
            "position": "suffix",
        },

        # Level 16
        {
            "name": "of Soulfire",
            "min_level": 16,
            "chance": 0.03,
            "power_text": "critical hits deal an extra 2d6 radiant damage",
            "position": "suffix",
        },

        # Level 17
        {
            "name": "Planar",
            "min_level": 17,
            "chance": 0.02,
            "power_text": "you can speak and understand any language",
            "position": "prefix",
        },

        # Level 18
        {
            "name": "God-Touched",
            "min_level": 18,
            "chance": 0.02,
            "power_text": "once per day, you may reroll a d20",
            "position": "prefix",
        },

        # Level 19
        {
            "name": "Eclipseforged",
            "min_level": 19,
            "chance": 0.01,
            "power_text": "this item leaves a trail of shadow-light; cosmetic only",
            "position": "prefix",
        },

        # Level 20
        {
            "name": "of the Ancients",
            "min_level": 20,
            "chance": 0.01,
            "power_text": "you can cast time stop once in your lifetime",
            "position": "suffix",
        },
    ]

    
    def generate_loot_for_character(self, character: Character) -> Item:
        """Generate one loot item for a given character based on their level and class."""
        base_item = self._choose_base_item(character.char_class)
        modifiers = self._roll_modifiers(character.level)
        full_name = self._build_item_name(base_item, modifiers)
        power = self._calculate_power(character.level, modifiers)
        return Item(
            base_item=base_item,
            full_name=full_name,
            modifiers=[m["name"] for m in modifiers],
            power=power,
        )
        
    def _choose_base_item(self, char_class: str) -> str:
        """Choose a base item for a given character class."""
        items = self._base_items_by_class.get(char_class, [])
        if not items:
            return "Mysterious Lint Ball"
        return random.choice(items)
    
    def _roll_modifiers(self, level: int) -> list[dict[str, any]]:
        """Roll for item modifiers based on character level.
        The gimmick for my modifier logic is the higher the level of the character, the more modifiers apply
        """
        chosen: list[dict[str, any]] = []
        for mod in self._modifiers:
            if level < mod["min_level"]:
                continue
            if random.random() < mod["chance"]:
                chosen.append(mod)
        max_mods = max(1, min(5, level // 4))
        if len(chosen) > max_mods:
            chosen = random.sample(chosen, k=max_mods)
        return chosen
    
    def _build_item_name(self, base_item: str, modifiers: list[dict[str, any]]) -> str:
        """Construct the full item name based on base item and modifiers."""
        prefixes: list[str] = []
        suffixes: list[str] = []
        
        for mod in modifiers:
            if mod.get("position") == "prefix":
                prefixes.append(mod["name"])
            elif mod.get("position") == "suffix":
                suffixes.append(mod["name"])
        
        parts: list[str] = []
        parts.extend(prefixes)
        parts.append(base_item)
        parts.extend(suffixes)
        
        return " ".join(parts)
    
    def _calculate_power(self, level: int, modifiers: list[dict[str, any]]) -> int:
        """Calculate the power of an item based on character level and modifiers."""
        base_power = level
        for mod in modifiers:
            # each modifier adds 1 to power
            base_power += 1
        return base_power