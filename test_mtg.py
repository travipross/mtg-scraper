import json

with open("my_collection.json", 'r') as f:
    collection = json.load(f)

for card in collection:
    print(card.get("name"), end="\t")
    print(card.get("price"))