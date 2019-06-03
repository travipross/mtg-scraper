import json
from mtg_scraper_utils import scrape_and_update


with open("my_collection.json", 'r') as f:
    collection = json.load(f)

scrape_and_update(collection)
print(json.dumps(collection, indent=4, sort_keys=True))
