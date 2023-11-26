# GWN API Examples 

This Python script serves as a simple API client for interacting with a GWN Manager API. The script provides functions to retrieve information about networks, vouchers, SSIDs, access points (APs), and portals. It uses the `requests` library to make HTTP requests and the `dotenv` library to load environment variables securely.

## Setup

1. **Dependencies**
   - Ensure you have the required dependencies installed. You can install them using:
     ```bash
     pip install requests
     pip install python-dotenv
     ```

2. **Environment Variables**
   - Create a `.env` file in the same directory as the script and set the following environment variables:
     - `DEFAULT_URL`: The base URL for the API.
     - `ID`: Your client ID.
     - `Key`: Your client secret.

3. **Run the Script**
   - Execute the script to obtain an access token and make API requests.

## Functions

1. **`get_token(DEFAULT_URL, ID, SECRET_KEY)`**
   - Obtains an access token using client credentials.

2. **`get_network(DEFAULT_URL, Access_token, appID, appSecret)`**
   - Retrieves a list of networks.

3. **`get_network_details(DEFAULT_URL, Access_token, appID, appSecret, networkID)`**
   - Retrieves details about a specific network.

4. **`get_voucher(DEFAULT_URL, Access_token, appID, appSecret, networkID)`**
   - Retrieves a list of vouchers for a specific network.

5. **`get_ssid(DEFAULT_URL, Access_token, appID, appSecret, networkID)`**
   - Retrieves a list of SSIDs for a specific network.

6. **`get_ap(DEFAULT_URL, Access_token, appID, appSecret, networkID)`**
   - Retrieves a list of access points (APs) for a specific network.

7. **`get_portals(DEFAULT_URL, Access_token, appID, appSecret, networkID)`**
   - Retrieves a list of portals for a specific network.


## Example

```python
# Load environment variables and obtain access token
key = get_token(DEFAULT_URL=DEFAULT_ENV, ID=ID_ENV, SECRET_KEY=SECRET_KEY_ENV)

# Example: Get a list of portals for network ID 1
get_portals(Access_token=key, appID=ID_ENV, appSecret=SECRET_KEY_ENV, DEFAULT_URL=DEFAULT_ENV, networkID=1)
