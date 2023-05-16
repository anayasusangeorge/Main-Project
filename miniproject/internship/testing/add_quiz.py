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

driver.get("http://127.0.0.1:8000/add_quiz/")

# Locate the username and password fields and input the credentials
course_name = Select(driver.find_element(By.NAME, 'course'))
course_name.select_by_value('7')

course_week = Select(driver.find_element(By.NAME, 'course_week'))
course_week.select_by_value('2')

question = driver.find_element(By.NAME, "question")
question.send_keys("Which of the following is the branch of Artificial Intelligence?")

option1_field = driver.find_element(By.NAME, "op1")
option1_field.send_keys("Machine Learning")

option2_field = driver.find_element(By.NAME, "op2")
option2_field.send_keys("Cyber forensics")

option3_field = driver.find_element(By.NAME, "op3")
option3_field.send_keys("Full-Stack Developer")

option4_field = driver.find_element(By.NAME, "op4")
option4_field.send_keys("Network Design")

coursetitle_field = driver.find_element(By.NAME, "ans")
coursetitle_field.send_keys("option1")

wait = WebDriverWait(driver, 10)
submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary')))

submit_button.click()
# submit_button = driver.find_element('css selector','button[type="submit"]')
# submit_button.click()


# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h3[contains(text(), 'Add Quiz')]")
if dashboard_element:
    print("Quiz added Successfully")
else:
    print("Test failed.")