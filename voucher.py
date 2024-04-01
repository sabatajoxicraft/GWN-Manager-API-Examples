import requests
import json
from hashlib import sha256
import time

from utils import ljson, debug  

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