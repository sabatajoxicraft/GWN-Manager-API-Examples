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

load_dotenv()

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
USE_MESSAGING_SERVICE = False  # Use messaging service by default

student_records = []  # Initialize it as an empty list

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def get_token(DEFAULT_URL, ID, SECRET_KEY):
    Data = {
        "grant_type" : "client_credentials",
        "client_id" : ID,
        "client_secret" : SECRET_KEY
    }
    r = requests.get(DEFAULT_URL + "/oauth/token", params=Data)
    res = json.loads(r.text)
    
    return res["access_token"]

def get_access_token():
    if AUTHORITY_URL is None or TENANT_ID is None:
        raise ValueError("AUTHORITY_URL and TENANT_ID must be set")

    app = msal.PublicClientApplication(authority=AUTHORITY_URL + TENANT_ID, client_id=CLIENT_ID)

    # Start the device flow and print instructions to screen
    flow = app.initiate_device_flow(scopes=["Files.Read.All"])
    print(flow["message"])

    # Block until user logs in
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(result["error"])

def get_network_id(DEFAULT_URL, Access_token, appID, appSecret, NetworkName):
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "type": "asc",
        "order": "id",
        "search": "",
        "pageNum": 1,
        "pageSize": 5
    }
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()
    
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/network/list'
    network_response = requests.get(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)
    ##debug(network_response.url)

    networkList = ljson(network_response.text)['data']['result']

    for network in networkList:
            if network['networkName'] == NetworkName:
                return network['id']  # Return the network data if its ID matches

    return None  # Return None if the ID is not found

def get_network_list_names(DEFAULT_URL, Access_token, appID, appSecret):
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "type": "asc",
        "order": "id",
        "search": "",
        "pageNum": 1,
        "pageSize": 5
    }
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()
    
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/network/list'
    network_response = requests.get(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)
    ##debug(network_response.url)

    networkList = ljson(network_response.text)['data']['result']

    networkNames = [network['networkName'] for network in networkList]
    return networkNames

def get_network_details(DEFAULT_URL, Access_token, appID, appSecret, networkID):
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "id": networkID
    }
    
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()
    
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/network/detail'  # Updated endpoint
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    ##debug(ljson(network_response.text)['data'])

def edit_client(DEFAULT_URL, Access_token, appID, appSecret, networkID, client_data):
    """Edits an existing client on the GWN network."""
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }

    body_data = {
        "networkId": networkID,
        "mac": client_data["MAC"],
        "userName": client_data["Username"],
        "password": client_data["Password"],
        "state": "enable"
    }

    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()

    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])

    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/client/edit'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    if network_response.status_code == 200:
        print(f"Client with MAC: {client_data['MAC']} edited successfully.")
    else:
        print(f"Error editing client: Status Code: {network_response.status_code}")
        print("Response Content:", network_response.text)

def get_client_list(DEFAULT_URL, Access_token, appID, appSecret, networkID):
    """Gets a list of clients on the GWN network."""
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }

    body_data = {
        "networkId": networkID,
        "search": "",  # Or any search criteria
        "order": "mac",  # Or any other order criteria
        "type": "asc",  # Or "desc"
        "pageNum": 1,  # Page number
        "pageSize": 100  # Number of clients per page
    }

    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()

    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])

    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/client/list'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    if network_response.status_code == 200:
        return ljson(network_response.text)['data']['result']
    else:
        print(f"Error getting client list: Status Code: {network_response.status_code}")
        print("Response Content:", network_response.text)
        return []

def get_client_details(DEFAULT_URL, Access_token, appID, appSecret, networkID, mac_address):
    """Gets details of a specific client on the GWN network."""
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }

    body_data = {
        "networkId": networkID,
        "mac": mac_address
    }

    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()

    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])

    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/client/detail'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    if network_response.status_code == 200:
        return ljson(network_response.text)['data']
    else:
        print(f"Error getting client details: Status Code: {network_response.status_code}")
        print("Response Content:", network_response.text)
        return None

def get_voucher_group_list(DEFAULT_URL, Access_token, appID, appSecret, networkID):
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "search": "",
        "order": "name",
        "pageNum": 1,
        "pageSize": 10,
        "networkId": networkID
    }
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()
    
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/voucher/list'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    # debug(ljson(network_response.text)['data'])

    return ljson(network_response.text)['data']['result']

def get_voucher_list_in_group(DEFAULT_URL, Access_token, appID, appSecret, groupId, networkId):
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "search": "",
        "order": "",
        "type": "",
        "pageNum": 1,
        "pageSize": 100,
        "filter": {
            "state": ""
        },
        "groupId": groupId,
        "networkId": networkId
    }
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()
    
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/voucher/vouchers/list'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    voucher_list = ljson(network_response.text)['data']['result']
    voucher_password = [voucher['password'] for voucher in voucher_list]
    return voucher_password

def new_voucher_group(DEFAULT_URL, Access_token, appID, appSecret, VoucherData):
    print("Creating new voucher group...")
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }

    print("Building request data...")
    body_data = {
        "networkId": VoucherData["networkId"],
        "name": VoucherData["voucherName"],
        "vocherNum": VoucherData["vocherNum"],
        "deviceNum": VoucherData["deviceNum"],
        "expiration": VoucherData["expiration"],
        "effectDurationMap": {
            "d": VoucherData["effectDurationMap"]["d"],
            "h": VoucherData["effectDurationMap"]["h"],
            "m": VoucherData["effectDurationMap"]["m"]
        },
        "description": VoucherData["description"]
    }
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    print("Calculating signature...")
    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()

    print("Building request payload...")
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])

    print(f"Sending POST request to '{DEFAULT_URL}/oapi/v1.0.0/voucher/save'...")
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/voucher/save'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    if network_response.status_code == 200:
        print("Voucher group created successfully!")
        ljson(network_response.text)
        debug(network_response.text)
    else:
        print(f"Error creating voucher group: Status Code: {network_response.status_code}")
        print("Response Content:", network_response.text)

def get_ssid(DEFAULT_URL, Access_token, appID, appSecret, networkID):
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "search": "",
        "order": "name",
        "pageNum": 1,
        "pageSize": 10,
        "networkId": networkID
    }
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()
    
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/ssid/list'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    ##debug(ljson(network_response.text)['data'])
    
def get_ap(DEFAULT_URL, Access_token, appID, appSecret, networkID):
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "search": "",
        "order": "name",
        "pageNum": 1,
        "pageSize": 10,
        "networkId": networkID
    }
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()
    
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/ap/list'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    ##debug(ljson(network_response.text)['data'])
    
def get_portals(DEFAULT_URL, Access_token, appID, appSecret, networkID):
    print("get-portal")
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "networkId": networkID
    }
    params = "&".join([f"{key}={public_params[key]}" for key in public_params])
    body = json.dumps(body_data, separators=(',', ':'))

    body_signature = sha256(body.encode()).hexdigest()
    signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()
    
    payload_data = {
        'access_token': Access_token,
        'appID': appID,
        'timestamp': timestamp,
        'signature': signature
    }

    payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/portal/list'
    ##debug(network_url)
    ##print(payload)
    ##print(body)
    
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)
    #print("get-portal")
    debug(ljson(network_response.text)['data'])

def ljson(input):
    json_return = json.loads(str(input))
    return json_return

def debug(input):
    pprint(input)
    print("")

def store_token(token):
    with open('token_store.txt', 'w') as f:
        json.dump({'token': token, 'timestamp': time.time()}, f)

def load_token():
    if os.path.exists('token_store.txt'):
        with open('token_store.txt', 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] < 300:  # Check if token is less than 15 minutes old
                return data['token']
    return None

def get_data_store():
    token = None
    if os.path.exists('token_store.txt'):
        with open('token_store.txt', 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] < 300:  # Check if token is less than 30 minutes old
                token = data['token']
    if token is None:
        token = get_token(DEFAULT_URL=DEFAULT_ENV, ID=ID_ENV, SECRET_KEY=SECRET_KEY_ENV)
        store_token(token)
    return token

def store_network_id(network_id):
    with open('network_store.txt', 'w') as f:
        json.dump({'network_id': network_id, 'timestamp': time.time()}, f)

def load_network_id():
    if os.path.exists('network_store.txt'):
        with open('network_store.txt', 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] < 3600:  # Check if network_store is less than 1 hour old
                return data['network_id']
    return None

def cleanup_files():
    if FILE_NAME is not None and os.path.exists(FILE_NAME):
        file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(FILE_NAME))
        one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)

        if file_modified_time < one_hour_ago:  # Check if file is older than 1 hour
            os.remove(FILE_NAME)  # Remove the file

def calculate_last_day_of_month(month):
    # Dummy implementation for the sake of completeness
    month_names = ["january", "february", "march", "april", "may", "june",
                   "july", "august", "september", "october", "november", "december"]
    current_year = datetime.datetime.now().year
    month_index = month_names.index(month.lower()) + 1
    next_month = datetime.datetime(current_year, month_index % 12 + 1, 1)
    return next_month - datetime.timedelta(days=1)

def get_voucher_data(networkID, voucher_group_number, voucher_month, accommodation_name, existing_voucher_groups, student_count):
    """
    Gets voucher data for a specific group, using data from the Excel file to suggest values.
    Checks if a voucher group already exists based on the name.

    Args:
        networkID (int): The network ID.
        voucher_group_number (int): The voucher group number.
        voucher_month (str): The voucher month in the format "Month Year" (e.g., "January 2025").
        accommodation_name (str): The accommodation name.
        existing_voucher_groups (list): A list of existing voucher groups.
        student_count (int): The number of students staying at the accommodation.

    Returns:
        dict: A dictionary containing voucher data.
    """
    # Extract month and year from the voucher month string
    month_name, month_year = voucher_month.split()
    month_year = int(month_year)

    # Calculate days left in the month (for expiration)
    last_day_of_month = calculate_last_day_of_month(month_name)
    if last_day_of_month is None:
        return None

    # Automatically populate voucher name and description
    voucherName = f"{month_name.title()} {month_year} - {accommodation_name.capitalize()}"
    description = f"{accommodation_name.capitalize()} voucher for {month_name.title()} {month_year}"

    # Check if the voucher group already exists
    if voucherName in existing_voucher_groups:
        print(f"Voucher group '{voucherName}' already exists. Reusing existing group.")
        return None  # Don't create a new group

    # Use the student_count directly as the number of vouchers
    print(f"We will create '{student_count}' vouchers + 10% extra")
    voucherNum = student_count + int(student_count * 0.1)  # Add 10% extra vouchers

    # Calculate the effect duration (delay until the beginning of the month)
    current_date = datetime.datetime.now()
    month_names = ["january", "february", "march", "april", "may", "june",
                   "july", "august", "september", "october", "november", "december"]

    # Determine the effect duration and expiration (current month vs. future month)
    if voucher_month == datetime.date.today().strftime("%B %Y").lower():
        print("Current month logic")
        # Calculate seconds until midnight of the last day of the current month
        midnight_last_day = datetime.datetime.combine(last_day_of_month, datetime.time(23, 59, 59))
        seconds_until_midnight = (midnight_last_day - current_date).total_seconds()

        # Convert seconds_until_midnight to days
        till_last_day_in_days = int(seconds_until_midnight / (60 * 60 * 24))  # Convert seconds to days

        # Calculate remaining hours and minutes
        seconds_remaining = seconds_until_midnight - (till_last_day_in_days * 60 * 60 * 24)
        last_day_hrs = int(seconds_remaining // (60 * 60))  # Calculate hours
        last_day_mins = int((seconds_remaining - (last_day_hrs * 60 * 60)) // 60)  # Calculate minutes

        # Set expiration_days and effectDurationMap
        expiration_days = till_last_day_in_days + 1
        effectDurationMap = {
            "d": till_last_day_in_days,
            "h": last_day_hrs, #23
            "m": last_day_mins #59
        }
        print(f"expiration_days: {expiration_days}")
        print(f"effectDurationMap: {effectDurationMap}")
    else:
        print("Future month logic")
        # Calculate seconds in the future month
        start_of_month = datetime.datetime(current_date.year, month_names.index(voucher_month) + 1, 1, 0, 0, 0)
        midnight_last_day = datetime.datetime.combine(last_day_of_month, datetime.time(23, 59, 59))
        seconds_in_month = (start_of_month - midnight_last_day).total_seconds()

        # Set expiration_days and effectDurationMap
        expiration_days = int(seconds_in_month / (60 * 60 * 24)) + 1  # Convert seconds to days
        effectDurationMap = {
            "d": int(seconds_in_month / (60 * 60 * 24)),  # Delay in days until the start of the month
            "h": 0,
            "m": 1
        }
        print(f"expiration_days: {expiration_days}")
        print(f"effectDurationMap: {effectDurationMap}")

    VoucherData = {
        "networkId": networkID,
        "voucherName": voucherName,
        "vocherNum": voucherNum,
        "deviceNum": ALLOWED_DEVICES,
        "expiration": expiration_days,
        "effectDurationMap": effectDurationMap,
        "description": description,
        "voucherMonth": voucher_month
    }
    return VoucherData

def modify_student_data(voucher_month, voucher_password, to_number, student_name, sent="Yes"):
    """
    Modifies the student data in the `student_records` dictionary with the voucher
    information, using the phone number and name for accurate identification.
    """
    global student_records
    to_number = to_number.strip("+")  # Remove the "+" from the phone number
    for index, student in enumerate(student_records):
        student_phone_number = format_number(student['WhatsApp number']).strip("+")
        if (student_phone_number == to_number and
            f"{student['First name']} {student['Last name']}" == student_name):
            student_records[index]['Voucher Code'] = voucher_password
            student_records[index]['Voucher Month'] = voucher_month
            student_records[index]['Voucher Sent'] = sent
            break  # Exit the loop after finding the correct student

    return student_records

def format_number(number):
    """
    Formats a phone number to the South African international format.

    Args:
        number (str or int): The phone number to be formatted.

    Returns:
        str: The formatted phone number in the South African international format.

    Raises:
        None

    Examples:
        >>> format_number('0821234567')
        '+27821234567'

        >>> format_number(821234567)
        '+27821234567'
    """
    # Convert number to string if it's not already a string
    if not isinstance(number, str):
        number = str(number)
    # Remove any spaces or special characters from the number
    number = number.replace(' ', '').replace('-', '')
    # Check if the number is a valid 9 or 10-digit number
    if len(number) == 11 and number.startswith('27'):
        return '+' + number
    elif len(number) == 10 and number.startswith('0'):
        return '+27' + number[1:]
    elif len(number) == 9:
        return '+27' + number
    else:
        return number

def process_excel_file(msToken, FILE_NAME):
    """
    Process an Excel file by downloading it from OneDrive, reading specific columns,
    modifying the file, and returning the column data.

    Parameters:
    - token (str): The access token for OneDrive authentication.
    - FILE_NAME (str): The name of the Excel file on OneDrive.
    - all_vouchers (list): A list of vouchers to be used for modifying the Excel file.

    Returns:
    - student_records (dict): A dictionary containing the data from specific columns of the Excel file.
    """
    global student_records

    # Initialize OneDrive
    drive = OneDrive(msToken)

    ItemPath = f"/{FILE_NAME}"
    # Download the Excel file from OneDrive
    drive.download_item(item_path=ItemPath, file_path=f'{FILE_NAME}')

    # Read specific columns from the Excel file
    student_records = read_excel_columns(FILE_NAME)

    return student_records

def read_excel_columns(filename):
    df = pd.read_excel(filename, usecols=None)
    return df.to_dict(orient='records')

def modify_excel_file(FILE_NAME, msToken):
    """
    Modifies the Excel file and uploads it back to OneDrive.
    """
    global student_records
    df = pd.DataFrame(student_records)
    df.to_excel(FILE_NAME, index=False)
    print(f"File: {FILE_NAME} saved!")

    """ drive = OneDrive(msToken)

    ItemPath = f"/{FILE_NAME}"
    # Upload the updated Excel file back to OneDrive
    drive.upload_item(item_path=ItemPath, file_path=f'{FILE_NAME}') """

def send_message(all_vouchers, voucher_month, voucher_group_names):
    """
    Sends an SMS or WhatsApp message for each voucher in the first group based on the preferred communication option.
    If WhatsApp fails, falls back to SMS using the same message structure.
    """

    global student_records

    if all_vouchers and student_records:

        # Group students by accommodation
        students_by_accommodation = {}
        for student_data in student_records:
            accommodation = student_data.get("Which accommodation do you stay at?")
            if accommodation:  # Check if accommodation is not None
                if accommodation not in students_by_accommodation:
                    students_by_accommodation[accommodation] = [] 
                students_by_accommodation[accommodation].append(student_data)
            else:
                print(f"Skipping student with no accommodation information: {student_data.get('First name')} {student_data.get('Last name')}")

        # Iterate through each accommodation group
        for accommodation, students in students_by_accommodation.items():
            # Find the corresponding voucher group
            voucher_group_index = next((i for i, group_name in enumerate(voucher_group_names) if accommodation.capitalize() in group_name), None)
            if voucher_group_index is not None:
                voucher_group = all_vouchers[voucher_group_index]

                # Distribute vouchers to students in this accommodation
                for index, student_data in enumerate(students):
                    if index < len(voucher_group):
                        preferred_num = ""
                        message_type = ""
                        content_sid = ""
                        voucher_month = voucher_month.title()  # Capitalize the first letter of the month name

                        voucher_code = voucher_group[index]  # Get the voucher from the current group
                        student_name = f"{student_data['First name']} {student_data['Last name']}"
                        preferred_communication = student_data['Preferred Communication Option']

                        # Check if the voucher has already been sent
                        if student_data['Voucher Sent'] == 'Yes' and student_data['Voucher Month'] == voucher_month:
                            print(f"Skipping {student_name} - Voucher already sent.")
                            continue  # Skip to the next student

                        # Get the student's existing voucher and month
                        existing_voucher = student_data.get('Voucher Code')
                        existing_month = student_data.get('Voucher Month')

                        # Check if the student already received a voucher for the current month
                        if (existing_voucher and existing_month == voucher_month) or (existing_voucher == "0" and existing_month == voucher_month):  # Handle voucher being "0" (handled as not assigned)
                            print(f"Skipping {student_name} - Voucher already assigned for this month.")
                            continue  # Skip to the next student

                        if preferred_communication.lower() == 'whatsapp':
                            preferred_num = format_number(student_data['WhatsApp number'])
                        elif preferred_communication.lower() == 'sms':
                            preferred_num = format_number(student_data['SMS number'])

                        # Determine message type and template based on preferred communication
                        if preferred_communication == 'WhatsApp' and preferred_num:
                            content_sid = TWILIO_WHATSAPP_TEMPLATE_SID
                        elif preferred_communication == 'SMS' and preferred_num:
                            content_sid = TWILIO_SMS_TEMPLATE_SID
                        else:
                            print(f"No valid number found for preferred communication method for student {student_name}.")
                            continue

                        message_type = preferred_communication
                        content_variables = f'{{"1": "{student_name}", "2": "{voucher_month}","3": "{voucher_code}"}}'

                        # Send the message
                        if send_twilio_message(message_type, preferred_num, content_sid, content_variables, voucher_month, voucher_code, student_name):
                            print(f"{message_type} message sent successfully to {preferred_num} for {student_name}.")
                        elif message_type.lower() == "whatsapp":
                            send_twilio_message("SMS", preferred_num, content_sid, content_variables, voucher_month, voucher_code, student_name)
                    else:
                        print(f"Not enough vouchers for {accommodation}. Skipping remaining students.")
                        break  # Stop distributing vouchers for this accommodation
            else:
                print(f"No voucher group found for {accommodation}. Skipping students in this accommodation.")


def send_twilio_message(message_type, to_number, content_sid, content_variables, voucher_month, voucher_code, student_name):
    """
    Sends a Twilio message using the provided parameters.
    Polls for status update until a final status is reached.
    After successful message delivery, modifies student data in the Excel file.
    """
    if message_type.lower() == "whatsapp":
        to_number = f"whatsapp:{to_number}"

        message = client.messages.create(
                messaging_service_sid = TWILIO_MESSAGE_SID,
                content_sid = content_sid,
                content_variables = content_variables,
                to = to_number
            )
    elif message_type.lower() == "sms":
        message = client.messages.create(
            messaging_service_sid=TWILIO_MESSAGE_SID,
            body=str(TWILIO_MESSAGE_TEMPLATE).format(student_name, voucher_month, voucher_code),
            to=to_number
        )

    if check_and_handle_message_status(message, content_variables, to_number, student_name, voucher_month, voucher_code):
        return True
    else:
        handle_message_failure(message_type, to_number, content_variables, student_name, voucher_month, voucher_code)
    return False  # Message failed after retries

def send_sms_message(to_number, message):
    message = client.messages.create(
        from_=f"{FROM_SMS_NUMBER}",  # Your SMS messaging service SID
        body=message,
        to=f"{to_number}"
    )

    return message

def send_WA_message(to_number, content_variables):
    message = client.messages.create(
        from_=f"whatsapp:{FROM_WA_NUMBER}",  # Your Twilio phone number
        content_sid=TWILIO_WHATSAPP_TEMPLATE_SID,  # Your SMS messaging service SID
        content_variables=content_variables,
        to=f'whatsapp:{to_number}'
    )

    return message

def check_and_handle_message_status(message, content_variables, to_number, student_name, voucher_month, voucher_code):
    """
    Checks the status of a message and handles it accordingly.

    Args:
        message (twilio.rest.api.v2010.account.Message): The message object.
        student_name (str): The name of the student.
        voucher_month (str): The voucher month.
        voucher_password (str): The voucher password.
        to_number (str): The recipient's phone number.
        max_retries (int, optional): The maximum number of retries. Defaults to 5.

    Returns:
        bool: True if the message was successfully sent, False otherwise.
    """

    global student_records
    retry_count = 0
    max_retries = 3  # Set the maximum number of retries

    while retry_count < max_retries:
        status = check_message_status(message.sid)  # Fetch updated message details
        if status in ['queued', 'sent', 'delivered', 'read', 'sending', 'failed', 'undelivered', 'rejected']:
            if status in ['sent', 'delivered', 'read']:
                print(f"Message for {student_name} is {status}.")
                student_records = modify_student_data(voucher_month, voucher_code, to_number, student_name)
                return True  # Message successful
            elif status in ['queued', 'sending']:
                print(f"Message for {student_name} is still {status}... Moving to next student.")
                student_records = modify_student_data(voucher_month, voucher_code, to_number, student_name, sent="No")
                return True  # Message successful
            else:
                print(f"Message for {student_name} has {status}.")
                return False  # Message failed
        else:
            retry_count += 1
            print(f"Message for {student_name} is still {status}. Waiting for message status update. Retry {retry_count} of {max_retries}.")
            time.sleep(10)  # Delay for 10 seconds

    # Reached max retries, consider message failed
    print(f"Message for {student_name} failed to reach a final status within {max_retries} retries.")
    return False

def handle_message_failure(message_type, to, content_variables, student_name, voucher_month, voucher_code):
    print("Message delivery failed. Will send manually:")

    if (message_type.lower() == "whatsapp"):
        # Construct message to be sent
        message = str(TWILIO_MESSAGE_TEMPLATE).format(student_name, voucher_month, voucher_code)
        to = switch_number(message_type, student_name)
        _sid = send_sms_message(to, message)  # Send SMS message manually
        print(f"Switching {student_name}'s to {to} and sending SMS message manually.")
        check_and_handle_message_status(_sid, content_variables, to, student_name, voucher_month, voucher_code)
    elif(message_type.lower() == "sms"):
        # Construct message to be sent
        #message = str(TWILIO_MESSAGE_TEMPLATE).format(student_name, voucher_month, voucher_code)
        to = switch_number(message_type, student_name)
        print(f"Switching {student_name}'s to {to} and sending WhatsApp message manually.")
        _sid = send_WA_message(to, content_variables)  # Send WhatsApp message manually
        check_and_handle_message_status(_sid, content_variables, to, student_name, voucher_month, voucher_code)

def switch_number(message_type, student_name):
    global student_records

    # Switch the number thats used to send a message to and from whatsapp to sms or vice versa
    if message_type.lower() == "whatsapp":
        # Get the student's data based on the name
        for student in student_records:
            if student['First name'] + " " + student['Last name'] == student_name:
                # Switch the numbers
                return format_number(student['SMS number'])
    elif message_type.lower() == "sms":
        # Get the student's data based on the name
        for student in student_records:
            if student['First name'] + " " + student['Last name'] == student_name:
                # Switch the numbers
                return format_number(student['WhatsApp number'])

def check_message_status(message_sid):
    """
    Checks the status of a Twilio message.

    Args:
        message_sid: The message SID.

    Returns:
        True if the message is successfully delivered, False otherwise.
    """
    message = client.messages(message_sid).fetch()
    return message.status

def get_next_month_name():
    """
    Returns the name of the month following the current month.

    Args:
        None

    Returns:
        str: The name of the next month.

    Examples:
        >>> get_next_month_name()  # If it's currently December
        'January'
    """
    current_month = time.strftime("%B")  # Get the current month name
    month_names = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    next_month_index = (month_names.index(current_month) + 1) % 12
    return month_names[next_month_index]

def determine_month(voucher_month):
  """
  Determines the correct month and year based on the provided voucher month,
  handling the case where the input month is the same as the current month but in a future year.

  Args:
      voucher_month (str): The voucher month name (e.g., "January").

  Returns:
      tuple: A tuple containing the month name and year.

  Example:
      >>> determine_month("January")  # Assuming the current month is December 2024
      ('January', 2025)

      >>> determine_month("February")  # Assuming the current month is December 2024
      ('February', 2025)

      >>> determine_month("December")  # Assuming the current month is December 2024
      ('December', 2024)
  """
  # Get the current month and year
  current_month_name = datetime.date.today().strftime("%B")
  current_year = datetime.datetime.now().year

  # Get the numerical representation of the month
  month_num = datetime.datetime.strptime(voucher_month, "%B").month

  # Determine the year
  if voucher_month == current_month_name:
    year = current_year + (month_num > datetime.date.today().month)
  else:
    year = current_year

  return voucher_month + " " + str(year)  # Return the month name and the determined year

def match_voucher_groups(student_records, voucher_groups, voucher_month):
    """Reconciles voucher codes with student records based on month and accommodation.

    Args:
        student_records (list): List of student records.
        existing_voucher_groups (list): List of existing voucher groups (each group is a list of vouchers).
        voucher_month (str): The desired voucher month in the format "YYYY-MM" (e.g., "2024-10").

    Returns:
        tuple: A tuple containing two lists:
            - all_vouchers: List of vouchers that matched student records based on month and accommodation.
            - unmatched_vouchers: List of vouchers that did not match.
    """

    # Get unique accommodation names and construct the expected voucher names
    accommodation_names = set(student_record.get("Which accommodation do you stay at?") for student_record in student_records)
    month_name = voucher_month.split()[0]  # Get the month name in full (e.g., "October")
    month_year = voucher_month.split()[1]  # Get the year (e.g., "2024")
    desired_voucher_groups = [f"{month_name.title()} {month_year} - {accommodation.capitalize()}" for accommodation in accommodation_names]

    matching_groups = []
    for group in voucher_groups:
        for desired_group in desired_voucher_groups:
            if group['name'] == desired_group:
                matching_groups.append(group)
                break # Move to the next group after finding a match
        else:
            continue # Move to the next voucher in the group if no match was found

    return matching_groups

def match_voucher_codes(
    student_records: List[Dict],
    existing_vouchers_in_groups: List[List[str]],
    voucher_month: str
) -> Tuple[List[List[str]], List[List[str]]]:
    """
    Reconciles voucher codes with student records based on voucher codes and key student details.

    Args:
        student_records: List of student record dictionaries containing voucher information
        existing_vouchers_in_groups: List of lists containing voucher codes grouped by category
        voucher_month: Month for voucher validation

    Returns:
        tuple: Two lists of lists (unmatched_vouchers, matched_vouchers), maintaining the group structure
    """
    # Initialize result containers
    group_count = len(existing_vouchers_in_groups)
    unmatched_vouchers = [[] for _ in range(group_count)]
    matched_vouchers = [[] for _ in range(group_count)]

    # Create a set of valid voucher codes for efficient lookup
    valid_vouchers = set()  # Create an empty set
    for record in student_records:
        if record.get("Voucher Month") == voucher_month.title():
            voucher_code = record.get("Voucher Code")
            if isinstance(voucher_code, (int, float)) and not math.isnan(voucher_code):
                valid_vouchers.add(str(round(voucher_code)))
            else:
                valid_vouchers.add('0')

    # Process each voucher group
    for group_idx, voucher_group in enumerate(existing_vouchers_in_groups):
        for voucher in voucher_group:
            if voucher in valid_vouchers:
                matched_vouchers[group_idx].append(voucher)
            else:
                unmatched_vouchers[group_idx].append(voucher)

    return unmatched_vouchers, matched_vouchers

def create_voucher_groups(student_records, voucher_month, networkID, token, existing_voucher_groups):
    """Creates new voucher groups based on accommodation names from student records."""
    print("Extracting unique accommodation names...")
    accommodation_names = []
    accommodation_counts = {}  # Store counts of students per accommodation

    for row in student_records:
        accommodation = row.get("Which accommodation do you stay at?")
        if accommodation:
            # Maintain unique accommodation names:
            if accommodation not in accommodation_names:
                accommodation_names.append(accommodation)

            # Increment the count for this accommodation:
            accommodation_counts[accommodation] = accommodation_counts.get(accommodation, 0) + 1

    num_vouchers = len(accommodation_names)  # Number of voucher groups

    print(f"Creating {num_vouchers} voucher groups...")

    # Create or reuse voucher groups
    for i, accommodation_name in enumerate(accommodation_names, start=1):
        print(f"Creating voucher group {i} for '{accommodation_name}'...")
        student_count = accommodation_counts[accommodation_name]

        # Check if the group already exists
        existing_group = next((group for group in existing_voucher_groups if group['name'] == accommodation_name), None)

        if not existing_group:  # Create only if the group doesn't exist
            VoucherData = get_voucher_data(networkID, i, voucher_month, accommodation_name, existing_voucher_groups, student_count)
            if VoucherData:
                print(f"Saving voucher group {i} to the GWN...")
                new_voucher_group(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, VoucherData=VoucherData)
                print("Voucher group created successfully!")
        else:
            print(f"Voucher group for '{accommodation_name}' already exists.")

    # No need to fetch voucher groups again, use the existing_voucher_groups list
    return existing_voucher_groups

def interact_with_network():
    print("Starting network management...")

    cleanup_files()
    token = get_data_store()
    print("My token: " + token)

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

    print("Getting OneDrive access token...")
    msToken = get_access_token()

    print("Processing Excel file...")
    global student_records
    student_records = process_excel_file(msToken, FILE_NAME)

    # Get and print the list of clients
    print("Getting list of clients...")
    clients = get_client_list(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, networkID=networkID)
    if clients:
        print("Client List:")
        for client in clients:
            print(f"MAC: {client['clientId']}, Name: {client['name']}")
    else:
        print("No clients found.")

    # Match clients to student records and update usernames
    for client in clients:
        client_mac = client['clientId'].upper()  # Convert client MAC to uppercase
        for student in student_records:
            phone_mac = str(format_mac_address(student.get("Phone MAC Address", ""))).upper()
            laptop_mac = str(format_mac_address(student.get("Laptop MAC Address", ""))).upper()

            # Check the length of the MAC addresses before comparing
            if len(phone_mac) == 12 and len(laptop_mac) == 12:
                if client_mac == phone_mac or client_mac == laptop_mac:
                    first_name = str(student.get("First name", "")).split()[0]  # Get the first name only
                    last_name = student.get("Last name", "")
                    client_name = f"{first_name} {last_name}"

                    if len(client_name) > 64:
                        client_name = client_name[:64]  # Truncate username if it exceeds 64 characters
                    print(f"Updating name for MAC {client_mac} to '{client_name}'")
                    client_data = {
                        "clientId": client_mac,
                        "name": client_name
                    }
                    edit_client(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, networkID=networkID, client_data=client_data)
                    break  # Move to the next client after a match
            else:
                print(f"Skipping MAC Address comparison for {phone_mac} or {laptop_mac} - invalid length.")

    print("Client updates completed.")

def format_mac_address(mac_address):
    """
    Formats a MAC address string to a standard format (all uppercase, separated by colons).

    Args:
        mac_address (str): The MAC address string to be formatted.

    Returns:
        str: The formatted MAC address string.

    Examples:
        >>> format_mac_address("00:11:22:33:44:55")
        '00:11:22:33:44:55'

        >>> format_mac_address("00-11-22-33-44-55")
        '00:11:22:33:44:55'

        >>> format_mac_address("001122334455")
        '00:11:22:33:44:55'
    """

    mac_address = mac_address.replace("-", ":").replace(" ", "").replace(".", ":").upper()
    parts = mac_address.split(":")

    if len(parts) == 6:
        return ":".join(parts)
    else:
        return None

def send_voucher_messages():
    print("Starting voucher generation and sending...")

    cleanup_files()
    token = get_data_store()
    print("My token: " + token)

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

    # Ask for voucher month only once
    voucher_month = input("Enter the month for which you are generating vouchers (e.g., January, February): ").lower()

    print("Determining the correct month in the year to use...")
    voucher_month = determine_month(voucher_month)  # Call the determine_month function
    print("The vouch month and year to use is " + voucher_month)

    print("Getting OneDrive access token...")
    msToken = get_access_token()

    print("Downloading Excel file...")
    global student_records
    student_records = process_excel_file(msToken, FILE_NAME)
    #print(student_records[0])

    # Get existing voucher groups (names)
    all_vouchers = []
    existing_vouchers_in_groups = []
    unmatched_vouchers = []
    matched_vouchers = []
    matching_groups = []
    voucher_groups = get_voucher_group_list(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, networkID=networkID)
    voucher_group_ids = [group['id'] for group in voucher_groups]
    voucher_group_names = [group[ 'name' ] for group in voucher_groups]

    # Match voucher groups based on month and accommodation
    matching_groups = match_voucher_groups(student_records, voucher_groups, voucher_month)

    if matching_groups:
        # Fetch existing voucher groups
        for group_id in voucher_group_ids:
            for group in matching_groups:  # Iterate through each group
                if group_id == group['id']:
                    vouchers_in_group = get_voucher_list_in_group(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, groupId=group['id'], networkId=networkID)
                    existing_vouchers_in_groups.append(vouchers_in_group)
                    break  # Move to the next group_id after finding a match

        all_vouchers, matched_vouchers = match_voucher_codes(student_records, existing_vouchers_in_groups, voucher_month)

        """ # Handle unmatched vouchers
        if matched_vouchers:
            print("Found matched vouchers:")
            for voucher in matched_vouchers:
                print(f"Voucher {voucher}") """
    else:
        # Create new voucher groups if none exist
        all_vouchers = create_voucher_groups(student_records, voucher_month, networkID, token, existing_vouchers_in_groups)

    # Send an SMS or WhatsApp message for the first voucher in the first group
    if all_vouchers:  # Ensure there are voucher groups before sending a message
        send_message(all_vouchers, voucher_month, voucher_group_names)

    # Modify the Excel file and upload to OneDrive
    modify_excel_file(FILE_NAME, msToken)

if __name__ == "__main__":
    while True:
        action = input("What do you want to do? (vouchers/network/exit): ").lower()
        if action == "vouchers":
            send_voucher_messages()
        elif action == "network":
            interact_with_network()
        elif action == "exit":
            break
        else:
            print("Invalid action. Please choose 'vouchers', 'network', or 'exit'.")
