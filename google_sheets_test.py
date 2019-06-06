import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

with open("my_collection.json") as f:
    collection_list = json.load(f)

client_secret_path = os.getenv("MTG_SECRET")
if not client_secret_path:
    print("Please set $MTG_SECRET environment variable to location of secret.json file")
    exit(1)

print("Working on sheet: %s" %
      "https://docs.google.com/spreadsheets/d/1VqBChGGDQH6f7ljv_zDVrw61sy2nrFjlX1WirEre1sM/edit?usp=sharing")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_path, scope)
except FileNotFoundError as e:
    print(e)
    print("Please ensure credentials file exists in the specified location. ")
    exit(1)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("jamietest").sheet1

# Extract and print all of the values
list_of_vals = sheet.get_all_records()
print(list_of_vals)
print(sheet.row_values(1))

row_labels = {'name': 'Card Name',
              'card_set': 'Card Set',
              'foil': 'Is Foil?',
              'quantity': 'Quantity',
              'purchase_price': 'Purchase Price',
              'current_price': 'Current Price',
              'highest_price': 'Highest Price',
              'lowest_price': 'Lowest Price',
              'daily_change': 'Daily Change',
              'weekly_change': 'Weekly Change',
              'time_updated': 'Time Updated',
              'url': 'URL'}

# Update title row
title_row = sheet.range(1, 1, 1, len(row_labels))
for i in range(len(title_row)):
    title_row[i].value = list(row_labels.values())[i]
sheet.update_cells(title_row)


# Update body
document_body = sheet.range(2, 1, len(collection_list)+1, len(row_labels))

new_values = [card.get(k) for card in collection_list for k in row_labels.keys()]

for i, cell in enumerate(document_body):
    cell.value = new_values[i]
sheet.update_cells(document_body)
# new_row = ['HELLO', 'WORLD', None, 5, None, None, None, None, None, None, "today"]
# for i, v in enumerate(new_row):
#     sheet.update_cell(5, i+1, v)
#

# for card, idx in enumerate(collection_list):
#     for k,v in card:
