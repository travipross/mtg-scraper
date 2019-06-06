import json
import argparse
import os
import shutil

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

print("File to be modified: %s" % path)

# If file exists, give user option to exit or overwrite
if os.path.exists(path):
    resp = input("File exists: (o)verwrite/(a)ppend/(c)ancel? ").lower()
    while resp not in ["o", "c", "a"]:
        resp = input("Invalid response: (o)verwrite/(a)ppend/(c)ancel? ").lower()
    if resp == "c":
        print("Exiting...")
        exit(1)
    else:
        # create a backup now before messing anything else up
        print("Okay fine, but I'm backing your shit up.")
        shutil.copy(path, path+'.backup')

        if resp == "a":
            with open(path) as f:
                collection = json.load(f)
                print("Loaded collection with %d entries" % len(collection))
        else: # overwrite mode
            collection = []
            print("Starting with empty collection and overwriting file")

# loop and prompt user for card info
more = True
while True:
    name = input("Please enter card name (case-sensitive): ")
    card_set = input("Please enter card set (case-sensitive): ")
    foil = input("Foil? (y/n): ").lower() in ["yes", "y"]
    purchase_price = float(input("Please enter approximate price paid for card (USD): "))
    quantity = int(input("Please enter the quantity of this card you own: "))

    card = {"name": name,
            "set": card_set,
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

if input("Does everything look okay? That's the full file. (y/n): ").lower() in ["yes", "y"]:
    with open(path, 'w') as f:
        json.dump(collection, f, indent=4, sort_keys=True)
    print("Written file to %s" % path)
else:
    print("Well okay then. Fine.")
    exit(1)
