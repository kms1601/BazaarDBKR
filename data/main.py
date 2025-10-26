import os

import json

from const import CWD, TITLE_ID, TIPS_ID, DESCRIPTION_ID, QUESTS_ID
from data.fetch_translate_data import fetch_translate_data
from fetch_game_data import fetch_game_data
from translate import translate

RESULT = {}


def main():
    if not os.path.exists(f"{CWD}/.json"):
        os.makedirs(f"{CWD}/.json")

    fetch_game_data()
    fetch_translate_data()

    with open(f"{CWD}/.json/{TITLE_ID}.json", "r", encoding="utf-8") as f:
        titles = json.load(f)

    with open(f"{CWD}/.json/{TIPS_ID}.json", "r", encoding="utf-8") as f:
        tooltips = json.load(f)

    with open(f"{CWD}/.json/{DESCRIPTION_ID}.json", "r", encoding="utf-8") as f:
        descriptions = json.load(f)

    with open(f"{CWD}/.json/{QUESTS_ID}.json", "r", encoding="utf-8") as f:
        quests = json.load(f)

    with open(f"{CWD}/.json/cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)


    for card in cards:
        translate(card, titles, tooltips, descriptions, quests)

        result = {
            "title": [],
        }

        en = card["Localization"]["Title"]["Text"]
        kr = card["Localization"]["Title"]["TextKR"] if "TextKR" in card["Localization"]["Title"] else "한국어 텍스트 누락"

        result["title"] = f"<span>{en}</span><span>{kr}</span><span style='opacity: 0.5; font-size: __FONT_SIZE__'>{en}</span><span style='opacity: 0.5; font-size: __FONT_SIZE__'>{kr}</span>"

        key = f"{en}_{card["Type"]}"
        RESULT[key] = result

    # JS 객체 문자열 만들기
    js_code = f"const DATA = {json.dumps(RESULT, ensure_ascii=False, indent=2)};"

    # 파일로 저장
    with open("../data.js", "w", encoding="utf-8") as f:
        f.write(js_code)

    print("data.js 파일 생성 완료!")


if __name__ == "__main__":
    main()
