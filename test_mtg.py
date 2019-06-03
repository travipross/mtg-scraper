import json
import re


def encode_for_url_without_escapes(card_name):
    if card_name is None:
        raise ValueError("Shit's fucked, yo")
    _chars_to_remove = ["\'", ","]
    name_url = re.sub(" ", "+", card_name)
    name_url = re.sub("|".join(_chars_to_remove), "", name_url)
    return name_url


def build_url_from_card_name(card_dict):
    if card_dict is None:
        raise ValueError("Shit's fucked, yo")
    name_url = encode_for_url_without_escapes(card_dict.get("name")) + "#paper"
    set_url = encode_for_url_without_escapes(card_dict.get("set"))
    if card_dict.get("foil"):
        set_url += ":Foil"
    url = "/".join(["https://www.mtggoldfish.com/price/", set_url, name_url])
    return url


with open("my_collection.json", 'r') as f:
    collection = json.load(f)

for card in collection:
    url = build_url_from_card_name(card)
    print(url)
