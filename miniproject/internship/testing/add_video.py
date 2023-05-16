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
username_field.send_keys("anayasusan3826@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("!QAZ2wsx")

# Submit the login form
password_field.send_keys(Keys.RETURN)

driver.get("http://127.0.0.1:8000/add_video/")

# Locate the username and password fields and input the credentials
course_name = Select(driver.find_element(By.NAME, 'course'))
course_name.select_by_value('7')

coursetitle_field = driver.find_element(By.NAME, "title")
coursetitle_field.send_keys("Python for Data Science, AI & Development")

course_week = Select(driver.find_element(By.NAME, 'course_week'))
course_week.select_by_value('2')

serial_field = driver.find_element(By.NAME, "serial_number")
serial_field.send_keys("1")

coursepromo_field = driver.find_element(By.NAME, "videos")
coursepromo_field.send_keys(r"D:\Main-Project\miniproject\internship\media\video\python.mp4")

time_field = driver.find_element(By.NAME, "time_duration")
time_field.send_keys("10.05")


submit_button = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div[2]/div/div/div/form/div/div[8]/button')
submit_button.click()


# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h3[contains(text(), 'Add Video')]")
if dashboard_element:
    print("Video added Successfully")
else:
    print("Test failed.")