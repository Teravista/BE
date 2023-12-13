import io
import random
import re
import xml.etree.ElementTree as ET

from prestapyt import PrestaShopWebServiceDict, PrestaShopWebServiceError


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
    # for category in categories:
    #     print(category)

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
    # for subcategory in subcategories:
    #     print(subcategory)

    return subcategories


def init_presta_api_connection():
    with open('./api/key.txt', 'r', encoding='utf-8') as file:
        api_key = file.read().strip()

    url = 'http://localhost:8080/api'
    return PrestaShopWebServiceDict(url, api_key)


def print_all_categories(prestashop):
    categories = prestashop.get('categories')

    # Process and print the categories
    for category in categories['categories']['category']:
        print(category)


def print_all_products(prestashop):
    products = prestashop.get('products')
    print(products)


def clear_categories(prestashop):
    print("clearing categories")
    try:
        # Pobieranie listy wszystkich kategorii
        response = prestashop.get('categories')
        categories = response['categories']['category']

        for category in categories:
            category_id = category['attrs']['id']

            # Pomijanie kategorii głównej (zwykle o ID 2)
            if category_id == '2' or category_id == '1':
                continue

            try:
                # Usuwanie kategorii
                prestashop.delete('categories', category_id)
                print(f'Usunięto kategorię o ID: {category_id}')
            except PrestaShopWebServiceError as e:
                print(f'Błąd podczas usuwania kategorii o ID {category_id}: {e}')
                # podczas usuwania podkategorii, których nadkategoria została usunięta będzie się pojawiał ten błąd, ale
                # podkategoria została już usunięta i wszystko dobrze działa

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
    print(result)  # Dodane do wypisania odpowiedzi

    # Odczytywanie ID nowo utworzonej kategorii
    try:
        new_category_id = result['prestashop']['category']['id']
        return new_category_id
    except KeyError:
        print("Nie można odnaleźć klucza 'category' w odpowiedzi")
        return None


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


def add_photo(id_of_product, file_name, prestashop):
    file_name = f"./scrapped_data/images_converted/{file_name}"
    fd = io.open(file_name, "rb")
    content = fd.read()
    fd.close()

    prestashop.add(f'/images/products/{id_of_product}', files=[('image', file_name, content)])


def validate(product):
    short_description = product['Specifications']
    if short_description is None:
        short_description = " "
        product['Specifications'] = short_description
    weight_match = re.search(r'Waga:\s*(\d+,\d+|\d+)\s*kg', short_description)
    weight = float(weight_match.group(1).replace(',', '.')) if weight_match else None

    if len(short_description) >= 799:
        short_description = short_description[:799]
        product['Specification'] = short_description
    long_description = product['SpecificationsHTML']
    if long_description is None:
        long_description = " "
        product['Specifications'] = long_description
    if weight is None:
        weight_match = re.search(r'Waga:\s*(\d+,\d+|\d+)\s*kg', long_description)
        weight = float(weight_match.group(1).replace(',', '.')) if weight_match else None
    if len(long_description) >= 21843:
        long_description = long_description[:21843]
        product['SpecificationHTML'] = long_description
    if weight is None:
        weight = random.randint(1, 60) / 10
    product['Weight'] = weight
    return product


def add_product(product, prestashop, id_category):
    formatted_price = product['Price'].replace('.', '').replace(',', '.')
    product = validate(product)
    try:
        product_schema = prestashop.get("products", options={"schema": "blank"})
    except PrestaShopWebServiceError as e:
        return {'error': str(e)}

    del product_schema['product']["position_in_category"]
    del product_schema['product']["associations"]["combinations"]

    print(product['Name'])

    product_schema['product']['name']['language']['value'] = product['Name']
    product_schema['product']['id_category_default'] = id_category
    product_schema['product']['price'] = formatted_price
    product_schema['product']['description_short']['language']['value'] = product['Specifications']
    product_schema['product']['description']['language']['value'] = product['SpecificationsHTML']
    product_schema["product"]["id_shop_default"] = 1
    product_schema['product']['active'] = 1
    product_schema["product"]["state"] = 1
    product_schema["product"]["weight"] = product['Weight']
    product_schema["product"]["available_for_order"] = 1
    product_schema["product"]["minimal_quantity"] = 1
    product_schema["product"]["show_price"] = 1
    product_schema['product']["associations"]["categories"] = {
        "category": [
            {"id": 2},
            {"id": id_category}
        ],
    }

    try:
        added_product = prestashop.add("products", product_schema)["prestashop"]["product"]
        product_id = added_product["id"]

        add_photo(product_id, product['ImageName1'], prestashop)
        add_photo(product_id, product['ImageName2'], prestashop)

        schema_id = prestashop.search("stock_availables", options={"filter[id_product]": product_id})[0]
        stock_available = prestashop.get("stock_availables", resource_id=schema_id)

        stock_available["stock_available"]["quantity"] = random.randint(0, 10)
        stock_available["stock_available"]["depends_on_stock"] = 0
        prestashop.edit("stock_availables", stock_available)
        return added_product
    except PrestaShopWebServiceError as e:
        error_message = str(e)
        return error_message


def find_index_by_name(pairs, name):
    for pair in pairs:
        if pair[0] == name:
            return pair[1]
    return None


def add_products(products, categories_pairs, prestashop, amount):
    print("adding product")
    products_to_add = products[:amount]
    for prod in products_to_add:
        category = prod['Category']
        idx = find_index_by_name(categories_pairs, category)
        if idx is None:
            formatted_category = category.lower()
            formatted_category = formatted_category[0].upper() + formatted_category[1:]
            idx = find_index_by_name(categories_pairs, formatted_category)
            if idx is None:
                print(f'couldnt find category for category name: {category}')
                continue

        add_product(prod, prestashop, idx)


def main(mode):
    products = read_products_from_xml()
    categories = read_main_categories()
    subcategories = read_subcategories()
    prestashop = init_presta_api_connection()

    if mode == 1:
        # clearing shop - doesn't work when there is only one product in shop.
        clear_products(prestashop)
        clear_categories(prestashop)
    elif mode == 2:
        # adding categories
        categories_pairs = add_main_categories(prestashop, categories)
        categories_pairs = add_subcategories(prestashop, categories_pairs, subcategories)
        print(categories_pairs)

        # adding products
        # not implemented yet
        amount = 1806
        add_products(products, categories_pairs, prestashop, amount)
    elif mode == 3:
        # printing all categories and products avaliable in shop
        print_all_categories(prestashop)
        print_all_products(prestashop)


if __name__ == "__main__":
    main(2)
