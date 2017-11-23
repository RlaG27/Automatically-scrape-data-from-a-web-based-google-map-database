from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import os, time

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars --disable-extensions --window-size=1366,768")
driver = webdriver.Chrome(chrome_options=options, executable_path=os.getcwd() + '/WebDriver/chromedriver.exe')
driver.get("https://www.google.com/maps")

elm = driver.find_element_by_css_selector("input#searchboxinput")

time.sleep(5)
# zoom in with shortcut
action_chain = ActionChains(driver)
action_chain.move_to_element(elm).move_by_offset(1000, 500).perform()

driver.execute_script("window.scrollBy(200,300);")
