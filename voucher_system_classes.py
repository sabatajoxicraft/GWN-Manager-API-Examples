# voucher_system_classes.py
import os
import requests
import json
import time
import datetime
from hashlib import sha256
from dotenv import load_dotenv
from twilio.rest import Client

from network import *
from utils import *
from messaging import *

load_dotenv()  # Load environment variables from .env file


+# Constants from your config.py
DEFAULT_ENV = os.getenv("DEFAULT_URL")
ID_ENV = os.getenv("ID")
SECRET_KEY_ENV = os.getenv("Key")
ACCESS_TOKEN_ENV = os.getenv("Access_token")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
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

client = Client(ACCOUNT_SID, AUTH_TOKEN)

class APIRequest:
    def __init__(self, default_url, app_id, app_secret, access_token):
        self.default_url = default_url
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token

    def _build_payload(self, body_data):
        timestamp = round(time.time() * 1000)
        public_params = {
            'access_token': self.access_token,
            'appID': self.app_id,
            'secretKey': self.app_secret,
            'timestamp': timestamp
        }

        params = "&".join([f"{key}={public_params[key]}" for key in public_params])
        body = json.dumps(body_data, separators=(',', ':'))

        body_signature = sha256(body.encode()).hexdigest()
        signature = sha256(f"&{params}&{body_signature}&".encode()).hexdigest()

        payload_data = {
            'access_token': self.access_token,
            'appID': self.app_id,
            'timestamp': timestamp,
            'signature': signature
        }

        payload = "&".join([f"{key}={payload_data[key]}" for key in payload_data])
        return payload

    def post(self, endpoint, body_data):
        payload = self._build_payload(body_data)
        url = f"{self.default_url}{endpoint}"
        response = requests.post(url + "?" + payload, data=body, headers={'Content-type': 'application/json'}, timeout=30)
        return response

    def get(self, endpoint, body_data=None):
        payload = self._build_payload(body_data) if body_data else ""
        url = f"{self.default_url}{endpoint}"
        response = requests.get(url + "?" + payload, headers={'Content-type': 'application/json'}, timeout=30)
        return response
    
    def get_token(self, DEFAULT_URL, ID, SECRET_KEY):
        Data = {
            "grant_type" : "client_credentials",
            "client_id" : ID,
            "client_secret" : SECRET_KEY
        }
        r = requests.get(DEFAULT_URL + "/oauth/token", params=Data)
        res = json.loads(r.text) 
        
        return res["access_token"]

    def get_access_token(self):
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
        
    def get_network_id(self, DEFAULT_URL, Access_token, appID, appSecret, NetworkName):
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
    
    def get_ap(self, DEFAULT_URL, Access_token, appID, appSecret, networkID):
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
        
class Network:
    def __init__(self, network_id, network_name, default_url, app_id, app_secret, access_token):
        self.network_id = network_id
        self.network_name = network_name
        self.default_url = default_url
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.api_request = APIRequest(self.default_url, self.app_id, self.app_secret, self.access_token)

    def get_network_details(self):
        endpoint = "/oapi/v1.0.0/network/detail"
        body_data = {"id": self.network_id}  # Pass the network ID
        response = self.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            print(f"Error getting network details: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return None

    def get_voucher_group_list(self):
        endpoint = "/oapi/v1.0.0/voucher/list"
        body_data = {
            "search": "",
            "order": "name",
            "pageNum": 1,
            "pageSize": 10,
            "networkId": self.network_id  # Pass the network ID
        }
        response = self.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            return response.json()["data"]["result"]
        else:
            print(f"Error getting voucher group list: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return None

    def create_voucher_group(self, voucher_data):
        endpoint = "/oapi/v1.0.0/voucher/save"
        response = self.api_request.post(endpoint, voucher_data)
        if response.status_code == 200:
            print("Voucher group created successfully!")
            print(response.text)
            return True  # Or return the group ID if needed
        else:
            print(f"Error creating voucher group: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return False

    def get_voucher_list_in_group(self, group_id):
        endpoint = "/oapi/v1.0.0/voucher/vouchers/list"
        body_data = {
            "search": "",
            "order": "",
            "type": "",
            "pageNum": 1,
            "pageSize": 100,
            "filter": {
                "state": ""
            },
            "groupId": group_id,
            "networkId": self.network_id  # Pass the network ID
        }
        response = self.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            voucher_list = response.json()["data"]["result"]
            voucher_password = [voucher['password'] for voucher in voucher_list]
            return voucher_password
        else:
            print(f"Error getting vouchers in group: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return None

    def get_ssid(self):
        endpoint = "/oapi/v1.0.0/ssid/list"
        body_data = {
            "search": "",
            "order": "name",
            "pageNum": 1,
            "pageSize": 10,
            "networkId": self.network_id 
        }
        response = self.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            return response.json()["data"]["result"]
        else:
            print(f"Error getting SSID list: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return None

    def get_ap(self):
        endpoint = "/oapi/v1.0.0/ap/list"
        body_data = {
            "search": "",
            "order": "name",
            "pageNum": 1,
            "pageSize": 10,
            "networkId": self.network_id 
        }
        response = self.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            return response.json()["data"]["result"]
        else:
            print(f"Error getting AP list: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return None

    def get_portals(self):
        endpoint = "/oapi/v1.0.0/portal/list"
        body_data = {"networkId": self.network_id}
        response = self.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            print(f"Error getting portal list: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return None

class VoucherGroup:
    def __init__(self, group_id, group_name, network):
        self.group_id = group_id
        self.group_name = group_name
        self.network = network

    def get_voucher_list(self):
        endpoint = "/oapi/v1.0.0/voucher/vouchers/list"
        body_data = {
            "search": "",
            "order": "",
            "type": "",
            "pageNum": 1,
            "pageSize": 100,
            "filter": {
                "state": ""
            },
            "groupId": self.group_id,
            "networkId": self.network.network_id
        }
        response = self.network.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            voucher_list = response.json()["data"]["result"]
            voucher_passwords = [voucher['password'] for voucher in voucher_list]
            return voucher_passwords
        else:
            print(f"Error getting vouchers in group: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return None

class Voucher:
    def __init__(self, voucher_id, password, network, group):
        self.voucher_id = voucher_id
        self.password = password
        self.network = network
        self.group = group

    def get_voucher_details(self):
        endpoint = "/oapi/v1.0.0/voucher/vouchers/detail"
        body_data = {
            "id": self.voucher_id,
            "networkId": self.network.network_id  # Pass the network ID
        }
        response = self.network.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            print(f"Error getting voucher details: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return None

    def update_voucher(self, update_data):
        endpoint = "/oapi/v1.0.0/voucher/vouchers/update"
        update_data["id"] = self.voucher_id
        update_data["networkId"] = self.network.network_id
        response = self.network.api_request.post(endpoint, update_data)
        if response.status_code == 200:
            print("Voucher updated successfully!")
            return True  # Or return the updated voucher data if needed
        else:
            print(f"Error updating voucher: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return False

    def delete_voucher(self):
        endpoint = "/oapi/v1.0.0/voucher/vouchers/delete"
        body_data = {
            "id": self.voucher_id,
            "networkId": self.network.network_id  # Pass the network ID
        }
        response = self.network.api_request.post(endpoint, body_data)
        if response.status_code == 200:
            print("Voucher deleted successfully!")
            return True
        else:
            print(f"Error deleting voucher: Status Code: {response.status_code}")
            print("Response Content:", response.text)
            return False

class Student:
    def __init__(self, student_data, network):
        self.student_data = student_data
        self.network = network

    def get_voucher_code(self):
        """Retrieves the voucher code associated with the student, if available."""
        return self.student_data.get("Voucher Code")

    def get_voucher_month(self):
        """Retrieves the voucher month associated with the student, if available."""
        return self.student_data.get("Voucher Month")

    def has_voucher(self):
        """Checks if the student has a voucher associated with them."""
        return self.get_voucher_code() is not None and self.get_voucher_month() is not None

    def send_voucher(self, voucher_password, voucher_month):
        """Sends a voucher code to the student via their preferred communication method."""
        preferred_communication = self.student_data['Preferred Communication Option']
        preferred_num = None

        if preferred_communication.lower() == 'whatsapp':
            preferred_num = format_number(self.student_data['WhatsApp number'])
        elif preferred_communication.lower() == 'sms':
            preferred_num = format_number(self.student_data['SMS number'])

        if preferred_num:
            content_sid = TWILIO_WHATSAPP_TEMPLATE_SID if preferred_communication == 'WhatsApp' else TWILIO_SMS_TEMPLATE_SID
            student_name = f"{self.student_data['First name']} {self.student_data['Last name']}"
            content_variables = f'{{"1": "{student_name}", "2": "{voucher_month}","3": "{voucher_password}"}}'
            if send_twilio_message(preferred_communication, preferred_num, content_sid, content_variables, voucher_month, voucher_password, student_name):
                print(f"{preferred_communication} message sent successfully to {preferred_num} for {student_name}.")
                self.student_data['Voucher Code'] = voucher_password
                self.student_data['Voucher Month'] = voucher_month
                self.student_data['Voucher Sent'] = "Yes"
                return True
            else:
                handle_message_failure(preferred_communication, preferred_num, content_variables, student_name, voucher_month, voucher_password)
                return False
        else:
            print(f"No valid number found for preferred communication method for student {student_name}.")
            return False

class Utils:
    @staticmethod
    def load_token():
        if os.path.exists('token_store.txt'):
            with open('token_store.txt', 'r') as f:
                data = json.load(f)
                if time.time() - data['timestamp'] < 300:  # Check if token is less than 15 minutes old
                    return data['token']
        return None
    
    @staticmethod
    def store_token(token):
        with open('token_store.txt', 'w') as f:
            json.dump({'token': token, 'timestamp': time.time()}, f)
    
    @staticmethod
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

    @staticmethod
    def load_network_id():
        if os.path.exists('network_store.txt'):
            with open('network_store.txt', 'r') as f:
                data = json.load(f)
                if time.time() - data['timestamp'] < 3600:  # Check if network_store is less than 1 hour old
                    return data['network_id']
        return None

    @staticmethod
    def store_network_id(network_id):
        with open('network_store.txt', 'w') as f:
            json.dump({'network_id': network_id, 'timestamp': time.time()}, f)

    @staticmethod
    def cleanup_files():
        if FILE_NAME is not None and os.path.exists(FILE_NAME):
            file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(FILE_NAME))
            one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)

            if file_modified_time < one_hour_ago:  # Check if file is older than 1 hour
                os.remove(FILE_NAME)  # Remove the file

    @staticmethod
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