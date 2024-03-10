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

- **p_add_reservation** - dopisanie nowej rezerwacji
```sql

```
- **p_modify_reservation_status** - zmiana statusu rezerwacji
```sql

```
parametry: reservation_id, status
procedura powinna kontrolować czy możliwa jest zmiana statusu, np. zmiana statusu już anulowanej wycieczki (przywrócenie do stanu
aktywnego nie zawsze jest możliwa – może już nie być miejsc)
procedura powinna również dopisywać inf. do tabeli log

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

## Zadanie 4. Triggery

## Zadanie 5. Triggery

## Zadanie 6.

## Zadanie 6a.

## Zadanie 6b.

## Zadanie 7.
