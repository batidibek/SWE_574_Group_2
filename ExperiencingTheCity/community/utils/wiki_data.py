from __future__ import unicode_literals

import requests

def suggest_tags(query):
    wiki_items = {}
    wiki_items["items"] = get_wiki_data_items(query, 10)
    tags = {}
    tags["items"] = []
    if wiki_items["items"] == []:
        return None
    counter = 0
    deleted_keys = []
    for item in wiki_items['items']:
        if counter != 0:
            for i in range(0,counter):
                print(str(item["label"]).lower() + "    " + str(wiki_items["items"][i]["label"]).lower())
                if str(item["label"]).lower() == str(wiki_items["items"][i]["label"]).lower():
                    print("true")
                    deleted_keys.append(item)
                    break
        counter = counter + 1
    for key in deleted_keys:
        wiki_items["items"].remove(key)
    return wiki_items

def get_wiki_data_items(search_term, limit):
    url = "https://www.wikidata.org/w/api.php"
    params = {
    "action": "wbsearchentities",
    "format": "json",
    "language": "en",
    "limit": limit,
    "search": search_term
    }
    response = requests.get(url=url, params=params)
    data = response.json()
    return data["search"]