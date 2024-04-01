import requests
import os
import json
from dotenv import load_dotenv
from hashlib import sha256
import time
from pprint import pprint
from twilio.rest import Client

load_dotenv()

DEFAULT_ENV = os.getenv("DEFAULT_URL")
ID_ENV = os.getenv("ID")
SECRET_KEY_ENV = os.getenv("Key")
ACCESS_TOKEN_ENV = os.getenv("Access_token")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_SMS_number = os.getenv("TWILIO_PHONE_NUMBER")
from_WA_number = os.getenv("TWILIO_WHATSAPP_NO")

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

    debug(ljson(network_response.text)['data'])

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

    debug(network_response.url)
    debug(ljson(network_response.text))

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
            if time.time() - data['timestamp'] < 3600:  # Check if network_id is less than 1 hour old
                return data['network_id']
    return None

def cleanup_files():
    if os.path.exists('token_store.txt'):
        with open('token_store.txt', 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] >= 3600:  # Check if token is more than 1 hour old
                os.remove('token_store.txt')
    if os.path.exists('network_store.txt'):
        with open('network_store.txt', 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] >= 3600:  # Check if network_id is more than 1 hour old
                os.remove('network_store.txt')

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

def send_sms_message(to_number, voucher_password):
    body_message = f'Hi Sebanebane Wa Kae-Kae, Your WIFI voucher password is:  + {voucher_password}'

    message = client.messages.create(
                    body = body_message,
                    from_ = from_SMS_number,
                    to = to_number
                )

    return message.sid

def send_WA_message(to_number, voucher_password):
    body_message = f'Hi Sebanebane Wa Kae-Kae, Your WIFI voucher password is:  + {voucher_password}'

    message = client.messages.create(
        from_=from_WA_number,
        body=body_message,
        to=f'whatsapp:{to_number}'
    )

    print(message.sid)

def interact_with_network():
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
        VoucherData = get_voucher_data(networkID, i+1)
        debug(VoucherData)
        new_voucher_group(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, VoucherData=VoucherData)

    # Get all the voucher groups
    voucher_group_ids = get_voucher_group_list(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, networkID=networkID)
    
    # Find the list of vouchers per group and save each group's vouchers into a multi-array list
    all_vouchers = []
    for group_id in voucher_group_ids:
        vouchers_in_group = get_voucher_list_in_group(DEFAULT_URL=DEFAULT_ENV, Access_token=token, appID=ID_ENV, appSecret=SECRET_KEY_ENV, groupId=group_id, networkId=networkID)
        all_vouchers.append(vouchers_in_group)

    # Print all the vouchers
    for group_vouchers in all_vouchers:
        print(group_vouchers)

    # Send SMS or WhatsApp message for the first voucher in the first group
    to_number = input("Enter the phone number to send the voucher to: ")
    message_type = input("Enter the type of message to send (SMS or WhatsApp): ")
    if all_vouchers:
        first_group_vouchers = all_vouchers[0]
        if first_group_vouchers:
            first_voucher = first_group_vouchers[0]
            voucher_password = first_voucher  # Replace this with the actual password extraction logic
            if message_type.lower() == "sms":
                send_sms_message(to_number, voucher_password)
            elif message_type.lower() == "whatsapp":
                send_WA_message(to_number, voucher_password)
            else:
                print("Invalid message type. Please enter either 'SMS' or 'WhatsApp'.")

    return all_vouchers

interact_with_network()