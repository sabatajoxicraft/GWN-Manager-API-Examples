# create a Messaging class
# messaging.py

import os
import time

from utils import format_number
from voucher_system_classes import FROM_SMS_NUMBER, FROM_WA_NUMBER, TWILIO_MESSAGE_SID, TWILIO_MESSAGE_TEMPLATE, TWILIO_SMS_TEMPLATE_SID, TWILIO_WHATSAPP_TEMPLATE_SID

class messaging:
    def __init__(self, sender, recipient, message):
        self.sender = sender
        self.recipient = recipient
        self.message = message

    def send_message(self, all_vouchers, voucher_month):
        """
        Sends an SMS or WhatsApp message for each voucher in the first group based on the preferred communication option.
        If WhatsApp fails, falls back to SMS using the same message structure.
        """
        global student_records

        if all_vouchers and student_records:
            first_group_vouchers = all_vouchers[0]
            for index, student_data in enumerate(student_records):
                if index < len(first_group_vouchers):
                    preferred_num = ""
                    message_type = ""
                    content_sid = ""
                    voucher_month = voucher_month.title()  # Capitalize the first letter of the month name

                    voucher = first_group_vouchers[index]
                    voucher_password = voucher  # Replace this with the actual password extraction logic
                    student_name = f"{student_data['First name']} {student_data['Last name']}"  # Get the student name
                    preferred_communication = student_data['Preferred Communication Option']

                    # Check if the voucher has already been sent
                    if student_data['Voucher Sent'] == 'Yes':
                        print(f"Skipping {student_name} - Voucher already sent.")
                        continue  # Skip to the next student

                    if preferred_communication.lower() == 'whatsapp':
                        preferred_num = format_number(student_data['WhatsApp number'])
                    elif preferred_communication.lower() == 'sms':
                        preferred_num = format_number(student_data['SMS number'])

                    # Determine message type and template based on preferred communication
                    if preferred_communication == 'WhatsApp' and preferred_num:
                        content_sid = TWILIO_WHATSAPP_TEMPLATE_SID
                    elif preferred_communication == 'SMS' and preferred_num:
                        content_sid = TWILIO_SMS_TEMPLATE_SID
                    else:
                        print(f"No valid number found for preferred communication method for student {student_name}.")
                        continue

                    #next_month = get_next_month_name()  # Get the next month name
                    message_type = preferred_communication
                    content_variables = f'{{"1": "{student_name}", "2": "{voucher_month}","3": "{voucher_password}"}}'

                    # Send the message
                    if self.send_twilio_message(message_type, preferred_num, content_sid, content_variables, voucher_month, voucher_password, student_name):
                            print(f"{message_type} message sent successfully to {preferred_num} for {student_name}.")
                    elif message_type.lower() == "whatsapp":
                        self.send_twilio_message("SMS", preferred_num, content_sid, content_variables, voucher_month, voucher_password, student_name)                        

    def send_twilio_message(self, message_type, to_number, content_sid, content_variables, voucher_month, voucher_password, student_name):
        """
        Sends a Twilio message using the provided parameters.
        Polls for status update until a final status is reached.
        After successful message delivery, modifies student data in the Excel file.
        """
        if message_type.lower() == "whatsapp":
            to_number = f"whatsapp:{to_number}"

            message = client.messages.create(
                    messaging_service_sid = TWILIO_MESSAGE_SID,
                    content_sid = content_sid,
                    content_variables = content_variables,
                    to = to_number
                ) 
        elif message_type.lower() == "sms":
            message = client.messages.create(
                messaging_service_sid=TWILIO_MESSAGE_SID,
                body=str(TWILIO_MESSAGE_TEMPLATE).format(student_name, voucher_month, voucher_password),
                to=to_number
            )

        if self.check_and_handle_message_status(message, content_variables, to_number, student_name, voucher_month, voucher_password):
            return True
        else: 
            self.handle_message_failure(message_type, to_number, content_variables, student_name, voucher_month, voucher_password)
        return False  # Message failed after retries

    def send_sms_message(self, to_number, message):
        message = client.messages.create(
            from_=f"{FROM_SMS_NUMBER}",  # Your SMS messaging service SID
            body=message,
            to=f"{to_number}"
        )

        return message

    def send_WA_message(self, to_number, content_variables):
        message = client.messages.create(
            from_=f"whatsapp:{FROM_WA_NUMBER}",  # Your Twilio phone number
            content_sid=TWILIO_WHATSAPP_TEMPLATE_SID,  # Your SMS messaging service SID
            content_variables=content_variables,
            to=f'whatsapp:{to_number}'
        )

        return message

    def check_and_handle_message_status(self, message, content_variables, to_number, student_name, voucher_month, voucher_password):
        """
        Checks the status of a message and handles it accordingly.

        Args:
            message (twilio.rest.api.v2010.account.Message): The message object.
            student_name (str): The name of the student.
            voucher_month (str): The voucher month.
            voucher_password (str): The voucher password.
            to_number (str): The recipient's phone number.
            max_retries (int, optional): The maximum number of retries. Defaults to 5.

        Returns:
            bool: True if the message was successfully sent, False otherwise.
        """

        global student_records
        retry_count = 0
        max_retries = 3  # Set the maximum number of retries

        while retry_count < max_retries:
            status = self.check_message_status(message.sid)  # Fetch updated message details
            if status in ['queued', 'sent', 'delivered', 'read', 'sending', 'failed', 'undelivered', 'rejected']:
                if status in ['sent', 'delivered', 'read']:
                    print(f"Message for {student_name} is {status}.")
                    student_records = modify_student_data(voucher_month, voucher_password, to_number, student_name)
                    return True  # Message successful
                elif status in ['queued', 'sending']:
                    print(f"Message for {student_name} is still {status}... Moving to next student.")
                    student_records = modify_student_data(voucher_month, voucher_password, to_number, student_name, sent="No")
                    return True  # Message successful
                else:
                    print(f"Message for {student_name} has {status}.")
                    return False  # Message failed
            else:
                retry_count += 1
                print(f"Message for {student_name} is still {status}. Waiting for message status update. Retry {retry_count} of {max_retries}.")
                time.sleep(10)  # Delay for 10 seconds

        # Reached max retries, consider message failed
        print(f"Message for {student_name} failed to reach a final status within {max_retries} retries.")
        return False

    def handle_message_failure(self, message_type, to, content_variables, student_name, voucher_month, voucher_password):
        print("Message delivery failed. Will send manually:")

        if (message_type.lower() == "whatsapp"):
            # Construct message to be sent
            message = str(TWILIO_MESSAGE_TEMPLATE).format(student_name, voucher_month, voucher_password)
            to = self.switch_number(message_type, student_name)
            _sid = self.send_sms_message(to, message)  # Send SMS message manually
            print(f"Switching {student_name}'s to {to} and sending SMS message manually.")
            self.check_and_handle_message_status(_sid, content_variables, to, student_name, voucher_month, voucher_password)
        elif(message_type.lower() == "sms"):
            # Construct message to be sent
            #message = str(TWILIO_MESSAGE_TEMPLATE).format(student_name, voucher_month, voucher_password)
            to = self.switch_number(message_type, student_name)
            print(f"Switching {student_name}'s to {to} and sending WhatsApp message manually.")
            _sid = self.send_WA_message(to, content_variables)  # Send WhatsApp message manually
            self.check_and_handle_message_status(_sid, content_variables, to, student_name, voucher_month, voucher_password)

    def switch_number(self, message_type, student_name):
        global student_records

        # Switch the number thats used to send a message to and from whatsapp to sms or vice versa
        if message_type.lower() == "whatsapp":
            # Get the student's data based on the name
            for student in student_records:
                if student['Name'] + " " + student['Surname'] == student_name:	
                    # Switch the numbers
                    return format_number(student['SMS number'])
        elif message_type.lower() == "sms":
            # Get the student's data based on the name
            for student in student_records:
                if student['Name'] + " " + student['Surname'] == student_name:
                    # Switch the numbers
                    return format_number(student['WhatsApp number'])
                
    def check_message_status(self, message_sid):
        """
        Checks the status of a Twilio message.

        Args:
            message_sid: The message SID.

        Returns:
            True if the message is successfully delivered, False otherwise.
        """
        message = client.messages(message_sid).fetch()
        return message.status
