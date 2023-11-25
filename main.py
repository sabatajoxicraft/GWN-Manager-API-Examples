import requests
import os
import json
from dotenv import load_dotenv
from hashlib import sha256
import time
from pprint import pprint
load_dotenv()

DEFAULT_ENV = os.getenv("DEFAULT_URL")
ID_ENV = os.getenv("ID")
SECRET_KEY_ENV = os.getenv("Key")

def get_token(DEFAULT_URL, ID, SECRET_KEY):
    Data = {
        "grant_type" : "client_credentials",
        "client_id" : ID,
        "client_secret" : SECRET_KEY
    }
    r = requests.get(DEFAULT_URL + "/oauth/token", params=Data)
    res = json.loads(r.text) 
    
    return res["access_token"]

def get_network(DEFAULT_URL, Access_token, appID, appSecret):
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
    network_response = requests.post(network_url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, verify=False, timeout=30)

    debug(ljson(network_response.text))
    
    
def get_voucher(DEFAULT_URL, Access_token, appID, networkID):
    param = {
     "search": "",
     "order": "",
     "pageNum": 1,
     "pageSize": 10,
     "networkId": networkID
    }
    
    signatur, timestamp = create_signature(Access_token=Access_token, appID=appID, param=param)
    URL = DEFAULT_URL + f"oapi/v1.0.0/voucher/list?&appID={appID}&timestamp={timestamp}&signatur={signatur}"
    headers = { 'Content-type': 'application/json'}
    debug(URL)
    r = requests.post(url=URL, params=param,  headers=headers)
    debug(r.json)
    
    
def ljson(input):
    json_return = json.loads(input)
    return json_return


def debug(input):
    pprint(input)
    print("")

key = get_token(DEFAULT_URL=DEFAULT_ENV, ID=ID_ENV, SECRET_KEY=SECRET_KEY_ENV)

get_network(DEFAULT_URL=DEFAULT_ENV, Access_token=key, appID=ID_ENV, appSecret=SECRET_KEY_ENV)
