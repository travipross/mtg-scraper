import json
import argparse
from mtg_scraper_utils import scrape_and_update


a = argparse.ArgumentParser()
a.add_argument("-p", "--path-to-collection", help="Path to json file containing data", default="my_collection.json")

args = vars(a.parse_args())
path = args.get("path-to-collection", "my_collection.json")
with open(path, 'r') as f:
    collection = json.load(f)

scrape_and_update(collection)
print(json.dumps(collection, indent=4, sort_keys=True))
