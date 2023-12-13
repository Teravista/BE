from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def format_subcategories(subcategories):
    formatted_subcategories = []
    for category, subcategory in subcategories:
        if subcategory != "":
            formatted_subcategory = subcategory.lower()
            formatted_subcategory = formatted_subcategory[0].upper() + formatted_subcategory[1:]
            formatted_subcategories.append((category, formatted_subcategory))
    return formatted_subcategories



def scrap_subcategories(driver, categories, url_file):
    with open(url_file, 'r') as file:
        urls = file.readlines()

    subcategories = []
    idx = 0
    # Process each URL
    for url in urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        driver.get(url)

        category_link_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.category-nav-link"))
        )

        # Extract the text from each category's span element
        for element in category_link_elements:
            category_name = element.find_element(By.CSS_SELECTOR, 'span.nav-link-text').text
            # Append both the category and the subcategory as a tuple
            subcategories.append((categories[idx], category_name))

        idx += 1
    subcategories = format_subcategories(subcategories)
    return subcategories


def create_file(categories, subcategories, subsubcategories):
    # Save the categories to a file
    with open('../scrapped_data/categories.txt', 'w', encoding='utf-8') as file:
        for category in categories:
            file.write(category + '\n')

    # Save the subcategories and subsubcategories to another file
    with open('../scrapped_data/subcategories.txt', 'w', encoding='utf-8') as file:
        for category, subcategory in subcategories:
            file.write(f"{subcategory}, {category}\n")
        for category, subsubcategory in subsubcategories:
            file.write(f"{subsubcategory}, {category}\n")


def remove_unnecesary_categories(subcategories, subsubcategories):
    unnecesary_categories = ['Akcesoria do niwelatorów', 'Albatros', 'Eco/aristo air', 'Elektroniczne', 'F10', 'Inne',
                             'Inne', 'Nawiew esab epr-x1', 'New-tech adc plus', 'Niwelatory laserowe', 'Origo',
                             'Pilarki', 'Pionowniki laserowe', 'Poziomice elektroniczne', 'Wózki paletowe']

    # Usuń krotki zawierające niepotrzebne podkategorie
    updated_subcategories = [subcat for subcat in subcategories if subcat[1] not in unnecesary_categories]

    # Zaktualizuj listę niepotrzebnych kategorii, usuwając te, które faktycznie zostały znalezione
    updated_unnecessary_categories = [cat for cat in unnecesary_categories if
                                      not any(cat == subcat[1] for subcat in subcategories)]

    # Usuń krotki zawierające niepotrzebne podkategorie
    updated_subsubcategories = [subcat for subcat in subsubcategories if subcat[1] not in unnecesary_categories]

    # Zaktualizuj listę niepotrzebnych kategorii, usuwając te, które faktycznie zostały znalezione
    updated_unnecessary_categories = [cat for cat in updated_unnecessary_categories if
                                      not any(cat == subcat[1] for subcat in subsubcategories)]

    print(updated_unnecessary_categories)
    return updated_subcategories, updated_subsubcategories


def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = 'https://spawanie.com/'

    try:
        driver.get(url)

        # Closing cookie button

        # Wait for the element with the class .cmplz-close to be present and clickable
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmplz-close"))
        )
        # Click the button
        close_button.click()

        # Opening the category list
        hover_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".menu-opener"))
        )
        # Hover over the element to trigger any interactions
        ActionChains(driver).move_to_element(hover_element).perform()

        # Wait for the category list to load after the hover action
        categories = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#menu-kategorie .nav-link-text"))
        )

        # Extract and store the text from each category
        categories = [category.text for category in categories]

        # Remove the fifth element
        if len(categories) >= 6:
            categories.pop(5)  # Index 4 corresponds to the fifth element
            categories.pop(11)
            categories.pop(10)

        print(categories)
        # Keep only the last 9 categories - the ones with subcategories
        last_9_categories = categories[-6:]

        # Call the scrap_subcategories function with the last 9 categories
        subcategories = scrap_subcategories(driver, last_9_categories, 'subcategories.txt')

        print(subcategories)

        subcategories_with_subcategories = [
            "Niwelatory i lasery", "Narzędzia ogrodowe", "Narzędzia ręczne", "Części do przyłbic",
            "Przyłbice spawalnicze", "Sprzęt asekuracyjny", "Tablice i naklejki bhp", "Szczotki druciane"
        ]

        subsubcategories = scrap_subcategories(driver, subcategories_with_subcategories, 'subsubcategories.txt')
        print(subsubcategories)
        subcategories, subsubcategories = remove_unnecesary_categories(subcategories, subsubcategories)
        create_file(categories, subcategories, subsubcategories)


    finally:
        driver.quit()


if __name__ == "__main__":
    main()
