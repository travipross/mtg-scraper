import json
import argparse
from mtg_scraper_utils import scrape_and_update
import pandas as pd

a = argparse.ArgumentParser()
a.add_argument("-p", "--path-to-collection", help="Path to json file containing data", default="my_collection.json")
a.add_argument("--overwrite", help="Overwrite file contents with new data (be sure to have a backup)", action='store_true', default=False)
a.add_argument("--update", help="Update information from web", action='store_true', default=False)
a.add_argument("--show", help="Print json file to console", action='store_true', default=False)
args = vars(a.parse_args())

# get arguments
path = args.get("path_to_collection", "my_collection.json")
overwrite = args.get("overwrite")
update_collection = args.get("update")
show = args.get("show")


# Open json file for updating
try:
    with open(path, 'r') as f:
        # TODO: Add some sort of validation for file since it's user-editable (jsonschema?)
        collection = json.load(f)
except FileNotFoundError as e:
    print("File not found: %s" % path)
    exit(1)

# Modify imported dictionary with new data if instructed to do so
if update_collection:
    updated_list = scrape_and_update(collection)
    print("Cards with updated data: %d (errors: %d)" % (updated_list.count(True), updated_list.count(None)))

    # Overwrite original file with new information
    if overwrite and updated_list.count(True) > 0:
        with open(path, 'w') as f:
            json.dump(collection, f, indent=4, sort_keys=True)

# Show json collection in console
if show:
    print(json.dumps(collection, indent=4, sort_keys=True))

# convert to pandas data frame for easier number crunchin'
df = pd.DataFrame(collection)

# summarize results
top3 = df.sort_values("current_price", ascending=False)
print("\n---------- Top cards by value ----------")
for i in range(3):
    print("#%d\t$%0.2f USD\t%s - %s%s" % (i+1,
                                        top3.current_price.iloc[i],
                                        top3.name.iloc[i],
                                        top3.set.iloc[i],
                                        (" (Foil)" if top3.foil.iloc[i] else "")
                                        ))
print("\nTotal value of card collection: $%0.2f USD" % (df.current_price * df.quantity).sum())
print("----------------------------------------")
print("Number of cards documented: %d (%d unique)" % (df.quantity.sum(), df.name.count()))
print("Most duplicates: %s = qty %d" % (df.name.loc[df.quantity.idxmax()], df.quantity.max()))
