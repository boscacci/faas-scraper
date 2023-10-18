import os, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# Get the username and password from environment variables
username = os.environ.get("FOOD_COOP_USER")
password = os.environ.get("FOOD_COOP_PASS")

# Set up selenium
# Set Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)


def lambda_handler(event=None, context=None):
    # Nav to page
    url = "https://ort.foodcoop.com/login/"
    driver.get(url)
    time.sleep(1.5)

    # Find the username field and enter the username
    username_field = driver.find_element(
        by=By.XPATH, value="/html/body/div[2]/form[1]/p[1]/input"
    )
    username_field.send_keys(username)

    # Find the password field and enter the password
    password_field = driver.find_element(
        by=By.XPATH, value="/html/body/div[2]/form[1]/p[2]/input"
    )
    password_field.send_keys(password)

    # Find the enter button and click it
    enter_button = driver.find_element(
        by=By.XPATH, value="/html/body/div[2]/form[1]/input[3]"
    )
    enter_button.click()
    time.sleep(2)

    # Click on calendar link
    cal_link = driver.find_element(
        by=By.XPATH, value="/html/body/div[2]/p[1]/a[2]"
    )
    cal_link.click()
    time.sleep(2)

    # Check if all appointments are taken
    element = driver.find_element(by=By.XPATH, value="/html/body/div[2]/ul/li")
    text = element.text
    driver.quit()

    if "Sorry, all appointments are currently taken" in text:
        print("NO APPOINTMENTS")
        return 0
    else:
        print("APPOINTMENT(S) AVAILABLE")
        return 1

lambda_handler()