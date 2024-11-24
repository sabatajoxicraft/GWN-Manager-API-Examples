from ast import And
from calendar import month
import datetime
import math
from turtle import st
import requests
import os
import json
from dotenv import load_dotenv
from hashlib import sha256
import time
from pprint import pprint
from twilio.rest import Client
import pandas as pd
from msdrive import OneDrive
import msal
from typing import List, Dict, Tuple
import math

from voucher_system_classes import APIRequest, Network, VoucherGroup, Voucher, Student, Utils # Import your classes from the other file

load_dotenv()

# --- Constants ---

DEFAULT_ENV = os.getenv("DEFAULT_URL")
ID_ENV = os.getenv("ID")
SECRET_KEY_ENV = os.getenv("Key")
ACCESS_TOKEN_ENV = os.getenv("Access_token")
TWILIO_WHATSAPP_TEMPLATE_SID = os.getenv("TWILIO_WHATSAPP_TEMPLATE_SID")
TWILIO_SMS_TEMPLATE_SID = os.getenv("TWILIO_SMS_TEMPLATE_SID")
TWILIO_MESSAGE_SID = os.getenv("TWILIO_MESSAGE_SID")
TWILIO_MESSAGE_TEMPLATE = os.getenv("TWILIO_MESSAGE_TEMPLATE")
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_SMS_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
FROM_WA_NUMBER = os.getenv("TWILIO_WHATSAPP_NO")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
FILE_ID = os.getenv("FILE_ID")
FOLDER_PATH = os.getenv("FOLDER_PATH")
FILE_NAME = os.getenv("FILE_NAME")
AUTHORITY_URL = os.getenv("AUTHORITY_URL")
TENANT_ID = os.getenv("TENANT_ID")
ALLOWED_DEVICES = os.getenv("ALLOWED_DEVICES")
USE_MESSAGING_SERVICE = False 

# Global variables
student_records = []
client = Client(ACCOUNT_SID, AUTH_TOKEN)


# --- Main function ---

def main():
    print("Starting network interaction...")

    # --- Initialization ---

    cleanup_files()
    token = get_data_store()  # Load access token
    print("My token: " + token)

    # --- Network Selection ---

    # Get the list of network names
    print("Getting network names...")
    network_names = get_network_list_names(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV)
    print("Available networks: ", ', '.join(network_names))

    network_name = input("Enter the network name you want to interact with: ")
    if network_name not in network_names:
        print("Invalid network name. Please enter a valid network name.")
        return

    print(f"Getting network ID for '{network_name}'...")
    networkID = get_network_id(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, NetworkName=network_name)
    store_network_id(networkID)  # Store the network ID after getting it

    # --- Network Object ---

    network = Network(networkID, network_name, DEFAULT_ENV, ID_ENV, SECRET_KEY_ENV, token)

    # --- OneDrive Access ---

    print("Getting OneDrive access token...")
    msToken = get_access_token()

    # --- Excel File Processing ---

    print("Processing Excel file...")
    global student_records
    student_records = process_excel_file(msToken, FILE_NAME)

    # --- Voucher Groups ---

    # Get existing voucher groups
    voucher_groups_data = network.get_voucher_group_list()
    voucher_groups = [VoucherGroup(group['id'], group['name'], network) for group in voucher_groups_data]

    # --- Voucher Month ---

    voucher_month = input("Enter the month for which you are generating vouchers (e.g., January, February): ").lower()
    voucher_month = determine_month(voucher_month)  # Determine the correct month in the year

    # --- Voucher Matching and Sending ---

    # Match voucher groups based on month and accommodation
    matching_groups = match_voucher_groups(student_records, voucher_groups_data, voucher_month)

    all_vouchers = []
    matched_vouchers = []
    unmatched_vouchers = []
    if matching_groups:
        # Fetch existing voucher groups
        for group_id in [group['id'] for group in voucher_groups_data]:
            for group in matching_groups:
                if group_id == group['id']:
                    vouchers_in_group = network.get_voucher_list_in_group(group['id'])
                    existing_vouchers_in_groups.append(vouchers_in_group)
                    break

        all_vouchers, matched_vouchers = match_voucher_codes(student_records, existing_vouchers_in_groups, voucher_month)
    else:
        # Create new voucher groups if none exist
        all_vouchers = create_voucher_groups(student_records, voucher_month, networkID, token, [group['name'] for group in voucher_groups_data]) 

    # --- Student Objects ---

    students = [Student(student_data, network) for student_data in student_records]

    # --- Send Vouchers ---

    for student in students:
        if not student.has_voucher():
            # Get a voucher from the appropriate group
            voucher_password = None  # Replace with actual voucher fetching logic
            if voucher_password:
                success = student.send_voucher(voucher_password, voucher_month)
                if success:
                    print(f"Voucher sent to {student.student_data['First name']} {student.student_data['Last name']}.")

    # --- Excel File Modification ---

    modify_excel_file(FILE_NAME, msToken)

if __name__ == "__main__":
    main()