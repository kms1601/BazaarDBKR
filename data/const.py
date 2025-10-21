import os

from fetch_json import fetch


CWD = os.getcwd()
PARATRANZ_URL = "https://paratranz.cn/api/projects"
BAZAAR_URL = "https://data.playthebazaar.com"
PROJECT_ID = 16333
DESCRIPTION_API = "ParatranzTranslateString_API_Cards_Description.json"
QUESTS_API = "ParatranzTranslateString_API_Cards_Quest.json"
TIPS_API = "ParatranzTranslateString_API_Cards_Tips.json"
TITLE_API = "ParatranzTranslateString_API_Cards_Title.json"
TOOLTIPS_API = "ParatranzTranslateString_API_Tooltips.json"
DESCRIPTION_ID = 2372720
QUESTS_ID = 2374157
TIPS_ID = 2372718
TITLE_ID = 2372719
TOOLTIPS_ID = 2359907

# file_list = fetch(f"{PARATRANZ_URL}/{PROJECT_ID}/files")
# for f in file_list:
#     if f["name"] == DESCRIPTION_API:
#         DESCRIPTION_ID = f["id"]
#     elif f["name"] == QUESTS_API:
#         QUESTS_ID = f["id"]
#     elif f["name"] == TIPS_API:
#         TIPS_ID = f["id"]
#     elif f["name"] == TITLE_API:
#         TITLE_ID = f["id"]
#     elif f["name"] == TOOLTIPS_API:
#         TOOLTIPS_ID = f["id"]

