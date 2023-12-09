from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = 'https://spawanie.com/'

    try:
        driver.get(url)

        # Closing the cookie consent banner
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmplz-close"))
        )
        close_button.click()

        # Opening the category list
        hover_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".menu-opener"))
        )
        ActionChains(driver).move_to_element(hover_element).perform()

        # Wait for the category list to load
        category_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#menu-kategorie li a.woodmart-nav-link"))
        )

        # Extract and print the text and link from each category
        for element in category_elements:
            category_name = element.find_element(By.CSS_SELECTOR, '.nav-link-text').text
            category_link = element.get_attribute('href')
            print(f"Category: {category_name}, Link: {category_link}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
