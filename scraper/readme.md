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
|--images_converted

## pliki do uruchomienia:
- **scrap_categories.py** - scrapuje wszystkie uzywane kategorie do dwóch plików opisanych niżej
- **main.py** - scrapuje produkty do pliku products.xml i pobiera zdjecia produktów

## zescrapowane dane:
- **categories.txt** - plik z kategoriami głównymi (te podlegające kategorii domowej)
- **subcategories.txt** - plik z podkategoriami (te podlegające innym kategoriom) wraz z ich nadrzędnymi kategoriami.
- **producs.xml** - plik z zescrapowanymi produktami i ich właściwościom
- **images** - folder z pobranymi zdjęciami. Ze względu na dużą ilość danych dodany do .gitignore. Wszystkie zdjęcia będzie można przez pewien czas znaleźć tutaj: [images](https://drive.google.com/drive/folders/1frfFdUcEB0J45K0mcMI1elQjlc0bJQBC?usp=sharing)
