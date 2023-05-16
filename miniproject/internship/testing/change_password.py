import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
service = Service(executable_path=r"\Users\city7\OneDrive\Desktop\FINAL\yogastudio\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("http://127.0.0.1:8000/login/")

username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("anayasusan826@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("!QAZ2wsx")
password_field.send_keys(Keys.RETURN)


driver.get("http://127.0.0.1:8000/changepassword/")

oldpass_field = driver.find_element(By.NAME, "current_password")
oldpass_field.send_keys(str("!QAZ2wsx"))

newpass_field = driver.find_element(By.NAME, "new_password")
newpass_field.send_keys(str("@WSX1qaz"))


conpass_field = driver.find_element(By.NAME, "confirm_password")
conpass_field.send_keys(str("@WSX1qaz"))
conpass_field.send_keys(Keys.RETURN)


driver.get("http://127.0.0.1:8000/login/")
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("anayasusan826@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("@WSX1qaz")
password_field.send_keys(Keys.RETURN)


dashboard_element = driver.find_element(By.XPATH, "//h1[contains(text(), 'Learning Today')]")
if dashboard_element:
    print("Test Passed")
else:
    print("Test Failed")

driver.quit()