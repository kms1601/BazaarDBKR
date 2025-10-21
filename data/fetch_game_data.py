import json

from const import BAZAAR_URL, CWD
from fetch_json import fetch


def fetch_game_data():
    cards_with_version = fetch(f"{BAZAAR_URL}/static/cards.json")
    version = list(cards_with_version.keys())[0]
    cards = cards_with_version[version]
    with open(f"{CWD}/.json/cards.json", "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False)


def main():
    fetch_game_data()


if __name__ == "__main__":
    main()
