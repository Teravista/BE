from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import json
import os
from product import Product

# Web Driver configuration
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()))
driver.get("http://www.python.org")

productList = []

# getting pages URLs
f = open("URL.txt", "r")
URLs = []
for x in f:
    URLs.append(x)
f.close()

# searching through each page from file and through each subpage (< 1 2 3 ... 7 >)
for URL in URLs:
    emptyPage = False  # means that the page number is out of range and there is no more content on this page
    subpageCounter = 1
    while not emptyPage:
        print(URL + '/page/' + str(subpageCounter))
        driver.get(URL + '/page/' + str(subpageCounter))
        subpageCounter += 1
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'products')))
            container = driver.find_element(By.CLASS_NAME, 'products')
            products = container.find_elements(By.CLASS_NAME, 'product-grid-item')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            counter = 0
            for product in products:
                name_link = product.find_element(By.CLASS_NAME, 'wd-entities-title').find_element(By.TAG_NAME, "a")
                name = name_link.text
                link = name_link.get_attribute('href')

                counter += 1
                p = Product(name, link)
                productList.append(p)

        except TimeoutException:
            print('[INFO] Ostatnia podstrona adresu URL')
            emptyPage = True

os.remove('productsJSON.txt')

for product in productList:
    # write converted course object into output file
    string = product.makeJSON()
    with open('productsJSON.txt', 'a', encoding='utf-8') as file:
        json.dump(string, file, ensure_ascii=False)
        file.write("\n")

driver.quit()
file.close()
