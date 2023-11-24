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

def create_signature(Access_token, param, appID):
    timestamp = int(time.time() * 1000)
    body = sha256(json.dumps(param).encode("utf-8")).hexdigest()
    signatur_string = f"&access_token={Access_token}&appID={appID}&timestamp={timestamp}&{body}&"
    signature = sha256(signatur_string.encode("utf-8")).hexdigest()

    print(f"Signature String: {signatur_string}")
    print(f"Calculated Signature: {signature}")
    print(f"Timestamp: {timestamp}")

    return signature, timestamp


def get_network(DEFAULT_URL, Access_token, appID):
    param = {
        "type": "asc",
        "order": "id",
        "search": "",
        "pageNum": 1,
        "pageSize": 5
    }
    
    signatur, timestamp = create_signature(Access_token=Access_token, appID=appID, param=param)
    
    URL = DEFAULT_URL + f"/oapi/v1.0.0/network/list?access_token={Access_token}&appID={appID}&timestamp={timestamp}&signature={signatur}"
    headers = { 'Content-type': 'application/json'}
    
    print(URL)
    r = requests.get(url=URL, params=param,  headers=headers)

    pprint(ljson(r.text))
    
    
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
    print(URL)
    r = requests.post(url=URL, params=param,  headers=headers)
    pprint(r.json)
    
    
def ljson(input):
    json_return = json.loads(input)
    return json_return

key = get_token(DEFAULT_URL=DEFAULT_ENV, ID=ID_ENV, SECRET_KEY=SECRET_KEY_ENV)

get_network(DEFAULT_URL=DEFAULT_ENV, Access_token=key, appID=ID_ENV)
