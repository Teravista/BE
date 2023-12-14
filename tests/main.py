import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def a_add_products(category):
    try:
        action = ActionChains(driver=driver)
        driver.get("http://localhost:8080/index.php?id_category=2&controller=category")
        cat1 = driver.find_element(by=By.LINK_TEXT, value=category)
        action.move_to_element(cat1).click().perform()

        number_of_products = 0
        needed_number_of_products = 5
        while(number_of_products < needed_number_of_products):
            products = driver.find_elements(by=By.CLASS_NAME, value="product-title")
            products[number_of_products].find_element(by=By.TAG_NAME, value="a").click()
            additional_product_amount = random.randint(0, 4)
            for j in range(additional_product_amount):
                driver.find_element(by=By.CLASS_NAME, value="touchspin-up").click()
            time.sleep(2)
            add_to_cart = driver.find_element(by=By.CLASS_NAME, value="add-to-cart")
            if add_to_cart.get_property("disabled"):
                # out of stock
                number_of_products += 1
                needed_number_of_products += 1
                driver.back()
                driver.back()
                continue
            add_to_cart.click()
            number_of_products += 1
            driver.back()
            driver.back()
    except:
        print("Error:   a) Adding products to cart")
    else:
        print("Success: a) Adding products to cart")


def b_search():
    try:
        search_box = driver.find_element(by=By.NAME, value="s")
        search_box.send_keys("rx 6700")
        search_box.send_keys(Keys.ENTER)

        products = driver.find_elements(by=By.CLASS_NAME, value="product-title")

        not_found = True
        while not_found:
            product = products[random.randint(0, len(products) - 1)]
            try:
                product.find_element(By.CLASS_NAME, value="out_of_stock")
            except:
                not_found = False
        product.click()
        driver.find_element(by=By.CLASS_NAME, value="add-to-cart").click()
        driver.back()
        driver.refresh()
    except:
        print("Error:   b) Searching for products")
    else:
        print("Success: a) Searching for products")
        time.sleep(2)

def c_remove_products():
    try:
        driver.find_element(by=By.CLASS_NAME, value="shopping-cart").click()
        for _ in range(3):
            driver.find_element(by=By.CLASS_NAME, value="remove-from-cart").click()
    except:
        print("Error:   c) Removing products")
    else:
        print("Success: c) Removing products")
        time.sleep(2)


def d_register():
    try:
        driver.find_element(By.PARTIAL_LINK_TEXT, "Zaloguj").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Nie masz").click()
        driver.find_element(By.CLASS_NAME, "custom-radio").click()
        driver.find_element(By.NAME, "firstname").send_keys("Mamasz")
        driver.find_element(By.NAME, "lastname").send_keys("Dziubale")

        email_randomizer = random.randint(0,99999999)
        driver.find_element(By.NAME, "email").send_keys("mamaszdziubale" + str(email_randomizer) + "@gmail.com" )
        driver.find_element(By.NAME, "password").send_keys("kochamako1234!")
        driver.find_element(By.NAME, "birthday").send_keys("1969-01-01")

        # RODO
        checkboxes = driver.find_elements(By.CLASS_NAME, "custom-checkbox")
        for box in checkboxes:
            box.click()
        driver.find_element(By.CLASS_NAME, "form-control-submit").click()
    except:
        print("Error:   d) Registering")
    else:
        print("Success: d) Registering")
        time.sleep(2)

def e_order_and_status():
    try:
        driver.find_element(by=By.CLASS_NAME, value="shopping-cart").click()
        driver.find_element(by=By.CLASS_NAME, value="btn-primary").click()
        driver.find_element(By.NAME, "address1").send_keys("Nottingham NG7 2WS")
        driver.find_element(By.NAME, "postcode").send_keys("12-345")
        driver.find_element(By.NAME, "city").send_keys("Lenton")
        driver.find_element(By.NAME, "confirm-addresses").click()
        driver.find_element(By.NAME, "confirmDeliveryOption").click()
        driver.find_element(By.NAME, "conditions_to_approve[terms-and-conditions]").click()
        driver.find_element(by=By.ID, value="payment-confirmation").find_element(by=By.CLASS_NAME, value="btn-primary").click()
        check_status()
    except:
        print("Error:   e) Ordering")
    else:
        print("Success: e) Ordering")

def check_status():
    try:
        driver.find_element(By.CLASS_NAME, "account").click()
        driver.find_element(By.ID, "history-link").click()
        driver.find_element(By.LINK_TEXT, "Szczegóły").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Pobierz").click()
    except:
        print("Error:   j) Checking status")
    else:
        print("Success: j) Checking status")
        time.sleep(2)

if __name__ == "__main__":
    host = 'http://localhost:8080/index.php'
    driver = webdriver.Chrome()
    driver.get(host)

    driver.implicitly_wait(7)

    # skip https warning
    driver.find_element(By.ID, "details-button").click()
    driver.find_element(By.ID, "proceed-link").click()

    # a. Dodanie do koszyka 10 produktów (w różnych ilościach) z dwóch różnych
    # kategorii
    a_add_products("Spawarki elektrodowe")
    a_add_products("Chemia spawalnicza")

    # b. Wyszukanie produktu po nazwie i dodanie do koszyka losowego produktu
    # spośród znalezionych
    b_search()

    # c. Usunięcie z koszyka 3 produktów,
    c_remove_products()

    # d. Rejestracja nowego konta,
    d_register()

    # e. Wykonanie zamówienia zawartości koszyka,
    # f. Wybór metody płatności: przy odbiorze,
    # g. Wybór jednego z dwóch przewoźników,
    # h. Zatwierdzenie zamówienia,
    # i. Sprawdzenie statusu zamówienia.
    # j. Pobranie faktury VAT
    e_order_and_status()

    driver.quit()
