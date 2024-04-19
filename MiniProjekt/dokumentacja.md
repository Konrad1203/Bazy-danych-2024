
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
- phone - numer telefonu

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

#### Categories (lista kategorii)
- category_id - id kategorii
- name - nazwa kategorii
  
#### Movies (tabela zawierające informacje o filmach)
- movie_id - id filmu
- category_id - id głównej kategorii filmu
- release_date - data globalna wydania filmu
- duration - czas trwania filmu
- rating - ocena filmu w skali 1 do 100
- description - krótki opis filmu
- budget - budżet filmu
- director - imię i nazwisko reżysera

#### Actors (lista aktorów)
- actor_id - id aktora
- firstname - imię aktora
- lastname - nazwisko aktora

#### Actors_in_movie (tabela łącząca aktora z filmem)
- movie_id - id filmu
- actor_id - id aktora
- role - rola aktora w filmie (jaką postać gra)

### Kod do wygenerowania bazy danych
```sql
CREATE TABLE Clients (
    client_id integer  NOT NULL,
    firstname varchar2(20)  NOT NULL,
    lastname varchar2(20)  NOT NULL,
    address_id integer  NOT NULL,
    phone varchar2(15)  NOT NULL,
    CONSTRAINT Clients_pk PRIMARY KEY (client_id)
);


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


CREATE TABLE Copy (
    copy_id integer  NOT NULL,
    movie_id integer  NOT NULL,
    on_loan char(1)  NOT NULL,
    CONSTRAINT Copy_pk PRIMARY KEY (copy_id)
);
ALTER TABLE Copy ADD CONSTRAINT Copy_Movies
    FOREIGN KEY (movie_id)
    REFERENCES Movies (movie_id);


CREATE TABLE Categories (
    category_id int  NOT NULL,
    name varchar2(20)  NOT NULL,
    CONSTRAINT Categories_pk PRIMARY KEY (category_id)
);


CREATE TABLE Movies (
    movie_id int  NOT NULL,
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


CREATE TABLE Actors (
    actor_id int  NOT NULL,
    firstname varchar2(20)  NOT NULL,
    lastname varchar2(20)  NOT NULL,
    CONSTRAINT Actors_pk PRIMARY KEY (actor_id)
);


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



