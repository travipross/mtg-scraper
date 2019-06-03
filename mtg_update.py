import json
import argparse
from mtg_scraper_utils import scrape_and_update


a = argparse.ArgumentParser()
a.add_argument("-p", "--path-to-collection", help="Path to json file containing data", default="my_collection.json")
a.add_argument("--overwrite", help="Overwrite file contents with new data (be sure to have a backup)", action='store_true', default=False)
args = vars(a.parse_args())
path = args.get("path_to_collection", "my_collection.json")
overwrite = args.get("overwrite")

# Open json file for updating
try:
    with open(path, 'r') as f:
        collection = json.load(f)
except FileNotFoundError as e:
    print("File not found: %s" % path)
    exit(1)

# Modify imported dictionary with new data
scrape_and_update(collection)
print(json.dumps(collection, indent=4, sort_keys=True))
