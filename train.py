# proberen om tickets voor een weinig rijdende echte stoom trein ;) te verkrijgen
import datetime
import subprocess
import sys
# from pathlib import Path

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    from selenium import webdriver
except ModuleNotFoundError as ve:
    print(f"{ve} trying to install")
    install("selenium")

try:
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
except ModuleNotFoundError as ve:
    print(f"{ve} trying to install")
    install("webdriver_manager")

try:
    import undetected_chromedriver as uc
except ModuleNotFoundError as ve:
    print(f"{ve} trying to install")
    install("undetected_chromedriver")

from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.common.exceptions import NoSuchElementException,TimeoutException

# driver =  webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver = uc.Chrome(use_subprocess=False)

delay = 20

driver.get("https://train.yoyaku.jrkyushu.co.jp/inbound/")


WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Click here for detailed search']"))).click()

WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='calender']//div"))).click()
WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ui-icon ui-icon-circle-triangle-e']"))).click()
try:
    # Reservation service is available from 05:30 to 23:00 (JST) ofwel 7 uur later, ofwel tussen 22:30 in de avond en 16 's middags.
    today = datetime.datetime.now().day
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space()='{today}']"))).click()
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchCondition.departureStationName']"))
    ).send_keys("Kumamoto", Keys.ENTER)
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchCondition.arrivalStationName']"))
    ).send_keys("Tosu")

    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='selectTrain1Btn']"))).click()
    select = Select(WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='useTrain1']"))))
    select.select_by_visible_text("SL Hitoyoshi")

    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='searchbtn']"))).click()

    try:

        date,mogelijk = driver.find_element(By.XPATH, "//p[@class='date']"),driver.find_element(By.XPATH, "//tr[@id='dispCheckFirst']/td/div")
        print(date.text, mogelijk.text)
    except NoSuchElementException as no:
        print("deze dag rijd er geen trein")

except TimeoutException as no:
    print("datum nog niet te selecteren")
