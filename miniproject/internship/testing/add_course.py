import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

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

driver.get("http://127.0.0.1:8000/add_subjects/")

# Locate the username and password fields and input the credentials
course_field = driver.find_element(By.NAME, "course_name")
course_field.send_keys("Python")

coursetitle_field = driver.find_element(By.NAME, "title")
coursetitle_field.send_keys("Python for Data Science, AI & Development")

courseimage_field = driver.find_element(By.NAME, "image")
courseimage_field.send_keys(r"D:\Main-Project\miniproject\internship\media\pics\python.png")

coursepromo_field = driver.find_element(By.NAME, "promo")
coursepromo_field.send_keys(r"D:\Main-Project\miniproject\internship\media\video\python.mp4")

desc_field = driver.find_element(By.NAME, "desc")
desc_field .send_keys("This introduction to Python course will take you from zero to programming in Python in a matter of hours—no prior programming experience necessary! You will learn about Python basics and the different data types. You will familiarize yourself with Python Data structures like List and Tuples, as well as logic concepts like conditions and branching. You will use Python libraries such as Pandas, Numpy & Beautiful Soup. You’ll also use Python to perform tasks such as data collection and web scraping with APIs.  ")

course_week = Select(driver.find_element(By.NAME, 'course_week'))
course_week.select_by_value('9')

price_field = driver.find_element(By.NAME, "price")
price_field.send_keys("899")

outcomes_field = driver.find_element(By.NAME, "outcomes")
outcomes_field.send_keys("Describe Python Basics including Data Types, Expressions, Variables, and Data Structures.")

assignment_field = driver.find_element(By.NAME, "assignment")
assignment_field.send_keys("Quiz.")

Certificate = Select(driver.find_element(By.NAME, 'Certificate'))
Certificate.select_by_value('Yes')

submit_button = driver.find_element('css selector', 'button[type="submit"]')
submit_button.click()

driver.get("http://127.0.0.1:8000/add_subjects/")

time.sleep(5)
# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h3[contains(text(), 'Add Courses')]")
if dashboard_element:
    print("Course added Successfully")
else:
    print("Test failed.")