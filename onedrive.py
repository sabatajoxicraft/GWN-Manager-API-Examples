# onedrive.py
import os
from dotenv import load_dotenv
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext

from main import get_access_token, FILE_ID, FILE_NAME

load_dotenv()

# You can use get_access_token from main.py here
access_token = get_access_token()

# Get your SharePoint site URL
site_url = 'YOUR_SHAREPOINT_SITE_URL'  # Replace with your SharePoint site URL

# Authenticate using the access token
auth_context = AuthenticationContext(site_url)
auth_context.acquire_token_with_client_credentials(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    resource=site_url
)

# Create a ClientContext object
ctx = ClientContext(site_url, auth_context)

# Example: Inspecting a folder
folder_path = 'path/to/your/folder'  # Replace with the actual folder path on OneDrive

# Get the folder object
folder = ctx.web.get_folder_by_server_relative_url(folder_path)
ctx.load(folder)
ctx.execute_query()

# Print the folder contents
print("Folder Contents:")
for item in folder.folders:
    print(f"- {item.name} (Folder)")
for item in folder.files:
    print(f"- {item.name} (File)")

# Example: Downloading a specific file from the folder
file_name = 'Joxicraft WIFI Voucher 3.xlsx'  # Replace with the name of the file you want to download

# Get the file object
file = ctx.web.get_file_by_server_relative_url(f"{folder_path}/{file_name}")
ctx.load(file)
ctx.execute_query()

# Download the file to the current directory
with open(file_name, 'wb') as f:
    f.write(file.download_binary())

# Example: Downloading a file using FILE_ID from your .env
file = ctx.web.get_file_by_server_relative_url(f"{FILE_NAME}")
ctx.load(file)
ctx.execute_query()

with open(FILE_NAME, 'wb') as f:
    f.write(file.download_binary())

