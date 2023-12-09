
<h1 style="font-size: 40px">Biznes-Elektroniczny-Pokatna</h1>

  

Jest to krótki tutorial jak uruchomić Prestashop

Musimy rozróżnić dwa przypadki:

- Windows

- Linux

  

Jeżeli używany jest linux można pominąć etap konfiguracji WSL

  

# Konfiguracja WSL

- [Docker](https://docs.docker.com/desktop/wsl/)

- [Windows](https://learn.microsoft.com/en-us/windows/wsl/install)

  

Powyżej wymienione są dwa linki do poradnika jak to zrobić, ale poniżej pokrótce to przedstawię.

  

1. Używamy komendy `wsl --install` w PowerShell. Jeżeli jest już zainstalowany Docker nie powinno to być konieczne

2. Wpisujemy `wsl.exe --set-default-version 2`, aby każda dokonana instalacja była w wersji 2

3. Instalujemy teraz dystrybucję Linuxa, polecam skorzystać po prostu z Ubuntu `wsl --install -d Ubuntu`

4. W moim przypadku konieczne było podniesiecie wersji do 2, ale można sprawdzić wersje swojej dystrybucji tą komendą `wsl.exe -l -v`

- Podnosimy wersję korzystając z tego `wsl.exe --set-version Ubuntu 2`

5. Ustawiamy naszą dystrybucję jako domyślną `wsl --set-default Ubuntu`

6. W **Settings** > **Resources** > **WSL Integration** ustawiamy naszą dystrybucję
  

# Uruchomienie Prestashop

Po pobraniu plików źródłowych wystarczy umieścić je w dowolnym (w przypadku WSL, to w dowolnym, ale na WSL) folderze. Następnie znajdując się w terminalu w wybranym folderze nadajemy uprawnienia 777 wszystkim plikom `sudo chmod 755 -R [folder]` i uruchamiamy `docker-compose up` i dzieje się magia. Uruchomi na się plik konfiguracyjny _docker-compose.yml_, który zainstaluje wymagane kontenery. Powinno to zająć około minuty, po tym czasie będzie możliwość wejścia w stronę sklepu.
**Uwaga doatkowy krok do pierwszej instalacji Prestashop:**
Po uruchomieniu sklepu konieczne jest cofnięcie zmian, aby być 1:1 z stanem jaki występuje na GitHub. Najpierw wyłączmy włączone kontenery dockera. Następnie ustawiamy uprawnienia plików na 777, potem przywracamy ustawienia gita korzystając z polecenia `git reset --hard`. 
Od tego momentu można korzystać z standardowych komend do uruchamiania i wyłączania dockera.

## Przykładowa sekwencja instalacji
1. `git clone https://github.com/kubix23/Biznes-Elektroniczny-Pokatna.git BiznesElektronicznyPokatna`
2. `cd BiznesElektronicznyPokatna`
3. `git checkout 'prestashop'`
4. `sudo chmod 777 -R Prestashop/`
5. `cd Prestashop/`
6. `docker-compose up`
7. ctrl + c
8. `docker-compose down`
9. `sudo chmod 777 -R .`
10. `git reset --hard`
11. `docker-compose up`
12. Prestashop już działa

## Komendy

- Uruchamianie: `docker-compose up`

- Wyłączanie: `docker-compose down`

- Login do bazy danych: **root**

- Hasło do bazy danych: **prestashop**

- Login administratora: **demo@prestashop.com**

- Hasło administratora: **12345678**

- Adres do:

- [Prestashop](http://localhost:8080)

- [Panelu administratora](http://localhost:8080/admin-dev)

- [PhpMyAdmin]( http://localhost:8081)


## Wybrane błędy

1. `prestashop exited with code 1`  
Jest to najczęściej spowodowane nie ustawieniem uprawnień 777 wszystkim plikom projektu. Często później wystąpi błąd 42
2. `prestashop exited with code 42`  
Powodem jest przerwanie inicjalizacji/instalacji Prestashop, może być to spowodowane ctrl+c, lub innymi czynnikami uniemożliwiającymi Prestashop ukończenie tego procesu.
3. Brak zmian na stronie sklepu  
Nie wykonano procesu związanego z pierwszą instalacją.
4. Błąd z dostępem do /var/www/...  
Nie wyłączono poprzednio otwrtych kontenerów poleceniem `docker-compose down`
