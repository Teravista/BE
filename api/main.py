import xml.etree.ElementTree as ET
from prestapyt import PrestaShopWebService, PrestaShopWebServiceDict, PrestaShopWebServiceError


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


def init_presta_api_connection():
    with open('./api/key.txt', 'r', encoding='utf-8') as file:
        api_key = file.read().strip()

    url = 'http://localhost:8080/api'
    return PrestaShopWebServiceDict(url, api_key)


def clear_categories(prestashop):
    print("clearing categories")
    try:
        # Pobieranie listy wszystkich kategorii
        response = prestashop.get('categories')
        categories = response['categories']['category']

        for category in categories:
            category_id = category['attrs']['id']

            # Pomijanie kategorii głównej (zwykle o ID 2)
            if category_id == '2':
                continue

            try:
                # Usuwanie kategorii
                prestashop.delete('categories', resource_ids=category_id)
                print(f'Usunięto kategorię o ID: {category_id}')
            except PrestaShopWebServiceError as e:
                print(f'Błąd podczas usuwania kategorii o ID {category_id}: {e}')

    except PrestaShopWebServiceError as e:
        print(f'Nie można pobrać listy kategorii: {e}')


def clear_products(prestashop):
    print("clearing products")
    try:
        # Pobieranie listy wszystkich produktów
        response = prestashop.get('products')
        products = response['products']['product']

        for product in products:
            product_id = product['attrs']['id']
            try:
                # Usuwanie produktu
                prestashop.delete('products', resource_ids=product_id)
                print(f'Usunięto produkt o ID: {product_id}')
            except PrestaShopWebServiceError as e:
                print(f'Błąd podczas usuwania produktu o ID {product_id}: {e}')
    except PrestaShopWebServiceError as e:
        print(f'Nie można pobrać listy produktów: {e}')


def add_category(prestashop, parent_id, category_name):
    link = category_name.replace(' ', '-')
    new_category = {
        'category': {
            'id_parent': parent_id,  # Parent category ID (e.g., 2 for Home category)
            'active': '1',  # Set to '1' to activate the category
            'name': {'language': {'attrs': {'id': '1'}, 'value': category_name}},
            'link_rewrite': {'language': {'attrs': {'id': '1'}, 'value': link}},
            'description': {'language': {'attrs': {'id': '1'}, 'value': category_name}},
        }
    }
    result = prestashop.add('categories', new_category)
    new_category_id = result['category']['id']

    return new_category_id


def add_main_categories(prestashop, categories):
    category_id_pairs = []

    for category in categories:
        category_id = add_category(prestashop, 2, category)
        category_id_pairs.append((category, category_id))

    return category_id_pairs


def add_subcategories(prestashop, categories_pairs, subcategories):
    for subcategory in subcategories:
        parent_category_name, subcategory_name = subcategory

        # Znajdź odpowiednią kategorię nadrzędną w categories_pairs
        parent_id = None
        for category_pair in categories_pairs:
            if category_pair[0] == parent_category_name:
                parent_id = category_pair[1]
                break

        if parent_id is not None:
            subcategory_id = add_category(prestashop, parent_id, subcategory_name)
            categories_pairs.append((subcategory_name, subcategory_id))
        else:
            print(f"error finding category for subcategory named: {subcategory}")

    return categories_pairs


def main(mode):
    products = read_products_from_xml()
    categories = read_main_categories()
    subcategories = read_subcategories()
    prestashop = init_presta_api_connection()

    if mode == 1:
        # clearing shop
        clear_products(prestashop)
        clear_categories(prestashop)
    elif mode == 2:
        categories_pairs = add_main_categories(prestashop, categories)
        categories_pairs = add_subcategories(prestashop, categories_pairs, subcategories)

        print(categories_pairs)

        # TODO implement adding products


if __name__ == "__main__":
    main(1)
