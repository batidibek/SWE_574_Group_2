import requests
import json

def new_annotation(body):
    url = "https://swe574-278917.appspot.com/annotations"
    params = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "type": "Annotation",
        "body": {
            "type": "TextualBody",
            "value": body["body"]["value"],
            "format": "text/plain"
        },
        "target": {
            "source": body["target"]["source"],
            "selector": {
                "type": "CssSelector",
                "value": body["target"]["selector"]["value"]
            }
        },
        "creator": body["creator"]
    }
    response = requests.post(url=url, json=params).json()
    print(response)
    return response

def get_annotations_page(page):
    url = "https://swe574-278917.appspot.com/annotations"
    response = requests.get(url=url, params={"page": page}).json()
    print(response)
    return response