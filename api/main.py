import xml.etree.ElementTree as ET
from prestapyt import PrestaShopWebService, PrestaShopWebServiceDict

def read_products_from_xml():
    # Wczytujemy dane z pliku XML
    with open('./scrapped_data/products.xml', 'r', encoding='utf-8') as file:
        xml_data = file.read()

    # Parsujemy XML
    root = ET.fromstring(xml_data)

    # Lista do przechowywania obiektów produktów
    products = []

    # Iterujemy po elementach Product
    for product_elem in root.findall('Product'):
        product = {}
        # Iterujemy po elementach wewnątrz Product
        for elem in product_elem:
            # Sprawdzamy, czy elem.text nie jest None
            text = elem.text.strip() if elem.text is not None else None
            product[elem.tag] = text
        # Dodajemy produkt do listy, tylko jeśli nie zawierał pustych wartości
        if any(product.values()):
            products.append(product)

    print(f"found {len(products)} valid products")
    return products


def read_main_categories():
    categories = []

    # Wczytujemy dane z pliku categories.txt
    with open('./scrapped_data/categories.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # Usuwamy białe znaki z początku i końca linii
            category = line.strip()
            # Pomijamy puste linie
            if category:
                categories.append(category)

    # Wyświetlamy odczytane kategorie
    for category in categories:
        print(category)

    return categories


def read_subcategories():
    # Lista do przechowywania par kategorii i podkategorii
    subcategories = []

    # Wczytujemy dane z pliku subcategories.txt
    with open('./scrapped_data/subcategories.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # Dzielimy linię na dwie części: kategorię i podkategorię
            parts = line.strip().split(', ')
            # Dodajemy parę kategoria, podkategoria do listy
            subcategories.append((parts[1], parts[0]))

    # Wyświetlamy odczytane pary kategorii i podkategorii
    for subcategory in subcategories:
        print(subcategory)

    return subcategories


def main():
    products = read_products_from_xml()
    categories = read_main_categories()
    subcategories = read_subcategories()


if __name__ == "__main__":
    main()