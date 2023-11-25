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

def create_signature(Access_token, param, appID, clientID):
    timestamp = int(time.time() * 1000)
    prebody = json.dumps(body_data, separators=(',', ':')).encode('utf-8')
    body = hashlib.sha256(prebody).hexdigest()
    signature_string = f"&access_token={Access_token}&appID={clientID}&timestamp={timestamp}&{body}&"
    signature = hashlib.sha256(signature_string.encode("utf-8")).hexdigest()
    return signature, timestamp


def get_network(DEFAULT_URL, Access_token, appID, clientID):
    param = {
        "type": "asc",
        "order": "id",
        "search": "",
        "pageNum": 1,
        "pageSize": 5
    }
    debug(param)
    
    signatur, timestamp = create_signature(Access_token=Access_token, appID=appID, clientID=clientID, param=param)
    
    URL = DEFAULT_URL + f"/oapi/v1.0.0/network/list?access_token={Access_token}&appID={appID}&timestamp={timestamp}&signature={signatur}"
    headers = { 'Content-type': 'application/json'}
    
    debug(URL)
    r = requests.get(url=URL, params=param,  headers=headers)
    
    debug(ljson(r.text))
    
    
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

get_network(DEFAULT_URL=DEFAULT_ENV, Access_token=key, appID=ID_ENV, clientID=ID_ENV)
