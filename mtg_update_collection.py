import json
import argparse
import os
import shutil

# TODO: Make it harder to overwrite data / add a way to append to existing data

# Parse arguments
a = argparse.ArgumentParser()
a.add_argument("-p", "--path", help="Full path to json file containing collection")
args = vars(a.parse_args())
path = args.get("path")

# prompt user for path if not provided
if path is None:
    filedir = input("Please enter a path to collection file to be updated: ")
    filename = input("Please enter a name for the collection file: ")
    if not filename.endswith(".json"):
        filename += ".json"
    path = os.path.join(filedir, filename)
path = os.path.expanduser(path)

# If file exists, give user option to exit or overwrite
if os.path.exists(path):
    resp = input("File exists: overwrite? (y/n) ").lower()
    while resp not in ["y", "n", "yes", "no"]:
        resp = input("Invalid response: overwrite? (y/n) ").lower()
    if resp not in ["y", "yes"]:
        print("Exiting...")
        exit(1)
    else:
        # create a backup now before messing anything else up
        print("Okay fine, but I'm backing your shit up.")
        shutil.copy(path, path+'.backup')

print("File to be created/modified: %s" % path)

# loop and prompt user for card info
more = True
collection = []
while True:
    name = input("Please enter card name (case-sensitive): ")
    set = input("Please enter card set (case-sensitive): ")
    foil = input("Foil? (y/n): ").lower() in ["yes", "y"]
    purchase_price = float(input("Please enter approximate price paid for card (USD): "))
    quantity = int(input("Please enter the quantity of this card you own: "))

    card = {"name": name,
            "set": set,
            "foil": foil,
            "purchase_price": purchase_price,
            "quantity": quantity}
    print(json.dumps(card, indent=4))
    if input("Does everything look okay? (y/n): ").lower() in ["yes", "y"]:
        collection.append(card)

    if input("Do you have more cards to enter? (y/n): ").lower() in ["yes", "y"]:
        continue
    else:
        break

print(json.dumps(collection, indent=4, sort_keys=True))

if input("Does everything look okay? (y/n): ").lower() in ["yes", "y"]:
    with open(path, 'w') as f:
        json.dump(collection, f, indent=4, sort_keys=True)
    print("Written file to %s" % path)
else:
    print("Well okay then. Fine.")
    exit(1)
