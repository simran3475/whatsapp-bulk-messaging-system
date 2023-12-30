'''
Design a Whatsapp Messaging System.
    A service in which user can send a message to all the whatsapp number present in csv file
    A service in which user can schedule the message to be sent at particular time to all the whatsapp number specified
    A service which allows you to filter specific phone numbers from the csv/excel file to send the message
'''
# Include all the necessary libraries
import csv
import pywhatkit
import schedule
import time

import pyautogui as pg

def send_messages_to_all(file_path, message):
    # Reads numbers from a CSV file and sends the message to each.
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        # Check for header like konse column mai numbers stored hai 👆
        for row in reader:
            number = row[header.index('Phone No.')] 
            pywhatkit.sendwhatmsg_instantly(number, message)
            pg.press("enter")
            pg.press("ctrl+w")
            time.sleep(10)

def schedule_message(file_path, message, time_hour, time_minute):
    # Schedules a message to be sent at the specified time.
    schedule.every().day.at(f"{time_hour}:{time_minute}").do(send_messages_to_all, file_path, message) # 24 hour format

def filter_and_send(file_path, message, filter_criteria):
    # Filters numbers based on criteria and sends the message.
    filtered_numbers = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row along with stored in a list header
        for row in reader:
            if filter_criteria(row):  # Implement your filtering logic here
                filtered_numbers.append(row[0])

    for number in filtered_numbers:
        pywhatkit.sendwhatmsg_instantly(number, message)


if __name__ == "__main__":
    # Example usage:
    file_path = "../contacts.csv"
    message = "Hello from the WhatsApp Messaging System!"
    time_hour = 10
    time_minute = 30

    '''
    before running this code, open whatsapp web in your browser and you have to be logged in 
    otherwise it will not work
    '''

    # testing
    send_messages_to_all(file_path, message)
    # schedule_message(file_path, message, time_hour, time_minute)
    # filter_and_send(file_path, message, lambda row: row[1] == "Country")  # Example filter

    # Keep the program running for scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)