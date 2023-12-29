'''
Design a Whatsapp Messaging System.
    A service in which user can send a message to all the whatsapp number present in csv file
    A service in which user can schedule the message to be sent at particular time to all the whatsapp number specified
    A service which allows you to filter specific phone numbers from the csv/excel file to send the message
'''

# Include all the necessary libraries from selenium/webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Include all the other required libraries
import schedule
import time
import pandas as pd
from datetime import datetime, timedelta, time
from urllib.parse import quote

# Function to open WhatsApp Web in the browser
def open_whastapp():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # Install/Creating a new instance of ChromeDriver
    link = "https://web.whatsapp.com/"
    driver.get(link)
    time.sleep(15)

# Function to send a message on whatsapp
def send_message(number, message, country_code="91"):
    _message = quote(message)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # Install/Creating a new instance of ChromeDriver
    link = f"https://web.whatsapp.com/send?phone={country_code}{number}&text={_message}" # URL to send a message to a number
    driver.get(link)
    time.sleep (5) # Wait for 5 seconds to load the page
    action = ActionChains (driver) 
    action.send_keys (Keys.ENTER) 
    action.perform() 
    time.sleep (5) # Wait for 5 seconds to confirm the message is sent

# Function to send messages to all the numbers in a CSV file
def send_messages_csv_all(file_path, message, column_name='Phone No.'):
    try:
        df = pd.read_csv(file_path)
        numbers = df['Phone No.'].tolist()
        for number in numbers:
            send_message(number, message)

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")

    except KeyError:
        print(f"Error: There is no column named '{column_name}' in the CSV file.")
        print("Please check the Excel file and try again.")
        print(f"If you find that the column name is different, please change it to '{column_name}' and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to send messages to all the numbers in a Excel file
def send_messages_excel_all(file_path, message, column_name='Phone No.'):
    try:
        df = pd.read_excel(file_path)
        numbers = df[column_name].tolist()
        for number in numbers:
            send_message(number, message)

    except pd.errors.EmptyDataError:
        print("Error: The Excel file is empty.")

    except KeyError:
        print(f"Error: There is no column named '{column_name}' in the Excel file.")
        print("Please check the Excel file and try again.")
        print(f"If you find that the column name is different, please change it to '{column_name}' and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def schedule_message_everyday(file_path, message, time_hour, time_minute, func):
    # Schedules a message to be sent at the specified time everyday.
    schedule.every().day.at(f"{time_hour}:{time_minute}").do(func, file_path, message) # 24 hour format

def schedule_message(file_path, message, time_hour, time_minute, func):
    # Schedules a message to be sent at the specified time that day.
    schedule.at(f"{time_hour}:{time_minute}").do(func, file_path, message) # 24 hour format

def schedule_message_weekly(file_path, message, time_hour, time_minute, day, func):
    # Schedules a message to be sent at the specified time on the specified day of the week.
    schedule.every().day.at(f"{time_hour}:{time_minute}").do(func, file_path, message).day.at(day) # 24 hour format

def schedule_message_monthly(file_path, message, time_hour, time_minute, day, func):
    # Schedules a message to be sent at the specified time on the specified day of the month.
    schedule.every().day.at(f"{time_hour}:{time_minute}").do(func, file_path, message).day.at(day) # 24 hour format

def schedule_message_yearly(file_path, message, time_hour, time_minute, day, month, func):
    # Schedules a message to be sent at the specified time on the specified day of the month.
    schedule.every().day.at(f"{time_hour}:{time_minute}").do(func, file_path, message).day.at(day).month.at(month) # 24 hour format


# Function can be used to filter the numbers based on the criteria specified by the user (tags/places/etc.)
def filter_by_tag_csv(file_path, message, tag, tag_column_name='Tag'):
    # Send a message to all the numbers that have the specified tag in the CSV file
    try:
        df = pd.read_csv(file_path)
        numbers = df[df[tag_column_name].lower() == tag.lower()]['Phone No.'].tolist()
        for number in numbers:
            send_message(number, message)

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")

    except KeyError:
        print(f"Error: There is no column named '{tag_column_name}' in the CSV file.")
        print("Please check the CSV file and try again.")
        print(f"If you find that the column name is different, please change it to '{tag_column_name}' and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function can be used to filter the numbers based on the criteria specified by the user (tags/places/etc.)
def filter_by_tag_excel(file_path, message, tag, tag_column_name='Tag'):
    # Send a message to all the numbers that have the specified tag in the Excel file
    try:
        df = pd.read_excel(file_path)
        numbers = df[df[tag_column_name].lower() == tag.lower()]['Phone No.'].tolist()
        for number in numbers:
            send_message(number, message)

    except pd.errors.EmptyDataError:
        print("Error: The Excel file is empty.")

    except KeyError:
        print(f"Error: There is no column named '{tag_column_name}' in the Excel file.")
        print("Please check the Excel file and try again.")
        print(f"If you find that the column name is different, please change it to '{tag_column_name}' and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to filter the numbers based on names (starts with/ends with/contains) using a CSV file
def filter_numbers_by_name_csv(file_path, message, filter_condition, name_pattern, column_name='Name'):
    try:
        df = pd.read_csv(file_path)
        # Apply the filtering condition based on the name pattern
        if filter_condition == 'starts_with':
            filtered_df = df[df[column_name].str.startswith(name_pattern, na=False)]
        elif filter_condition == 'ends_with':
            filtered_df = df[df[column_name].str.endswith(name_pattern, na=False)]
        elif filter_condition == 'contains':
            filtered_df = df[df[column_name].str.contains(name_pattern, na=False)]
        # Extract the 'Phone No.' column from the filtered DataFrame
        filtered_numbers = filtered_df['Phone No.'].tolist()
        for number in filtered_numbers:
                send_message(number, message)

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")

    except KeyError:
        print(f"Error: There is no column named '{column_name}' in the CSV file.")
        print("Please check the CSV file and try again.")
        print(f"If you find that the column name is different, please change it to '{column_name}' and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to filter the numbers based on names (starts with/ends with/contains) using a Excel file
def filter_numbers_by_name_excel(file_path, message, filter_condition, name_pattern, column_name='Name'):
    try:
        df = pd.read_excel(file_path)
        # Apply the filtering condition based on the name pattern
        if filter_condition == 'starts_with':
            filtered_df = df[df[column_name].str.startswith(name_pattern, na=False)]
        elif filter_condition == 'ends_with':
            filtered_df = df[df[column_name].str.endswith(name_pattern, na=False)]
        elif filter_condition == 'contains':
            filtered_df = df[df[column_name].str.contains(name_pattern, na=False)]
        # Extract the 'Phone No.' column from the filtered DataFrame
        filtered_numbers = filtered_df['Phone No.'].tolist()
        for number in filtered_numbers:
                send_message(number, message)

    except pd.errors.EmptyDataError:
        print("Error: The Excel file is empty.")

    except KeyError:
        print(f"Error: There is no column named '{column_name}' in the Excel file.")
        print("Please check the Excel file and try again.")
        print(f"If you find that the column name is different, please change it to '{column_name}' and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")