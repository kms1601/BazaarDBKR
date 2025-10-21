import json

from const import *
from fetch_json import fetch


def fetch_translate_data():
    for id_num in [DESCRIPTION_ID, QUESTS_ID, TIPS_ID, TITLE_ID, TOOLTIPS_ID]:
        data = fetch(f"{PARATRANZ_URL}/{PROJECT_ID}/files/{id_num}/translation")

        with open(f"{CWD}/.json/{id_num}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    fetch_translate_data()


if __name__ == "__main__":
    main()
