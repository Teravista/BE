subcategories = [
    ('Materiały spawalnicze', 'Druty do spawania pod topnikiem'),
    ('Materiały spawalnicze', 'Druty lite do spawania w osłonie gazów'),
    ('gowno', 'mega'),
    ('test', 'abcd')
]

unnecessary_categories = ['Druty do spawania pod topnikiem', 'gowno', 'abcd']

# Usuń krotki zawierające niepotrzebne podkategorie
updated_subcategories = [subcat for subcat in subcategories if subcat[1] not in unnecessary_categories]

# Zaktualizuj listę niepotrzebnych kategorii, usuwając te, które faktycznie zostały znalezione
updated_unnecessary_categories = [cat for cat in unnecessary_categories if not any(cat == subcat[1] for subcat in subcategories)]

# Wynikowe tablice
print("Subcategories after removal:", updated_subcategories)
print("Unnecessary categories after removal:", updated_unnecessary_categories)
