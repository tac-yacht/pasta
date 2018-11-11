from selenium import webdriver
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    code = event['placementInfo']['attributes']['code']
    if not code:
        raise Exception('attr[code] is undefined')
    url = "https://ssl.jobcan.jp/m/work/accessrecord?_m=adit&code=" + code
    logger.info("target url: %s",url)

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
    driver.get(url)
    adit_item = driver.find_element_by_xpath("//input[@type=\"submit\" and @value=\"打刻\"]").get_attribute("class")    
    driver.close()
    return adit_item