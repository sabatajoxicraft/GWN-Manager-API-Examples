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

load_dotenv()

DEFAULT_ENV = os.getenv("DEFAULT_URL")
ID_ENV = os.getenv("ID")
SECRET_KEY_ENV = os.getenv("Key")
ACCESS_TOKEN_ENV = os.getenv("Access_token")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_SMS_number = os.getenv("TWILIO_PHONE_NUMBER")
from_WA_number = os.getenv("TWILIO_WHATSAPP_NO")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
FILE_ID = os.getenv("FILE_ID")
FILE_NAME = os.getenv("FILE_NAME")
AUTHORITY_URL = os.getenv("AUTHORITY_URL")
TENANT_ID = os.getenv("TENANT_ID")

client = Client(account_sid, auth_token)

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

    voucher_groups = ljson(network_response.text)['data']['result']
    voucher_group_ids = [group['id'] for group in voucher_groups]
    return voucher_group_ids

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
    timestamp = round(time.time() * 1000)
    public_params = {
        'access_token': Access_token,
        'appID': appID,
        'secretKey': appSecret,
        'timestamp': timestamp
    }
        
    body_data = {
        "networkId": VoucherData["networkId"],
        "name": VoucherData["voucherName"],
        "vocherNum": VoucherData["vocherNum"],
        "deviceNum": VoucherData["deviceNum"],
        "expiration": VoucherData["expiration"],
        "effectDurationMap": {
            "d": VoucherData["effectDurationMap_d"],
            "h": VoucherData["effectDurationMap_h"],
            "m": VoucherData["effectDurationMap_m"]
        },
        "description": VoucherData["description"]
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
    
    network_url = f'{DEFAULT_URL}/oapi/v1.0.0/voucher/save'
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)

    # debug(network_response.url)
    # debug(ljson(network_response.text))

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
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] >= 3600:  # Check if FILE_NAME is more than 1 hour old
                os.remove(FILE_NAME)

def get_voucher_data(networkID, voucher_group_number):
    voucherName = input(f"Enter the voucher {voucher_group_number} group name: ")
    vocherNum = int(input(f"Enter the number of vouchers for group {voucher_group_number}: "))
    deviceNum = int(input(f"Enter the max devices number in each voucher for group {voucher_group_number} (0 means no limit): "))
    expiration = int(input(f"Enter the validity time (day) for group {voucher_group_number}: "))
    effectDurationMap_d = input(f"Enter the effect duration in day (0-365) for group {voucher_group_number}: ")
    effectDurationMap_h = input(f"Enter the effect duration in hour (0-23) for group {voucher_group_number}: ")
    effectDurationMap_m = input(f"Enter the effect duration in minute (0-59) for group {voucher_group_number}: ")
    description = input(f"Enter the description for group {voucher_group_number}: ")
    VoucherData = {
        "networkId": networkID,
        "voucherName": voucherName,
        "vocherNum": vocherNum,
        "deviceNum": deviceNum,
        "expiration": expiration,
        "effectDurationMap_d": effectDurationMap_d,
        "effectDurationMap_h": effectDurationMap_h,
        "effectDurationMap_m": effectDurationMap_m,
        "description": description
    }
    return VoucherData

def send_sms_message(to_number, message):
    message = client.messages.create(
                    body = message,
                    from_ = from_SMS_number,
                    to = to_number
                )

    if message.sid:
        print("SMS: " + message.sid)
        return True
    else:
        return False

def send_WA_message(to_number, message):
    message = client.messages.create(
        from_=from_WA_number,
        body=message,
        to=f'whatsapp:{to_number}'
    )

    if message.sid:
        print("WA: " + message.sid)
        return True
    else:
        return False

def read_excel_columns(filename):
    df = pd.read_excel(filename, usecols=None)
    return df.to_dict(orient='records')

def modify_excel_file(FILE_NAME, column_data, all_vouchers):
    """
    Modifies an Excel file by updating specific columns with provided data.

    Args:
        FILE_NAME (str): The path of the Excel file to be modified.
        column_data (list): A list of data to be updated in the Excel file.
        all_vouchers (list): A list of voucher codes corresponding to each data item.

    Returns:
        None
    """

    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(FILE_NAME)

    # Iterate over each student's data and update the corresponding row
    for index, row in enumerate(column_data):
        voucher_code = None
        if all_vouchers and index < len(all_vouchers[0]):
            voucher_code = all_vouchers[0][index]

        # Update the "Voucher Sent" column to "Yes"
        df.at[index, 'Voucher Sent'] = 'Yes'

        # Update the "Voucher Code" column with the corresponding voucher code
        if voucher_code:
            df.at[index, 'Voucher Code'] = voucher_code

    # Save the modified DataFrame back to the Excel file
    df.to_excel(FILE_NAME, index=False)

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
    if len(number) == 10 and number.startswith('0'):
        return '+27' + number[1:]
    elif len(number) == 9:
        return '+27' + number
    else:
        return number

def process_excel_file(token, FILE_ID, FILE_NAME, all_vouchers):
    """
    Process an Excel file by downloading it from OneDrive, reading specific columns,
    modifying the file, and returning the column data.

    Parameters:
    - token (str): The access token for OneDrive authentication.
    - FILE_ID (str): The ID of the Excel file on OneDrive.
    - FILE_NAME (str): The local file path to save the downloaded Excel file.
    - all_vouchers (list): A list of vouchers to be used for modifying the Excel file.

    Returns:
    - column_data (dict): A dictionary containing the data from specific columns of the Excel file.
    """
    # Initialize OneDrive
    drive = OneDrive(token)

    # Download the Excel file from OneDrive
    # if you know the item ID
    drive.download_item(item_id=FILE_ID, file_path=FILE_NAME) 

    # Read specific columns from the Excel file
    column_data = read_excel_columns(FILE_NAME)

    # Modify the Excel file
    modify_excel_file(FILE_NAME, column_data, all_vouchers)

    return column_data

def send_message(all_vouchers, column_data):
    """
    Sends an SMS or WhatsApp message for each voucher in the first group based on the preferred communication option.

    Args:
        all_vouchers (list): A multi-array list containing all the vouchers in the network.
        column_data (dict): A dictionary containing the data from specific columns of the Excel file.

    Returns:
        None
    """
    # Send SMS or WhatsApp message for each voucher in the first group
    if all_vouchers and column_data:
        first_group_vouchers = all_vouchers[0]
        for index, student_data in enumerate(column_data):
            if index < len(first_group_vouchers):
                voucher = first_group_vouchers[index]
                voucher_password = voucher  # Replace this with the actual password extraction logic
                student_name = f"{student_data['First name']} {student_data['Last name']}"  # Get the student name
                whatsapp_number = format_number(student_data['WhatsApp number'])
                sms_number = format_number(student_data['SMS number'])
                preferred_communication = student_data['Preferred Communication Option'].lower()

                if preferred_communication == 'WhatsApp' and whatsapp_number:  # If WhatsApp number is present
                    to_number = whatsapp_number
                    message_type = "WhatsApp"
                elif preferred_communication == 'SMS' and sms_number:  # If SMS number is present
                    to_number = sms_number
                    message_type = "SMS"
                else:
                    print(f"No valid number found for preferred communication method for student {student_name}.")
                    continue

                message = f"Hello {student_name}, your voucher password is {voucher_password}. Enjoy your internet access!"

                if message_type.lower() == "sms":
                    if send_sms_message(to_number, message):
                        print("SMS sent to: " + to_number)
                    else:
                        print("Failed to send SMS to: " + to_number)
                elif message_type.lower() == "whatsapp":
                    if send_WA_message(to_number, message):
                        print("Whatsapp sent to: " + to_number)
                    else:
                        print("Failed to send Whatsapp to: " + to_number)

                
def interact_with_network():
    """
    Interacts with a network by performing various operations such as creating voucher groups,
    retrieving voucher information, processing an Excel file, and sending SMS or WhatsApp messages.

    Returns:
        all_vouchers (list): A multi-array list containing all the vouchers in the network.
    """
    cleanup_files()  # Call cleanup_files at the start of the function
    token = get_data_store()
    print("My token: " + token)
    
    # Get the list of network names
    network_names = get_network_list_names(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV)
    print("Available networks: ", ', '.join(network_names))
    
    network_name = input("Enter the network name you want to interact with: ")
    if network_name not in network_names:
        print("Invalid network name. Please enter a valid network name.")
        return
    
    networkID = get_network_id(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, NetworkName=network_name)
    store_network_id(networkID)  # Store the network ID after getting it

    # Create my vouchers
    num_vouchers = int(input("Enter the number of voucher groups you want to create: "))
    for i in range(num_vouchers):
        VoucherData = get_voucher_data(networkID, i + 1)
        # debug(VoucherData)
        new_voucher_group(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, VoucherData=VoucherData)

    # Get all the voucher groups
    voucher_group_ids = get_voucher_group_list(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, networkID=networkID)
    
    # Find the list of vouchers per group and save each group's vouchers into a multi-array list
    all_vouchers = []
    for group_id in voucher_group_ids:
        vouchers_in_group = get_voucher_list_in_group(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, groupId=group_id, networkId=networkID)
        all_vouchers.append(vouchers_in_group)

    # Print all the vouchers
    #for group_vouchers in all_vouchers:
    #     print(group_vouchers)

    column_data = process_excel_file(token, FILE_ID, FILE_NAME, all_vouchers)

    # Send an SMS or WhatsApp message for the first voucher in the first group
    send_message(all_vouchers, column_data)  

interact_with_network()