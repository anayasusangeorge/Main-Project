import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service = Service(executable_path=r"D:\Main-Project\miniproject\internship\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:8000/login/")

# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("anayasusan826@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("@WSX1qaz")

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h1[contains(text(), 'Learning Today')]")
if dashboard_element:
    print("Login successful!")
else:
    print("Login failed.")


# Close the browser
driver.quit()