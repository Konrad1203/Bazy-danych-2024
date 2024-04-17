
# **<p align="center">Wypożyczalnia filmów</p>**
#### **<p align="center">Zespół: Tomasz Furgała, Konrad Tendaj, Łukasz Zegar</p>**

<br>

### Aktorzy

1. Klient:
    - klient może założyć konto, które umożliwia mu korzystanie z systemu,
    - może składać rezerwacje na wybrany film,
    - przegląda listę filmów oferowanych przez wyporzyczalnie,
    - przeglądanie listy obecnie zarezrwonych i wypożyczonych przez niego filmów.

2. Pracownik:
    - rejestruje wypożycznie i zwracanie filmów w systemie,
    - dodawanie nowych filmów i kopii do systemu,
    - przegląda rezerawacje i wypożyczenia klientów,
    - może generować raporty.
    
3. Administrator
    - może edytować, dodawać, usuwać tabele,
    - może edytować, dodawać, usuwać dane w tabelach,
    - może generować raporty.

### Diagram

<p align="center">
  <img src="imgs/diagram.png" alt="Diagram">
</p>

### Opis tabel

#### Clients (lista klientów wypożyczalni)
- client_id - id klienta (to samo co login_id)
- firstname - imię
- lastname - nazwisko
- phone - numer telefonu

#### Movies (tabela zawierające informacje o filmach)
- movie_id - id filmu
- category_id - id głównej kategorii filmu
- release_date - data globalna wydania filmu
- duration - czas trwania filmu
- rating - ocena filmu w skali 1 do 100
- description - krótki opis filmu
- budget - budżet filmu
- director - imię i nazwisko reżysera

#### Categories (lista kategorii)
- category_id - id kategorii
- name - nazwa kategorii

#### Actors (lista aktorów)
- actor_id - id aktora
- firstname - imię aktora
- lastname - nazwisko aktora

#### Actors_in_movie (tabela łącząca aktora z filmem)
- movie_id - id filmu
- actor_id - id aktora
- role - rola aktora w filmie (jaką postać gra)

#### Reservation (tabela z rezerwacjami filmów)
- reservation_id - id rezerwacji
- copy_id - id egzemplarza filmu
- client_id - id klienta
- reservation_date - data rezerwacji 
- reservation_expiry_date - data wygaśnięcia rezerwacji
- status - akutalny status rezerwacji

#### Rental (informacje dotyczące wypożyczeń filmów przez klientów)
- rental_id - id wypożyczenia
- client_id - id klienta
- copy_id - id wypożyczonego egzemplarza
- out_date - data wypożyczenia filmu
- due_date - okres, na który film został wypożyczony

#### Copy (lista fizycznych kopii danego filmu)
- copy_id - id danej kopii
- movie_id - id jej filmu
- on_loan - czy wypożyczona ("Y", jeśli wypożyczona, "N" jeśli nie)

