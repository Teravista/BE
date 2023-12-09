import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re


def scrape_product_page(driver, product_page_url):
    # Navigate to the product page URL
    driver.get(product_page_url)

    # Extracting the price
    try:
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.price span.woocommerce-Price-amount.amount'))
        )
        product_price_raw = price_element.text.strip()
    except Exception:
        product_price_raw = "Price not available"

    # Clean up the price using regular expression
    product_price = re.sub(r'[^\d.,]', '', product_price_raw)
    print(f"Product Price: {product_price}")

    # Alternative method if the first one fails
    try:
        attributes_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.woocommerce-product-attributes.shop_attributes'))
        )
        attribute_rows = attributes_table.find_elements(By.CSS_SELECTOR, 'tbody tr')
        print("Specifications:")
        for row in attribute_rows:
            attribute_name = row.find_element(By.CSS_SELECTOR, 'span.wd-attr-name').text.strip()
            attribute_value = row.find_element(By.CSS_SELECTOR,
                                               'td.woocommerce-product-attributes-item__value').text.strip()
            print(f"{attribute_name}: {attribute_value}")

    except Exception:
        print("No specifications found in the second method.")
    # Extracting specifications
    # This part depends heavily on the structure of your product page
    # You need to adjust the selectors based on your page's HTML structure
    try:
        specifications_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.wc-tab-inner'))
        )

        # Get the HTML content of the element
        specifications_html = specifications_div.get_attribute('outerHTML')

        # Now, specifications_html contains the HTML content
        # You can print it or save it to a file
        print(specifications_html)

        # If you want to save it to a file
        # with open('specifications.html', 'w', encoding='utf-8') as file:
        #     file.write(specifications_html)

    except Exception:
        print("No specifications found in the first method.")

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully and saved at: {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = 'https://spawanie.com/kategoria/agregaty-pradotworcze/agregaty-trojfazowe/'

    try:
        driver.get(url)

        # Fetch the total number of products
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-element-top"))
        )
        total_products = len(product_elements)

        for index in range(total_products):
            # Navigate back to the main page
            driver.get(url)

            # Re-fetch the list of products
            product_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-element-top"))
            )

            # Access the current product
            product = product_elements[index]
            product_name = product.find_element(By.CSS_SELECTOR, '.top-information h3.wd-entities-title a').text.strip()
            product_page_link = product.find_element(By.CSS_SELECTOR,
                                                     '.top-information h3.wd-entities-title a').get_attribute('href')
            srcset = product.find_element(By.CSS_SELECTOR,
                                          'a img').get_attribute('srcset')
            srcset = srcset.split(',')
            for i in range(len(srcset)):
                srcset[i] = srcset[i].split(' ')
                srcset[i] = srcset[i][-2]
            photo_link_1 = srcset[0]
            photo_link_2 = srcset[len(srcset) - 2]
            download_image(photo_link_1, f"images/{product_name}_1.jpg")
            download_image(photo_link_2, f"images/{product_name}_2.jpg")
            print(f"Product Name: {product_name}, Page Link: {product_page_link}")

            scrape_product_page(driver, product_page_link)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
