import os
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

URL_CARD = "https://bazaardb.gg/search?c=all"
URL_SKILLS = "https://bazaardb.gg/search?c=skills"
URL_EVENTS = "https://bazaardb.gg/search?c=events"
URL_MONSTERS = "https://bazaardb.gg/search?c=monsters"
URL_DETAIL = "https://bazaardb.gg/card/cncaftikwwa8eiq7k4s31m1pz/Aludel"


def get_html(url):
    response = requests.get(url)
    html = response.text
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)
    return BeautifulSoup(html, "html.parser")


def get_class_name():
    soup_card = get_html(URL_CARD)
    soup_skills = get_html(URL_SKILLS)
    soup_events = get_html(URL_EVENTS)
    soup_monsters = get_html(URL_MONSTERS)
    soup_detail = get_html(URL_DETAIL)

    element = soup_card.select_one("#cardlist > div > div > div:nth-child(1) > div > div")
    card = "." + element.get("class")[0]
    print("card: " + card)

    element = soup_card.select_one(
        "#cardlist > div > div > div:nth-child(1) > div > div > div > div > div > div > div:nth-child(1) > a:nth-child(1) > h3")
    card_title = "." + element.get("class")[0]
    print("card_title: " + card_title)

    element = soup_card.select_one(
        "#cardlist > div > div > div:nth-child(1) > div > div > div > div > div:nth-child(1) > a > div > div > div")
    image = "." + element.get("class")[0]
    print("image: " + image)

    element = soup_skills.select_one(
        "#cardlist > div > div > div:nth-child(1) > div > div > div > div > div:nth-child(1) > a > div > div > div")
    skill_card_image = image + "." + element.get("class")[1]
    print("skill_card_image: " + skill_card_image)

    element = soup_events.select_one(
        "#cardlist > div > div > div:nth-child(1) > div > div > div > div > div:nth-child(1) > a > div > div > div")
    event_card_image = image + "." + element.get("class")[1]
    print("event_card_image: " + event_card_image)

    element = soup_monsters.select_one(
        "#cardlist > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div > div:nth-child(2) > div:nth-child(1)")
    monster_card_count = "." + element.get("class")[0]
    print("monster_card_count: " + monster_card_count)

    element = soup_detail.select_one("body > div:nth-child(6) > div:nth-child(3) > div")
    detail = "." + element.get("class")[0]
    print("detail: " + detail)

    element = soup_detail.select_one("body > div:nth-child(6) > div:nth-child(3) > div:nth-child(1) > div:nth-child(3)")
    card_detail = "." + element.get("class")[0]
    print("card_detail: " + card_detail)

    driver = webdriver.Chrome()
    driver.get(URL_EVENTS)
    target = driver.find_element(By.CSS_SELECTOR, "#cardlist > div > div > div > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
    ActionChains(driver).move_to_element(target).perform()

    time.sleep(1)

    element = driver.find_element(By.CSS_SELECTOR, "#cardlist > div > div > div > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(6) > div > div > div > div > div > div > div > div > div")
    event_step_image = image + "." + element.get_attribute("class")[4:]
    print("event_step_image: " + event_step_image)

    driver.quit()

    js_code = f"""const PROCESSED_ATTR = "bazaardbkr-processed";

const CARD = "{card}"; // after █ _xx element
const CARD_TITLE = "{card_title}"; // h3 element
    
const SKILL_CARD_IMAGE = "{skill_card_image}";
const EVENT_CARD_IMAGE = "{event_card_image}";
const EVENT_STEP_IMAGE = "{event_step_image}";
    
const MONSTER_CARD_COUNT = "{monster_card_count}"; // tooltip
    
const DETAIL = "{detail}"; // after first element
const CARD_DETAIL = "{card_detail}"; // first element
    """

    with open(os.path.join(os.getcwd() + "/..", "const.js"), "w", encoding="utf-8") as f:
        f.write(js_code)


if __name__ == "__main__":
    get_class_name()
