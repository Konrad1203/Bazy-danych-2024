
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

### Diagram bazy danych

<p align="center">
  <img src="imgs/diagram.png" alt="Diagram">
</p>

### Opis tabel

#### Clients (lista klientów wypożyczalni)
- client_id - id klienta (to samo co login_id)
- firstname - imię
- lastname - nazwisko
- address - adres
- phone - numer telefonu

```sql
CREATE TABLE Clients (
    client_id integer  NOT NULL,
    firstname varchar2(20)  NOT NULL,
    lastname varchar2(20)  NOT NULL,
    address_id integer  NOT NULL,
    phone varchar2(15)  NOT NULL,
    CONSTRAINT Clients_pk PRIMARY KEY (client_id)
);
```
![clients](imgs/tables/clients.png)

---

#### Reservation (tabela z rezerwacjami filmów)
- reservation_id - id rezerwacji
- copy_id - id egzemplarza filmu
- client_id - id klienta
- reservation_date - data rezerwacji 
- reservation_expiry_date - data wygaśnięcia rezerwacji
- status - akutalny status rezerwacji

```sql
CREATE TABLE Reservation (
    reservation_id integer  NOT NULL,
    copy_id integer  NOT NULL,
    client_id integer  NOT NULL,
    reservation_date date  NOT NULL,
    reservation_expiry_date date  NOT NULL,
    status char(1)  NOT NULL,
    CONSTRAINT Reservation_pk PRIMARY KEY (reservation_id)
);
ALTER TABLE Reservation ADD CONSTRAINT Reservation_Clients
    FOREIGN KEY (client_id)
    REFERENCES Clients (client_id);
ALTER TABLE Reservation ADD CONSTRAINT Reservation_Copy
    FOREIGN KEY (copy_id)
    REFERENCES Copy (copy_id);
```
![reservations](imgs/tables/reservations.png)
---

#### Rental (informacje dotyczące wypożyczeń filmów przez klientów)
- rental_id - id wypożyczenia
- client_id - id klienta
- copy_id - id wypożyczonego egzemplarza
- out_date - data wypożyczenia filmu
- due_date - okres, na który film został wypożyczony

```sql
CREATE TABLE Rental (
    rental_id integer  NOT NULL,
    client_id integer  NOT NULL,
    copy_id integer  NOT NULL,
    out_date date  NOT NULL,
    due_date date  NOT NULL,
    CONSTRAINT Rental_pk PRIMARY KEY (rental_id)
);
ALTER TABLE Rental ADD CONSTRAINT Copy_Rental
    FOREIGN KEY (copy_id)
    REFERENCES Copy (copy_id);
ALTER TABLE Rental ADD CONSTRAINT Rental_Clients
    FOREIGN KEY (client_id)
    REFERENCES Clients (client_id);
```

![rental](imgs/tables/rental.png)
---

#### Copy (lista fizycznych kopii danego filmu)
- copy_id - id danej kopii
- movie_id - id jej filmu
- on_loan - czy wypożyczona ("Y", jeśli wypożyczona, "N" jeśli nie)

```sql
CREATE TABLE Copy (
    copy_id integer  NOT NULL,
    movie_id integer  NOT NULL,
    on_loan char(1)  NOT NULL,
    CONSTRAINT Copy_pk PRIMARY KEY (copy_id)
);
ALTER TABLE Copy ADD CONSTRAINT Copy_Movies
    FOREIGN KEY (movie_id)
    REFERENCES Movies (movie_id);
```
![copy](imgs/tables/copy.png)

---

#### Categories (lista kategorii)
- category_id - id kategorii
- name - nazwa kategorii
  
```sql
CREATE TABLE Categories (
    category_id int  NOT NULL,
    name varchar2(20)  NOT NULL,
    CONSTRAINT Categories_pk PRIMARY KEY (category_id)
);
```

![categories](imgs/tables/categories.png)

---

#### Movies (tabela zawierające informacje o filmach)
- movie_id - id filmu
- name - nazwa filmu
- title - tytuł filmu
- category_id - id głównej kategorii filmu
- release_date - data globalna wydania filmu
- duration - czas trwania filmu
- rating - ocena filmu w skali 1 do 10
- description - krótki opis filmu
- production_country - kraj produkcji
- director - imię i nazwisko reżysera

```sql
CREATE TABLE Movies (
    movie_id int  NOT NULL,
    title varchar2(50) NOT NULL,
    category_id int  NOT NULL,
    release_date date  NOT NULL,
    duration timestamp  NOT NULL,
    rating int  NULL,
    description varchar2(100)  NULL,
    budget int  NULL,
    director varchar2(40)  NULL,
    CONSTRAINT Movies_pk PRIMARY KEY (movie_id)
);
ALTER TABLE Movies ADD CONSTRAINT Movies_Categories
    FOREIGN KEY (category_id)
    REFERENCES Categories (category_id);

```

![movies](imgs/tables/movies.png)

---

#### Actors (lista aktorów)
- actor_id - id aktora
- firstname - imię aktora
- lastname - nazwisko aktora

```sql
CREATE TABLE Actors (
    actor_id int  NOT NULL,
    firstname varchar2(20)  NOT NULL,
    lastname varchar2(20)  NOT NULL,
    CONSTRAINT Actors_pk PRIMARY KEY (actor_id)
);
```

![actors](imgs/tables/actors.png)

---

#### Actors_in_movie (tabela łącząca aktora z filmem)
- movie_id - id filmu
- actor_id - id aktora
- role - rola aktora w filmie (jaką postać gra)

```sql
CREATE TABLE Actors_in_movie (
    movie_id int  NOT NULL,
    actor_id int  NOT NULL,
    role varchar2(20)  NOT NULL,
    CONSTRAINT Actors_in_movie_pk PRIMARY KEY (actor_id,movie_id)
);
ALTER TABLE Actors_in_movie ADD CONSTRAINT Actors_in_movie_Actors
    FOREIGN KEY (actor_id)
    REFERENCES Actors (actor_id);
ALTER TABLE Actors_in_movie ADD CONSTRAINT Actors_in_movie_Movies
    FOREIGN KEY (movie_id)
    REFERENCES Movies (movie_id);
```

![actors_in_movie](imgs/tables/actors_in_movie.png)

---

### Widoki

#### vw_available_copies

Widok dostępnych kopii filmów wyświetla listę dostępnych kopii filmów wraz z ich szczegółami, takimi jak tytuł filmu, kategoria, data wydania, dostępność itp.

```sql
CREATE VIEW vw_available_copies  AS
SELECT c.copy_id,
       m.title AS movie_title,
       cat.name AS category_name,
       m.release_date,
       m.duration,
       c.on_loan
FROM Copy c
JOIN Movies m ON c.movie_id = m.movie_id
JOIN Categories cat ON m.category_id = cat.category_id
WHERE c.on_loan = 'N';
```
```sql
select * from vw_available_copies;
```
![vw_available_copies](imgs/views/vw_available_copies.png)

---


#### vw_current_reservations

Widok rezerwacji aktualnych klientów pokazuje rezerwacje aktualnych klientów wraz z danymi klientów, filmami, na które zarezerwowali kopie, datami rezerwacji itp.

```sql
CREATE VIEW vw_current_reservations AS
SELECT r.reservation_id,
       c.client_id,
       c.firstname,
       c.lastname,
       m.title AS movie_title,
       r.reservation_date,
       r.reservation_expiry_date
FROM Reservation r
JOIN Clients c ON r.client_id = c.client_id
JOIN Copy co ON r.copy_id = co.copy_id
JOIN Movies m ON co.movie_id = m.movie_id
WHERE r.status = 'A';
```
```sql
select * from vw_current_reservations;
```
![vw_current_reservations](imgs/views/vw_current_reservations.png)

---

#### vw_movie_popularity

```sql
CREATE VIEW vw_movie_popularity AS
SELECT m.movie_id,
       m.title AS movie_title,
       COUNT(r.rental_id) AS num_rentals
FROM Movies m
LEFT JOIN Copy c ON m.movie_id = c.movie_id
LEFT JOIN Rental r ON c.copy_id = r.copy_id
GROUP BY m.movie_id, m.title
ORDER BY COUNT(r.rental_id) DESC;
```
```sql
select * from vw_movie_popularity;
```
![vw_movie_popularity](imgs/views/vw_movie_popularity.png)

---


#### vw_actor_rentals

Widok przedstawiający listę aktorów występujących w obecnie wypożyczonych filmach oraz liczbę filmów, w których każdy aktor wystąpił.

```sql
CREATE OR REPLACE VIEW vw_actor_rentals AS
SELECT a.actor_id,
       a.firstname,
       a.lastname,
       COUNT(*) AS num_movies
FROM Actors a
JOIN Actors_in_movie aim ON a.actor_id = aim.actor_id
JOIN Movies m ON aim.movie_id = m.movie_id
JOIN Copy c ON m.movie_id = c.movie_id
JOIN Rental r ON c.copy_id = r.copy_id
GROUP BY a.actor_id, a.firstname, a.lastname;
```
```sql
SELECT * FROM ActorRentals;
```
![vw_actor_rentals](imgs/views/vw_actor_rentals.png)

---

### Możliwe widoki do zrealizowania:

1. Widok Aktywnych Wypożyczeń: Ten widok mógłby wyświetlać aktualne wypożyczenia, obejmujące informacje o klientach, filmach, kopii filmów, datach wypożyczenia i zwrotu itp.
2. Widok Klientów z Opóźnieniami Zwrotu: Ten widok mógłby identyfikować klientów, którzy mają opóźnione zwroty i wyświetlać informacje o klientach, filmach, które wypożyczyli, datach wypożyczenia i zwrotu oraz czasie opóźnienia.
3. Widok Dochodów z Wypożyczeń: Ten widok mógłby obliczać całkowite dochody z wypożyczeń, grupując wypożyczenia według miesiąca lub roku i sumując opłaty za wypożyczenia.


### Funkcje

#### f_get_client_reservations

Funkcja `f_get_client_reservations` umożliwia pobranie listy rezerwacji dla określonej osoby na podstawie jej identyfikatora klienta. Zwraca informacje o identyfikatorze rezerwacji, tytule filmu, dacie rezerwacji, dacie wygaśnięcia rezerwacji i statusie rezerwacji, co ułatwia zarządzanie rezerwacjami klientów w systemie wypożyczalni filmów.

```sql
CREATE OR REPLACE FUNCTION f_get_client_reservations(client_id_input INT) 
RETURN SYS_REFCURSOR
IS
    reservation_cursor SYS_REFCURSOR;
BEGIN
    OPEN reservation_cursor FOR
        SELECT r.reservation_id,
               m.title AS movie_title,
               r.reservation_date,
               r.reservation_expiry_date,
               r.status
        FROM Reservation r
        JOIN Copy c ON r.copy_id = c.copy_id
        JOIN Movies m ON c.movie_id = m.movie_id
        WHERE r.client_id = client_id_input;

    RETURN reservation_cursor;
END;
```
```sql
select f_get_client_reservations(1) from dual;
```
![f_get_client_reservations](imgs/functions/f_get_client_reservations.png)

---

#### f_is_copy_reserved_or_rented

Funkcja `f_is_copy_reserved_or_rented` umożliwia sprawdzenie statusu konkretnej kopii filmu na podstawie jej identyfikatora. Zwraca informacje o tym, czy kopia jest aktualnie zarezerwowana, wypożyczona, dostępna, lub czy nie istnieje w bazie danych. Jest to przydatne narzędzie do zarządzania dostępnością kopii filmów w systemie wypożyczalni.

```sql
CREATE OR REPLACE FUNCTION f_is_copy_reserved_or_rented(copy_id_input INT) 
RETURN VARCHAR2
IS
    status VARCHAR2(10);
BEGIN
    SELECT 
        CASE
            WHEN EXISTS (SELECT 1 FROM Reservation WHERE copy_id = copy_id_input AND status = 'A') THEN 'Reserved'
            WHEN EXISTS (SELECT 1 FROM Rental WHERE copy_id = copy_id_input) THEN 'Rented'
            ELSE 'Available'
        END
    INTO status
    FROM dual;

    RETURN status;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 'Copy not found';
END;
```
```sql
select f_is_copy_reserved_or_rented(1) from dual;
```
![f_is_copy_reserved_or_rented](imgs/functions/f_is_copy_reserved_or_rented.png)


---


#### f_get_movies_by_category

Funkcja `f_get_movies_by_category` zwraca filmy należące do określonej kategorii na podstawie przekazanego identyfikatora kategorii. Zestawienie zawiera nazwę kategorii, tytuł filmu, opis filmu, datę premiery, czas trwania, ocenę, i reżysera.

```sql
CREATE OR REPLACE FUNCTION f_get_movies_by_category(category_id_input INT)
RETURN SYS_REFCURSOR
IS
    movie_cursor SYS_REFCURSOR;
BEGIN
    OPEN movie_cursor FOR
        SELECT
            c.name AS category_name,
            m.title AS movie_name,
            m.description AS movie_description,
            m.release_date,
            m.duration,
            m.rating,
            m.director
        FROM Movies m
        JOIN Categories c ON m.category_id = c.category_id
        WHERE c.category_id = category_id_input;

    RETURN movie_cursor;
END;
```

```sql
select f_get_movies_by_category(2) from dual;
```
![f_get_movies_by_category](imgs/functions/f_get_movies_by_category.png)


---

### Procedury

CRUD dla Reservation, Rental, Copy, Movie

### Triggery


