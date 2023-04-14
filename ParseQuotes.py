import json
import random


def parseQuotes():
    with open("quotesList.json", "w") as jsonFile:

        with open('allHighlights.json','r', encoding="utf8") as file:
            json_data = json.load(file)
            allHighlights = json_data["allHighlights"]
            array = []
            ##need to filter the instagram ones
            for object in allHighlights:
                if "Insta" in object["highlight"]["category"]:
                    textObject = {
                        "Text":object["highlight"]["Text"],
                        "Author":object["author"],
                        "Title":object["title"]
                    }
                    array.append(textObject)
            random.shuffle(array)
            json.dump(array,jsonFile, indent=4)


parseQuotes()