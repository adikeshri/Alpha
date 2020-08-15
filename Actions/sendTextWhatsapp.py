from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys

from selenium.webdriver.chrome.options import Options

def sendTextWhatsapp(to,message):
    print(to)
    print(message)
    try:
        options = Options()
        options.add_argument("user-data-dir=/home/adi/.config/google-chrome/Default")
        # Replace below path with the absolute path of the \
        #chromedriver in your computer
        driver = webdriver.Chrome(r'/home/adi/Downloads/chromedriver',chrome_options=options)

        driver.get("https://web.whatsapp.com/")
        # time.sleep()
        wait = WebDriverWait(driver, 600)
        # Replace 'My Bsnl' with the name of your friend or group name
        target = '"'+to+'"'
        # Replace the below string with your own message
        string = message+" "+"[Sent via Anton]"

        x_arg = '//span[contains(@title,' + target + ')]'
        group_title = wait.until(EC.presence_of_element_located((
        By.XPATH, x_arg)))
        group_title.click()
        message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]

        message.send_keys(string)
        sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
        sendbutton.click()
        driver.close()
    except:
        return "Could not send the message."
    return "Message sent to " + to + " on whatsapp saying " + message
