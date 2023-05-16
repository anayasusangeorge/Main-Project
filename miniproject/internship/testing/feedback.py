import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path=r"D:\Main-Project\miniproject\internship\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:8000/login/")

# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("anayasusan826@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("!QAZ2wsx")

# Submit the login form
password_field.send_keys(Keys.RETURN)

driver.get("http://127.0.0.1:8000/feedback/1/")

# Locate the username and password fields and input the credentials


feedback_msg = driver.find_element(By.NAME, "feedback_msg")
feedback_msg.send_keys("It was a great experience learning python from a trainer who is very friendly and gives an opportunity to every trainee to learn and enjoy the session. The course was completed with best examples that could be provided. Thank You.")


submit_button = driver.find_element(By.XPATH,'/html/body/main/section/div[2]/div/div/form/div[3]/button')
submit_button.click()

driver.get("http://127.0.0.1:8000/feedback/1/")
# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h2[contains(text(), 'Feedback')]")
if dashboard_element:
    print("Feedback sent Successfully")
else:
    print("Test failed.")




