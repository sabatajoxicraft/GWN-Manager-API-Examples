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

The interact_with_network function in your code performs several operations related to network interaction. Here’s a high-level overview of what it does:

It first cleans up any old token and network ID files that are more than an hour old.
It retrieves an access token, either from a stored file or by making a request to get a new one.
It fetches the list of available network names.
It prompts the user to enter the name of the network they want to interact with.
It retrieves the ID of the specified network.
It prompts the user to specify the number of voucher groups they want to create and collects necessary details for each group.
It creates the specified number of voucher groups.
It retrieves the list of all voucher groups.
For each voucher group, it retrieves the list of vouchers and appends them to a list.
Finally, it returns the list of all vouchers.
This function allows you to interact with a specified network, create voucher groups, and retrieve information about vouchers within those groups. The returned list of vouchers can then be used for further operations as needed. Please note that this function involves user interaction for inputting network and voucher details.

The function get_voucher_group_list is used to get the list of voucher groups in a network. It makes a POST request to the /oapi/v1.0.0/voucher/list endpoint with the necessary parameters and returns the IDs of the voucher groups.

The function get_voucher_list_in_group is used to get the list of vouchers in a specific voucher group. It makes a POST request to the /oapi/v1.0.0/voucher/vouchers/list endpoint with the necessary parameters and returns the IDs of the vouchers in the group.

These functions are part of a larger process of interacting with the network, creating voucher groups, and retrieving voucher information. They are used within the interact_with_network function.

Please let me know if you need more information about any other part of the code.