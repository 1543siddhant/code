import os
import requests

# Input from exec()
folder = input("Enter folder number: ").strip()

OWNER = "1543siddhant"
REPO = "code"

# GitHub API URL
api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{folder}"

# Create local folder
os.makedirs(folder, exist_ok=True)

# Get files list
response = requests.get(api_url)

if response.status_code != 200:
    print("Folder not found!")
    exit()

data = response.json()

# Download all files
for file in data:

    if file["type"] == "file":

        download_url = file["download_url"]
        file_path = os.path.join(folder, file["name"])

        print(f"Downloading {file['name']}...")

        file_data = requests.get(download_url)

        with open(file_path, "wb") as f:
            f.write(file_data.content)

print(f"\nFolder '{folder}' downloaded successfully!")