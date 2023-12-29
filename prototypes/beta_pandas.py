import pandas as pd
import pywhatkit
import schedule
import time

def send_messages_to_all(df, message):
    for number in df['Phone No.']:
        pywhatkit.sendwhatmsg_instantly(number, message)

def schedule_message(df, message, time_hour, time_minute):
    def job():
        send_messages_to_all(df, message)

    schedule.every().day.at(f"{time_hour}:{time_minute}").do(job)

def filter_and_send(df, message, filter_criteria):
    filtered_numbers = df[df.apply(filter_criteria, axis=1)]['Phone No.'].tolist()

    for number in filtered_numbers:
        pywhatkit.sendwhatmsg_instantly(number, message)

# Example usage:
file_path = "../contacts.csv"
message = "Hello from the WhatsApp Messaging System!"
time_hour = 10
time_minute = 30

# Load CSV into a DataFrame
df = pd.read_csv(file_path)

'''
before running this code, open whatsapp web in your browser and you have to be logged in 
otherwise it will not work
'''

# testing
send_messages_to_all(df, message)
# schedule_message(df, message, time_hour, time_minute)
# filter_and_send(df, message, lambda row: row['Column_Name'] == "Filter_Criteria")  # Example filter

# Keep the program running for scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
