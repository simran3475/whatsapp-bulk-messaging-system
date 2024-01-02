from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
input("Scan QR code and press Enter")

timeout = 300

driver.get("https://web.whatsapp.com/send?phone=919625579828&text=Hello%20World")
# make the browser wait untill the send_button shows up

send_button_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'

send_button = WebDriverWait(driver, timeout).until(
    ec.visibility_of_element_located((By.XPATH, send_button_xpath))
)

send_button.click()

driver.get("https://web.whatsapp.com/send?phone=919625579828&text=fuck%20yez")

send_button_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'

send_button = WebDriverWait(driver, timeout).until(
    ec.visibility_of_element_located((By.XPATH, send_button_xpath))
)

send_button.click()
