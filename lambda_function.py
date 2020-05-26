from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
loginURL = "https://ssl.jobcan.jp/login/mb-employee?lang_code=ja"

def lambda_handler(event, context):
    clientId = event['placementInfo']['attributes']['clientId']
    if not clientId:
        raise Exception('attr[clientId] is undefined')
    email = event['placementInfo']['attributes']['email']
    if not email:
        raise Exception('attr[email] is undefined')
    password = event['placementInfo']['attributes']['password']
    if not password:
        raise Exception('attr[password] is undefined')

    options = webdriver.ChromeOptions()

    options.binary_location = "./bin/headless-chromium"

    # headlessで動かすために必要なオプション
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")

    driver = webdriver.Chrome("./bin/chromedriver",chrome_options=options)
    logger.info("init done")

    # ログインページ
    driver.get(loginURL)
    logger.info("open done:%s",driver.title)
    log.debug(driver.current_url)
    #諸情報入力
    driver.find_element_by_id("client_id").send_keys(clientId)
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("password").send_keys(password)
    #ログイン画面遷移
    driver.find_element_by_xpath("//button[@type=\"submit\" and contains(text(),\"ログイン\")]").click()
    wait = WebDriverWait(driver, 60)
    element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//img[@alt=\"打刻\"]")))

    #打刻画面遷移
    driver.find_element_by_xpath("//img[@alt=\"打刻\"]").click()

#    driver.find_element_by_xpath("//input[@type=\"submit\" and @value=\"打刻\"]").click()
    log.debug(driver.find_element_by_xpath("//input[@type=\"submit\" and @value=\"打刻\"]").is_enabled())
    driver.close()
    return