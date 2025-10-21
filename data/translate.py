import json

from const import *

ENCHANTMENT_NAME = ["Heavy", "Golden", "Icy", "Turbo", "Shielded", "Restorative", "Toxic", "Fiery", "Shiny", "Deadly",
                    "Radiant", "Obsidian"]


def translate(card: dict, title: dict, tooltips: dict, descriptions: dict, quests: dict) -> None:
    translate_title(card, title)
    translate_tooltips(card, tooltips, quests)
    translate_description(card, descriptions)


def translate_title(card: dict, translate_titles_kr: dict) -> None:
    for tran in translate_titles_kr:
        if card["Localization"]["Title"]["Text"] == tran["original"]:
            card["Localization"]["Title"]["TextKR"] = tran["translation"]
            break


def translate_tooltips(card: dict, translate_tooltips_kr: dict, translate_quest_kr: dict) -> None:
    for tooltip in card["Localization"]["Tooltips"]:
        for tran in translate_tooltips_kr:
            if tooltip["Content"]["Text"] == tran["original"]:
                tooltip["Content"]["TextKR"] = tran["translation"]
                break
    if "Enchantments" in card and card["Enchantments"]:
        translate_enchantments(card, translate_tooltips_kr)
    if "Quests" in card and card["Quests"]:
        translate_quests(card, translate_quest_kr)


def translate_enchantments(card: dict, translate_tooltips_kr: dict) -> None:
    for enchantment in ENCHANTMENT_NAME:
        if enchantment not in card["Enchantments"]:
            continue
        ench = card["Enchantments"][enchantment]
        for tooltip in ench["Localization"]["Tooltips"]:
            for tran in translate_tooltips_kr:
                if tooltip["Content"]["Text"] == tran["original"]:
                    tooltip["Content"]["TextKR"] = tran["translation"]
                    break


def translate_quests(card: dict, translate_quests_kr: dict) -> None:
    for quest in card["Quests"]:
        for q in quest["Entries"]:
            for tooltip in q["Localization"]["Tooltips"]:
                for tran in translate_quests_kr:
                    if tooltip["Content"]["Text"] == tran["original"]:
                        tooltip["Content"]["TextKR"] = tran["translation"]
                        break
            for tooltip in q["Reward"]["Localization"]["Tooltips"]:
                for tran in translate_quests_kr:
                    if tooltip["Content"]["Text"] == tran["original"]:
                        tooltip["Content"]["TextKR"] = tran["translation"]
                        break


def translate_description(card: dict, translate_descriptions_kr: dict) -> None:
    if "Description" in card["Localization"] and card["Localization"]["Description"]:
        for tran in translate_descriptions_kr:
            if card["Localization"]["Description"]["Text"] == tran["original"]:
                card["Localization"]["Description"]["TextKR"] = tran["translation"]
                break
