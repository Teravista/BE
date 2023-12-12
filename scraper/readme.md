# WAŻNE
**przed pierwszym uruchomieniem scrappera należy:**
- usunąć plik products.xml
- dodać folder images do folderu scrapped_data
- dodatkowo można usunąć zawartość folderu images (jeśli uruchamiamy już któryś raz).
- Ważne żeby struktura plików wyglądała następująco

scrapper <br>
|--main.py <br>
|--scrap_categories.py <br>
|--main_categories_urls <br>
|--subcategories.txt <br>
|--subsubcategories.txt <br>
|--readme.md <br>
scrapped_data <br>
|--images

## pliki do uruchomienia:
- **scrap_categories.py** - scrapuje wszystkie uzywane kategorie do dwóch plików opisanych niżej
- **main.py** - scrapuje produkty do pliku products.xml i pobiera zdjecia produktów