'''
Design a Whatsapp Messaging System.
    A service in which user can send a message to all the whatsapp number present in csv file
    A service in which user can schedule the message to be sent at particular time to all the whatsapp number specified
    A service which allows you to filter specific phone numbers from the csv/excel file to send the message
'''
from yowsup.env import YowsupEnv
from yowsup.stacks import YowStack
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer, ProtocolEntity
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.stanzaregulator import YowStanzaRegulatorLayer
from yowsup.layers import YowParallelLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers import YowParallelLayer

import csv
from datetime import datetime, timedelta

class WhatsAppMessagingSystem:
    def __init__(self, phone_number, password):
        self.phone_number = phone_number
        self.password = password
        self.stack = self.setup_whatsapp_stack()

    def setup_whatsapp_stack(self):
        layers = (
            YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer]),
            YowParallelLayer([YowCoderLayer, YowNetworkLayer, YowStanzaRegulatorLayer]),
        )
        return YowStack(layers)

    def start_whatsapp_stack(self):
        self.stack.setProp(YowAuthenticationProtocolLayer.PHONE_NUMBER, self.phone_number)
        self.stack.setProp(YowAuthenticationProtocolLayer.PASSWORD, self.password)
        self.stack.setProp(YowNetworkLayer.ENDPOINT, YowStack.ENDPOINTS[0])
        self.stack.start()

    def send_whatsapp_message(self, to_whatsapp_number, message):
        outgoing_message = self.stack.send(YowMessagesProtocolLayer.toLower(message))
        outgoing_message["message"]["to"] = f"{to_whatsapp_number}@s.whatsapp.net"
        self.stack.broadcast(outgoing_message)

    def send_message_to_all(self, csv_file, message):
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                to_whatsapp_number = row[0]
                self.send_whatsapp_message(to_whatsapp_number, message)

    def schedule_message(self, csv_file, message, scheduled_time):
        now = datetime.now()
        scheduled_datetime = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")

        if scheduled_datetime <= now:
            print("Scheduled time must be in the future.")
            return

        delay_seconds = (scheduled_datetime - now).total_seconds()

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                to_whatsapp_number = row[0]
                self.send_whatsapp_message(to_whatsapp_number, message)

    def send_message_to_selected_numbers(self, csv_file, message, selected_numbers):
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                to_whatsapp_number = row[0]
                if to_whatsapp_number in selected_numbers:
                    self.send_whatsapp_message(to_whatsapp_number, message)

# Replace these values with your WhatsApp account details
phone_number = 'your_phone_number'  # in the format: '1234567890'
password = 'your_password'

whatsapp_system = WhatsAppMessagingSystem(phone_number, password)

# Example usage
message = "Hello, this is a test message!"

# Send message to all numbers in the CSV file
whatsapp_system.send_message_to_all('contacts.csv', message)

# Schedule a message to be sent at a specific time (Note: Yowsup doesn't support scheduling, this is just for illustration)
scheduled_time = "2023-12-25 12:00:00"
whatsapp_system.schedule_message('contacts.csv', message, scheduled_time)

# Send message to selected numbers from the CSV file
selected_numbers = ['1234567890', '9876543210']
whatsapp_system.send_message_to_selected_numbers('contacts.csv', message, selected_numbers)
