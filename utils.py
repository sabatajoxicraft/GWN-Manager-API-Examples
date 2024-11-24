import json
import os
from pprint import pprint
import time

from config import DEFAULT_ENV, ID_ENV, SECRET_KEY_ENV
from network import get_token

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
