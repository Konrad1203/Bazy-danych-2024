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
  f_person_reservations
zadaniem funkcji jest zwrócenie listy rezerwacji danej osoby
parametry funkcji: person_id
funkcja zwraca podobny zestaw danych jak widok vw_reservation
  f_available_trips_to
zadaniem funkcji jest zwrócenie listy wycieczek do wskazanego kraju, dostępnych w zadanym okresie czasu (od date_from do
date_to)
parametry funkcji: country, date_from, date_to


## Zadanie 3. Procedury

- **p_add_reservation** - dopisanie nowej rezerwacji
 ```sql
create or replace procedure p_add_reservation(a_trip_id int, a_person_id int)  
as  
  s_trip_date date;  
    s_count int;  
    s_free_places int;  
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
  select MAX_NO_PLACES - count(RESERVATION_ID)  
    into s_free_places  
    from TRIP t  
    left join RESERVATION r on t.TRIP_ID = r.TRIP_ID  
  where t.TRIP_ID = a_trip_id and r.STATUS = 'P'  
  group by t.TRIP_ID, t.MAX_NO_PLACES;  
    DBMS_OUTPUT.PUT_LINE('Liczba wolnych miejsc: ' || s_free_places);  
    if s_free_places <= 0 then RAISE_APPLICATION_ERROR(-20005, 'Brak wolnych miejsc na wycieczce.');  
    end if;  
  
    -- Wstawienie rekordu do RESERVATION  
  insert into RESERVATION (TRIP_ID, PERSON_ID, STATUS)  
    values (a_trip_id, a_person_id, 'N');  
  
    --Pobranie RESERVATION_ID  
  select RESERVATION_ID into s_reservation_id from RESERVATION  
    where TRIP_ID = a_trip_id and PERSON_ID = a_person_id;  
  
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

- **p_modify_reservation_tatus** - zmiana statusu rezerwacji

parametry: reservation_id, status
procedura powinna kontrolować czy możliwa jest zmiana statusu, np. zmiana statusu już anulowanej wycieczki (przywrócenie do stanu
aktywnego nie zawsze jest możliwa – może już nie być miejsc)
procedura powinna również dopisywać inf. do tabeli log

- **p_modify_max_no_places** - zmiana maksymalnej liczby miejsc na daną wycieczkę

parametry: trip_id, max_no_places
nie wszystkie zmiany liczby miejsc są dozwolone, nie można zmniejszyć liczby miejsc na wartość poniżej liczby zarezerwowanych miejsc


## Zadanie 4. Triggery


## Zadanie 5. Triggery


## Zadanie 6.


## Zadanie 6a.


## Zadanie 6b.


## Zadanie 7.
