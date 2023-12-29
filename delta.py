# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# import time as timee

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # Install/Creating a new instance of ChromeDriver
# link = "https://web.whatsapp.com/"
# driver.get(link)
# timee.sleep(15)

# from alright import WhatsApp
# messenger = WhatsApp()
# messenger.find_user("919625579828")
# messenger.send_message("Hello from the WhatsApp Messaging System!")

# import keyboard as key


import webbrowser as web
import pyautogui as pg
import time as timee

web.open("https://web.whatsapp.com/send?phone=919625579828&text={_message}")
timee.sleep(15)
pg.press("enter")

# browser se bhejo code og browser valla 
# wrote pywhatkit pura khud se lol