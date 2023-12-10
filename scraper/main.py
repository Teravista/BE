import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import xml.etree.ElementTree as ET
import os


def append_to_xml(product_details, xml_file_path):
    # Check if the XML file exists
    if not os.path.exists(xml_file_path):
        # Create the root element
        root = ET.Element('Products')
        tree = ET.ElementTree(root)
    else:
        # Parse the existing XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

    # Create a new element for this product
    product_element = ET.SubElement(root, 'Product')

    # Add details to the product element
    for key, value in product_details.items():
        sub_element = ET.SubElement(product_element, key)
        sub_element.text = str(value)

    # Write back to the XML file
    tree.write(xml_file_path)


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
    # print(f"Product Price: {product_price}")

    specifications = ""
    # Alternative method if the first one fails
    try:
        attributes_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.woocommerce-product-attributes.shop_attributes'))
        )
        attribute_rows = attributes_table.find_elements(By.CSS_SELECTOR, 'tbody tr')
        # print("Specifications:")
        for row in attribute_rows:
            attribute_name = row.find_element(By.CSS_SELECTOR, 'span.wd-attr-name').text.strip()
            attribute_value = row.find_element(By.CSS_SELECTOR,
                                               'td.woocommerce-product-attributes-item__value').text.strip()
            # print(f"{attribute_name}: {attribute_value}")
            specifications += f"{attribute_name}: {attribute_value}\n"

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
        # print(specifications_html)

    except Exception:
        print("No specifications found in the first method.")
    finally:
        return [product_price, specifications, specifications_html]

def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)


def scrap_products_from_category(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    xml_file_path = '../scrapped_data/products.xml'

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
            category = scrap_category_name(product_page_link)
            # print(category)
            srcset = product.find_element(By.CSS_SELECTOR,
                                          'a img').get_attribute('srcset')
            srcset = srcset.split(',')
            for i in range(len(srcset)):
                srcset[i] = srcset[i].split(' ')
                srcset[i] = srcset[i][-2]
            photo_link_1 = srcset[0]
            photo_link_2 = srcset[len(srcset) - 2]
            file_name = sanitize_filename(product_name)
            download_image(photo_link_1, f"../scrapped_data/images/{file_name}_1.jpg")
            download_image(photo_link_2, f"../scrapped_data/images/{file_name}_2.jpg")
            # print(f"Product Name: {product_name}, Page Link: {product_page_link}")

            details = scrape_product_page(driver, product_page_link)
            if (details[0] != ""):
                product_details = {
                    'Name': product_name,
                    'Category': category,
                    'ImageName1': f"{file_name}_1.jpg",
                    'ImageName2': f"{file_name}_2.jpg",
                    'Price': details[0],
                    'Specifications': details[1],
                    'SpecificationsHTML': details[2],
                    'Link': product_page_link
                }

                append_to_xml(product_details, xml_file_path)



    finally:
        driver.quit()
        print(f"saved category from url: {url} succesfully")


def scrap_category_name(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)

        # Wait for the breadcrumb element to be present
        breadcrumb_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".breadcrumb-link.breadcrumb-link-last"))
        )

        # Extract the text from the breadcrumb element
        breadcrumb_text = breadcrumb_element.text

    finally:
        driver.quit()

    return breadcrumb_text


def main():
    # amount of pages for each category
    lengths = [3, 5, 9, 2, 31, 3, 5, 36, 13, 34, 3, 7]
    with open("main_categories_urls.txt", 'r') as file:
        urls = file.readlines()
        idx = 0
        for url in urls:
            url = url[:-2]
            length = lengths[idx]
            for i in range(length):
                page = f"{url}/page/{i+1}"
                scrap_products_from_category(page)
        idx +=1


if __name__ == "__main__":
    main()
