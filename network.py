import requests
import json
from hashlib import sha256
import time

from utils import ljson 

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
