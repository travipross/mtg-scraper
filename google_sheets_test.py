import gspread
from oauth2client.service_account import ServiceAccountCredentials

print("https://docs.google.com/spreadsheets/d/1VqBChGGDQH6f7ljv_zDVrw61sy2nrFjlX1WirEre1sM/edit?usp=sharing")
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("jamietest").sheet1

# Extract and print all of the values
list_of_vals = sheet.get_all_records()
print(list_of_vals)

new_row = ['HELLO', 'WORLD', None, 5, None, None, None, None, None, None, "today"]
for i, v in enumerate(new_row):
    sheet.update_cell(5, i+1, v)

