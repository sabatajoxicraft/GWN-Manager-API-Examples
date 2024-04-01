from config import DEFAULT_ENV, ID_ENV, SECRET_KEY_ENV 
from message import send_WA_message, send_sms_message 
from network import get_network_id, get_network_list_names  
from utils import cleanup_files, debug, get_data_store, store_network_id  
from voucher import get_voucher_data, get_voucher_group_list, get_voucher_list_in_group, new_voucher_group 

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