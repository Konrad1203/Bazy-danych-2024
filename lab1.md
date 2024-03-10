# Zadanie 0.
  Skomentuj dzialanie transakcji. Jak działa polecenie commit, rollback?. Co się dzieje w przypadku wystąpienia błędów podczas wykonywania
transakcji? Porównaj sposób programowania operacji wykorzystujących transakcje w Oracle PL/SQL ze znanym ci systemem/językiem MS
Sqlserver T-SQL

# Zadanie 1. Widoki
  vw_reservation widok łączy dane z tabel: trip, person, reservation
zwracane dane: reservation_id, country, trip_date, trip_name, firstname, lastname, status, trip_id, person_id
  vw_trip widok pokazuje liczbę wolnych miejsc na każdą wycieczkę
zwracane dane: trip_id, country, trip_date, trip_name, max_no_places, no_available_places (liczba wolnych miejsc)
  vw_available_trip
podobnie jak w poprzednim punkcie, z tym że widok pokazuje jedynie dostępne wycieczki (takie które są w przyszłości i są na nie wolne miejsca)

# Zadanie 2. Funkcje
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

# Zadanie 3. Procedury
  p_add_reservation
zadaniem procedury jest dopisanie nowej rezerwacji
parametry: trip_id, person_id,
procedura powinna kontrolować czy wycieczka jeszcze się nie odbyła, i czy sa wolne miejsca
procedura powinna również dopisywać inf. do tabeli log
  p_modify_reservation_tatus
zadaniem procedury jest zmiana statusu rezerwacji
parametry: reservation_id, status
procedura powinna kontrolować czy możliwa jest zmiana statusu, np. zmiana statusu już anulowanej wycieczki (przywrócenie do stanu
aktywnego nie zawsze jest możliwa – może już nie być miejsc)
procedura powinna również dopisywać inf. do tabeli log
  p_modify_max_no_places
zadaniem procedury jest zmiana maksymalnej liczby miejsc na daną wycieczkę
parametry: trip_id, max_no_places
nie wszystkie zmiany liczby miejsc są dozwolone, nie można zmniejszyć liczby miejsc na wartość poniżej liczby zarezerwowanych miejsc

# Zadanie 4. Triggery

# Zadanie 5. Triggery

# Zadanie 6.

# Zadanie 6a.

# Zadanie 6b.

# Zadanie 7.

  
