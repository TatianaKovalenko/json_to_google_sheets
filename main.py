import json
from a1range import A1Range
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1JcuP80WL08h4L2H3ALBel--ozI5JvKTOrHMPNfLZueE'
SAMPLE_RANGE_NAME = 'first'


service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

# Call the Sheets API
result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()

data_from_sheet = result.get('values', [])

data_values = []
count = 0

with open("file.json", "r", encoding="utf8") as file:
    text = json.load(file)
for txt in text["data"]:
    for i in txt:
        if count < 10:
            data_values.append([i, txt[i]])
        else:
            data_values[count % 10].append(txt[i])
        count += 1

print(data_values)
array = {'values': data_values}
range_ = A1Range.create_a1range_from_list('first', 1, 1, array['values']).format()
response = service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                          range=range_,
                          valueInputOption='USER_ENTERED',
                          body=array).execute()




