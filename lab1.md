# LAB 1. Oracle PL/Sql
widoki, funkcje, procedury, triggery ćwiczenie  
**Imiona i nazwiska autorów:** Tomasz Furgała, Konrad Tendaj, Łukasz Zegar


## Zadanie 0.
  Skomentuj dzialanie transakcji. Jak działa polecenie commit, rollback?. Co się dzieje w przypadku wystąpienia błędów podczas wykonywania
transakcji? Porównaj sposób programowania operacji wykorzystujących transakcje w Oracle PL/SQL ze znanym ci systemem/językiem MS
Sqlserver T-SQL


## Zadanie 1. Widoki
  vw_reservation widok łączy dane z tabel: trip, person, reservation
zwracane dane: reservation_id, country, trip_date, trip_name, firstname, lastname, status, trip_id, person_id
  vw_trip widok pokazuje liczbę wolnych miejsc na każdą wycieczkę
zwracane dane: trip_id, country, trip_date, trip_name, max_no_places, no_available_places (liczba wolnych miejsc)
  vw_available_trip
podobnie jak w poprzednim punkcie, z tym że widok pokazuje jedynie dostępne wycieczki (takie które są w przyszłości i są na nie wolne miejsca)


## Zadanie 2. Funkcje
  f_trip_participants
zadaniem funkcji jest zwrócenie listy uczestników wskazanej wycieczki
parametry funkcji: trip_id
funkcja zwraca podobny zestaw danych jak widok vw_eservation

```sql
CREATE OR REPLACE FUNCTION f_trip_participants (p_trip_id NUMBER)
    RETURN SYS_REFCURSOR
IS
    participants_cursor SYS_REFCURSOR;
    trip_exists NUMBER;
BEGIN
    IF p_trip_id IS NULL THEN
        RAISE_APPLICATION_ERROR(-20001, 'Parametry funkcji muszą być określone.');
    END IF;

    SELECT COUNT(*) INTO trip_exists FROM TRIP WHERE trip_id = p_trip_id;

    IF trip_exists = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Wycieczka o podanym trip_id nie istnieje.');
    END IF;

    OPEN participants_cursor FOR
        SELECT * FROM vw_reservation WHERE trip_id = p_trip_id;
    RETURN participants_cursor;
END;
```

  f_person_reservations
zadaniem funkcji jest zwrócenie listy rezerwacji danej osoby
parametry funkcji: person_id
funkcja zwraca podobny zestaw danych jak widok vw_reservation

```sql
CREATE or REPLACE FUNCTION f_person_reservations (p_person_id NUMBER)
    RETURN SYS_REFCURSOR
IS
    participants_cursor SYS_REFCURSOR;
    person_exists NUMBER;
BEGIN
    IF p_person_id IS NULL THEN
        RAISE_APPLICATION_ERROR(-20001, 'Parametry funkcji muszą być określone.');
    END IF;

    SELECT COUNT(*) INTO person_exists FROM PERSON WHERE PERSON_ID = p_person_id;

    IF person_exists = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Wycieczka o podanym trip_id nie istnieje.');
    END IF;

    OPEN participants_cursor FOR
        SELECT * FROM vw_reservation WHERE person_id = p_person_id;
    RETURN participants_cursor;
end;
```


  f_available_trips_to
zadaniem funkcji jest zwrócenie listy wycieczek do wskazanego kraju, dostępnych w zadanym okresie czasu (od date_from do
date_to)
parametry funkcji: country, date_from, date_to

```sql
CREATE or REPLACE FUNCTION f_available_trips_to (p_country VARCHAR(50), p_date_from date, p_date_to date)
    RETURN SYS_REFCURSOR
IS
    participants_cursor SYS_REFCURSOR;
BEGIN
    IF p_country IS NULL OR p_date_from IS NULL OR p_date_to IS NULL THEN
        RAISE_APPLICATION_ERROR(-20001, 'Wszystkie parametry funkcji muszą być określone.');
    END IF;

    IF p_date_from > p_date_to THEN
        RAISE_APPLICATION_ERROR(-20002, 'Data początkowa nie może być większa niż data końcowa.');
    END IF;


    OPEN participants_cursor FOR
        SELECT * FROM TRIP WHERE COUNTRY = p_country AND TRIP_DATE > p_date_from AND TRIP_DATE < p_date_to;
    RETURN participants_cursor;
end;
```

Czy kontrola parametrów w przypadku funkcji ma sens?
- jakie są zalety/wady takiego rozwiązania?

Zalety:
1. Bezpieczeństwo: Kontrola parametrów pozwala zapobiec wykonaniu funkcji z nieprawidłowymi danymi lub unieważnionymi wartościami parametrów, co może prowadzić do błędów lub niewłaściwych wyników.

2. Ochrona danych: Poprawna kontrola parametrów może chronić dane w bazie przed błędnym dostępem lub zmianami spowodowanymi przez nieprawidłowe parametry.

3. Poprawność danych: Zapewnienie, że funkcja otrzymuje poprawne dane, pomaga zachować integralność danych w systemie.

Wady:
1. Złożoność kodu: Dodanie kontroli parametrów może zwiększyć złożoność kodu funkcji, co może prowadzić do większej liczby linii kodu i trudniejszej analizy i debugowania.

2. Wydajność: Długotrwałe lub złożone kontrole parametrów mogą wpływać na wydajność funkcji, zwłaszcza gdy są wywoływane wielokrotnie w złożonych zapytaniach.


## Zadanie 3. Procedury

- pomocnicza funkcja **f_get_reserved_places_counter** - zwraca liczbę zarezerwowanych miejsc na daną wycieczkę podając jej id
```sql
create or replace function f_get_reserved_places(a_trip_id int)  
return int  
is  
  s_reserved_places int;  
begin  
 select count(RESERVATION_ID) into s_reserved_places  
    from RESERVATION r  
 where r.TRIP_ID = a_trip_id and r.status in ('N', 'P');  
    return s_reserved_places;  
end;
```
---
- pomocnicza funkcja **f_check_free_places** - zwraca liczbę wolnych miejsc na daną wycieczkę podając jej id
```sql
create or replace function f_check_free_places(a_trip_id int)  
return int  
is  
  s_free_places int;  
begin  
 select MAX_NO_PLACES - f_get_reserved_places(a_trip_id)  
    into s_free_places  
    from TRIP;  
    return s_free_places;  
end;
```
---
- **p_add_reservation** - dopisanie nowej rezerwacji
```sql
create or replace procedure p_add_reservation(a_trip_id int, a_person_id int)  
as  
  s_trip_date date;  
    s_count int;  
    s_reservation_id int;  
begin  
  -- Sprawdzenie czy osoba istnieje w systemie  
  select count(*) into s_count from PERSON where PERSON_ID = a_person_id;  
    if s_count = 0 then RAISE_APPLICATION_ERROR(-20001, 'Nie istnieje osoba o podanym ID.');  
    end if;  
  
    -- Sprawdzenie czy wycieczka istnieje w systemie  
  select count(*) into s_count from TRIP where TRIP_ID = a_trip_id;  
    if s_count = 0 then RAISE_APPLICATION_ERROR(-20002, 'Wycieczka o podanym ID nie istnieje.');  
    end if;  
  
    -- Sprawdzenie czy wycieczka się już nie odbyła  
  select TRIP_DATE into s_trip_date from TRIP t where t.TRIP_ID = a_trip_id;  
    DBMS_OUTPUT.PUT_LINE('Data wycieczki: ' || s_trip_date);  
    if s_trip_date < SYSDATE then RAISE_APPLICATION_ERROR(-20003, 'Wycieczka już się odbyła.');  
    end if;  
  
    -- Sprawdzenie czy osoba jest już zapisana na tą wycieczkę  
  select COUNT(*) into s_count from RESERVATION  
    where TRIP_ID = a_trip_id and PERSON_ID = a_person_id;  
    if s_count > 0 then RAISE_APPLICATION_ERROR(-20004, 'Ta osoba jest już zapisana na tę wycieczkę.');  
    end if;  
  
    -- Sprawdzenie czy jest wolne miejsce  
  if f_check_free_places(a_trip_id) <= 0 then  
  RAISE_APPLICATION_ERROR(-20005, 'Brak wolnych miejsc na wycieczce.');  
    end if;  
  
    -- Wstawienie rekordu do RESERVATION i pobranie RESERVATION_ID  
  insert into RESERVATION (TRIP_ID, PERSON_ID, STATUS)  
    values (a_trip_id, a_person_id, 'N')  
    returning RESERVATION_ID into s_reservation_id;  
  
    -- Wstawienie rekordu do LOG  
  insert into LOG (RESERVATION_ID, LOG_DATE, STATUS)  
    values (s_reservation_id, SYSDATE, 'N');  
  
    commit;  
    DBMS_OUTPUT.PUT_LINE('Rezerwacja została pomyślnie dodana.');  
exception  
 when others then rollback;  
        DBMS_OUTPUT.PUT_LINE('Wystąpił błąd: ' || SQLERRM);  
end;
```
---
- **p_modify_reservation_status** - zmiana statusu rezerwacji
```sql
create or replace procedure p_modify_reservation_status(a_reservation_id int, a_status char(1))  
as  
  s_trip_id int;  
    s_curr_status char(1);  
    s_trip_date date;  
begin  
  -- Poprawność argumentu a_status  
  if a_status not in ('N', 'P', 'C') then  
  RAISE_APPLICATION_ERROR(-20001, 'Niepoprawny status.');  
    end if;  
  
    -- Pobranie TRIP_ID i STATUS  
  select TRIP_ID, STATUS into s_trip_id, s_curr_status  
    from RESERVATION where RESERVATION_ID = a_reservation_id;  
  
    -- Sprawdzenie istnienia rezerwacji  
  if s_trip_id is null then  
  RAISE_APPLICATION_ERROR(-20002, 'Rezerwacja o podanym ID nie istnieje.');  
    end if;  
  
    -- Sprawdzenie czy rezerwacja nie ma już podanego statusu  
  if s_curr_status = a_status then  
  RAISE_APPLICATION_ERROR(-20001, 'Rezerwacja ma już ten status.');  
    end if;  
  
    if a_status = 'C' then -- anulowanie rezerwacji  
  update RESERVATION set STATUS = a_status where RESERVATION_ID = a_reservation_id;  
        insert into LOG (RESERVATION_ID, LOG_DATE, STATUS) values (a_reservation_id, SYSDATE, a_status);  
        DBMS_OUTPUT.PUT_LINE('Twoja rezerwacja została anulowana.');  
        return;  
    end if;  
  
    if s_curr_status = 'C' then  
  -- Data wycieczki  
  select TRIP_DATE into s_trip_date from TRIP  
        where TRIP_ID = s_trip_id;  
  
        -- Sprawdzenie czy wycieczka się już nie odbyła  
  if s_trip_date < SYSDATE then  
  RAISE_APPLICATION_ERROR(-20003, 'Wycieczka już się odbyła. Nie można zmienić statusu');  
        end if;  
  
        -- Sprawdzenie czy jest wolne miejsce  
  if f_check_free_places(s_trip_id) <= 0 then  
  RAISE_APPLICATION_ERROR(-20005, 'Brak wolnych miejsc na wycieczce.');  
        end if;  
  
        update RESERVATION set STATUS = a_status where RESERVATION_ID = a_reservation_id;  
        insert into LOG (RESERVATION_ID, LOG_DATE, STATUS) values (a_reservation_id, SYSDATE, a_status);  
        DBMS_OUTPUT.PUT_LINE('Status twojej rezerwacji został zaaktualizowany.');  
        return;  
    end if;  
  
    if a_status = 'P' then  
 update RESERVATION set STATUS = a_status where RESERVATION_ID = a_reservation_id;  
        insert into LOG (RESERVATION_ID, LOG_DATE, STATUS) values (a_reservation_id, SYSDATE, a_status);  
        DBMS_OUTPUT.PUT_LINE('Twoje miejsce jest już potwierdzone i zapłacone.');  
    end if;  
end;
```
---
- **p_modify_max_no_places** - zmiana maksymalnej liczby miejsc na daną wycieczkę
```sql
create or replace procedure p_modify_max_no_places(a_trip_id int, a_max_no_places int)  
as  
  s_count int;  
begin  
 if a_max_no_places <= 0 then  
  RAISE_APPLICATION_ERROR(-20001, 'Proszę podać poprawną liczbę');  
    end if;  
  
    select count(*) into s_count from TRIP WHERE TRIP_ID = a_trip_id;  
    if s_count = 0 then  
  RAISE_APPLICATION_ERROR(-20002, 'Nie istnieje wycieczka o podanym ID');  
    end if;  
  
    if f_get_reserved_places(a_trip_id) > a_max_no_places then  
  RAISE_APPLICATION_ERROR(-20003, 'Nie można zmiejszyć liczby miejsc poniżej liczby zarezerwowanych');  
    end if;  
  
    update TRIP  
    set MAX_NO_PLACES = a_max_no_places where TRIP_ID = a_trip_id;  
    commit;  
exception  
 when others then rollback;  
        raise;  
end;
```
---

## Zadanie 4. Triggery

- **trg_reservation_log** - tworzy log'a przy dodaniu / aktualizacji statusu rezerwacji
```sql
create or replace trigger trg_reservation_log
after insert or update on RESERVATION
for each row
begin
    if :OLD.STATUS != :NEW.STATUS then
        insert into LOG (RESERVATION_ID, LOG_DATE, STATUS)
    values (:NEW.RESERVATION_ID, SYSDATE, :NEW.STATUS);
    end if;
end;
```
---
- **trg_prevent_reservation_deletion** - blokuje możliwość usuwania rezerwacji
```sql
create or replace trigger trg_prevent_reservation_deletion
before delete on RESERVATION
for each row 
begin
    RAISE_APPLICATION_ERROR(-20001, 'Usunięcie rezerwacji jest zabronione.');
end;
```
---
- **Aktualizacja procedur** polega na usunięciu wierszów z dodawaniem do log'ów
#### Z procedury **p_add_reservation** usuwamy zmienną *s_reservation_id* oraz zmieniamy:
```sql
  -- Wstawienie rekordu do RESERVATION i pobranie RESERVATION_ID  
  insert into RESERVATION (TRIP_ID, PERSON_ID, STATUS)  
  values (a_trip_id, a_person_id, 'N')  
  returning RESERVATION_ID into s_reservation_id;  
  
  -- Wstawienie rekordu do LOG  
  insert into LOG (RESERVATION_ID, LOG_DATE, STATUS)  
  values (s_reservation_id, SYSDATE, 'N');  
```
#### na:
```sql
  -- Wstawienie rekordu do RESERVATION i pobranie RESERVATION_ID
  insert into RESERVATION (TRIP_ID, PERSON_ID, STATUS)
  values (a_trip_id, a_person_id, 'N');
```

#### Natomiast z procedury **p_modify_reservation_status** usuwamy 3 takie wiersze:
```sql
insert into LOG (RESERVATION_ID, LOG_DATE, STATUS) values (a_reservation_id, SYSDATE, a_status);  
```
---

## Zadanie 5. Triggery

- **trg_insert_reservation** - sprawdza czy jest wolne miejsce do nowej rezerwacji
```sql
create or replace trigger trg_insert_reservation
before insert on RESERVATION
for each row
begin
    if f_check_free_places(:NEW.TRIP_ID) <= 0 then
        RAISE_APPLICATION_ERROR(-20005, 'Brak wolnych miejsc na wycieczce.');
    end if;
end;
```
---
- **trg_update_reservation_status** - sprawdza czy jest wolne miejsce do odnowienia rezerwacji ze statusu anulowanej 'C' na nową 'N' / zapłaconą 'P'
```sql
create or replace trigger trg_update_reservation_status
before update on RESERVATION
for each row
begin
    if :OLD.STATUS = 'C' and f_check_free_places(:NEW.TRIP_ID) <= 0 then
        RAISE_APPLICATION_ERROR(-20005, 'Brak wolnych miejsc na wycieczce.');
    end if;
end;
```
---
- **Aktualizacja procedur** polega na usunięciu fragmentów ze sprawdzania wolnych miejsc
#### Z procedury **p_add_reservation** usuwamy ten fragment:
```sql
  -- Sprawdzenie czy jest wolne miejsce
  if f_check_free_places(a_trip_id) <= 0 then
    RAISE_APPLICATION_ERROR(-20005, 'Brak wolnych miejsc na wycieczce.');
  end if;
```
#### Z procedury **p_modify_reservation_status** usuwamy ten fragment:
```sql
  -- Sprawdzenie czy jest wolne miejsce  
  if f_check_free_places(s_trip_id) <= 0 then  
    RAISE_APPLICATION_ERROR(-20005, 'Brak wolnych miejsc na wycieczce.');  
  end if;
```
---

## Zadanie 6.


#### Modyfikacja procedury p_add_reservation:
```sql
create or replace procedure p_add_reservation_6(a_trip_id int, a_person_id int)
as
  s_trip_date date;
  s_count int;
  s_reservation_id int;
  s_available_places int;
begin
  -- Sprawdzenie czy osoba istnieje w systemie
  select count(*) into s_count from PERSON where PERSON_ID = a_person_id;
    if s_count = 0 then RAISE_APPLICATION_ERROR(-20001, 'Nie istnieje osoba o podanym ID.');
    end if;

    -- Sprawdzenie czy wycieczka istnieje w systemie
  select count(*) into s_count from TRIP where TRIP_ID = a_trip_id;
    if s_count = 0 then RAISE_APPLICATION_ERROR(-20002, 'Wycieczka o podanym ID nie istnieje.');
    end if;

    -- Sprawdzenie czy wycieczka się już nie odbyła
  select TRIP_DATE into s_trip_date from TRIP t where t.TRIP_ID = a_trip_id;
    DBMS_OUTPUT.PUT_LINE('Data wycieczki: ' || s_trip_date);
    if s_trip_date < SYSDATE then RAISE_APPLICATION_ERROR(-20003, 'Wycieczka już się odbyła.');
    end if;

    -- Sprawdzenie czy osoba jest już zapisana na tą wycieczkę
  select COUNT(*) into s_count from RESERVATION
    where TRIP_ID = a_trip_id and PERSON_ID = a_person_id;
    if s_count > 0 then RAISE_APPLICATION_ERROR(-20004, 'Ta osoba jest już zapisana na tę wycieczkę.');
    end if;

  select NO_AVAILABLE_PLACES
  into s_available_places
  from TRIP
  where TRIP_ID = a_trip_id;

  if (s_available_places <= 0) then
        RAISE_APPLICATION_ERROR(-20005, 'Brak wolnych miejsc na wycieczce.');
  end if;

    -- Wstawienie rekordu do RESERVATION i pobranie RESERVATION_ID
  insert into RESERVATION (TRIP_ID, PERSON_ID, STATUS)
    values (a_trip_id, a_person_id, 'N')
    returning RESERVATION_ID into s_reservation_id;

    -- Wstawienie rekordu do LOG
  insert into LOG (RESERVATION_ID, LOG_DATE, STATUS)
    values (s_reservation_id, SYSDATE, 'N');

    commit;
    DBMS_OUTPUT.PUT_LINE('Rezerwacja została pomyślnie dodana.');
exception
 when others then rollback;
        DBMS_OUTPUT.PUT_LINE('Wystąpił błąd: ' || SQLERRM);
end;
```

#### Modyfikacja procedury p_modify_reservation_status:
```sql

```


#### Modyfikacja procedury p_modify_max_no_places:
```sql
create or replace procedure p_modify_max_no_places_6(a_trip_id int, a_max_no_places int)
as
  s_count int;
  s_available_places int;
  s_max_no_places int;
begin
  if a_max_no_places <= 0 then
  RAISE_APPLICATION_ERROR(-20001, 'Proszę podać poprawną liczbę');
    end if;

    select count(*) into s_count from TRIP WHERE TRIP_ID = a_trip_id;
    if s_count = 0 then
  RAISE_APPLICATION_ERROR(-20002, 'Nie istnieje wycieczka o podanym ID');
    end if;

  select NO_AVAILABLE_PLACES
  into s_available_places
  from TRIP
  where TRIP_ID = a_trip_id;

  select MAX_NO_PLACES
  into s_max_no_places
  from TRIP
  where TRIP_ID = a_trip_id;

    if s_max_no_places - s_available_places > a_max_no_places then
  RAISE_APPLICATION_ERROR(-20003, 'Nie można zmiejszyć liczby miejsc poniżej liczby zarezerwowanych');
    end if;

    UPDATE TRIP
    SET MAX_NO_PLACES = a_max_no_places,
        NO_AVAILABLE_PLACES = s_available_places - s_max_no_places + a_max_no_places
    WHERE TRIP_ID = a_trip_id;
    commit;
exception
 when others then rollback;
        raise;
end;
```


## Zadanie 6a.


## Zadanie 6b.


## Zadanie 7.
