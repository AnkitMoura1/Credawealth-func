import os
import requests
import csv
import datetime
from appwrite.client import Client
from appwrite.services.databases import Databases

# --- Read env vars ---
APPWRITE_ENDPOINT = os.environ.get("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.environ.get("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.environ.get("APPWRITE_API_KEY")
APPWRITE_DB_ID = os.environ.get("APPWRITE_DB_ID")
APPWRITE_COLLECTION_ID = os.environ.get("APPWRITE_COLLECTION_ID")

# --- Setup Appwrite client ---
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

db = Databases(client)

# Get yesterday's date in required format
today = datetime.date.today() - datetime.timedelta(days=1)
formatted_date = today.strftime("%d-%b-%Y")

# URL
url = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={formatted_date}"

print(url)

# Fetch response
resp = requests.get(url)

# Split response into lines and create CSV reader
lines = resp.text.splitlines()
reader = csv.reader(lines, delimiter=';')

# Extract headers
headers = next(reader)
headers = [h.strip() for h in headers]  # clean headers

# Collect only rows where first element starts with a digit
filtered_rows = []
for row in reader:
    row = [col.strip() for col in row]  # strip spaces
    if row and row[0] and row[0][0].isdigit():
        filtered_rows.append(row)

# Convert to list of dictionaries
data = [dict(zip(headers, row)) for row in filtered_rows]

# Save as JSON
output_filename = f"amfi_data_{formatted_date}.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"JSON file saved as {output_filename} with {len(data)} records.")
