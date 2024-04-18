# Dokumentowe bazy danych – MongoDB

ćwiczenie 2


---

**Imiona i nazwiska autorów:** Tomasz Furgała, Łukasz Zegar, Konrad Tendaj

--- 


## Yelp Dataset

- [www.yelp.com](http://www.yelp.com) - serwis społecznościowy – informacje o miejscach/lokalach
- restauracje, kluby, hotele itd. `businesses`,
- użytkownicy odwiedzają te miejsca - "meldują się"  `check-in`
- użytkownicy piszą recenzje `reviews` o miejscach/lokalach i wystawiają oceny oceny,
- przykładowy zbiór danych zawiera dane z 5 miast: Phoenix, Las Vegas, Madison, Waterloo i Edinburgh.

# Zadanie 1 - operacje wyszukiwania danych

Dla zbioru Yelp wykonaj następujące zapytania

W niektórych przypadkach może być potrzebne wykorzystanie mechanizmu Aggregation Pipeline

[https://www.mongodb.com/docs/manual/core/aggregation-pipeline/](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)


1. Zwróć dane wszystkich restauracji (kolekcja `business`, pole `categories` musi zawierać wartość "Restaurants"), które są otwarte w poniedziałki (pole hours) i mają ocenę co najmniej 4 gwiazdki (pole `stars`).  Zapytanie powinno zwracać: nazwę firmy, adres, kategorię, godziny otwarcia i gwiazdki. Posortuj wynik wg nazwy firmy.

2. Ile każda firma otrzymała ocen/wskazówek (kolekcja `tip` ) w 2012. Wynik powinien zawierać nazwę firmy oraz liczbę ocen/wskazówek Wynik posortuj według liczby ocen (`tip`).

3. Recenzje mogą być oceniane przez innych użytkowników jako `cool`, `funny` lub `useful` (kolekcja `review`, pole `votes`, jedna recenzja może mieć kilka głosów w każdej kategorii).  Napisz zapytanie, które zwraca dla każdej z tych kategorii, ile sumarycznie recenzji zostało oznaczonych przez te kategorie (np. recenzja ma kategorię `funny` jeśli co najmniej jedna osoba zagłosowała w ten sposób na daną recenzję)

4. Zwróć dane wszystkich użytkowników (kolekcja `user`), którzy nie mają ani jednego pozytywnego głosu (pole `votes`) z kategorii (`funny` lub `useful`), wynik posortuj alfabetycznie według nazwy użytkownika.

5. Wyznacz, jaką średnia ocenę uzyskała każda firma na podstawie wszystkich recenzji (kolekcja `review`, pole `stars`). Ogranicz do firm, które uzyskały średnią powyżej 3 gwiazdek.

	a) Wynik powinien zawierać id firmy oraz średnią ocenę. Posortuj wynik wg id firmy.

	b) Wynik powinien zawierać nazwę firmy oraz średnią ocenę. Posortuj wynik wg nazwy firmy.

## Zadanie 1  - rozwiązanie

### 1. 
Zwróć dane wszystkich restauracji (kolekcja `business`, pole `categories` musi zawierać wartość "Restaurants"), które są otwarte w poniedziałki (pole hours) i mają ocenę co najmniej 4 gwiazdki (pole `stars`).  Zapytanie powinno zwracać: nazwę firmy, adres, kategorię, godziny otwarcia i gwiazdki. Posortuj wynik wg nazwy firmy.

```js
db.business.find({
  "categories": "Restaurants",
  "hours.Monday.open": { $exists: true },
  "stars": { $gte: 4 }
}, {
  "name": 1,
  "address": 1,
  "categories": 1,
  "hours.Monday": 1,
  "stars": 1,
  "_id": 0
}).sort({ "name": 1 })
```

![alt text](img/1_1.png)

### 2.
Ile każda firma otrzymała ocen/wskazówek (kolekcja `tip` ) w 2012. Wynik powinien zawierać nazwę firmy oraz liczbę ocen/wskazówek Wynik posortuj według liczby ocen (`tip`).
```js
db.tip.aggregate([
  {
    $match: {
      date: { $gte: "2012-01-01", $lt: "2013-01-01" }
    }
  },
  {
    $group: {
      _id: "$business_id",
      tipCount: { $sum: 1 }
    }
  },
  {
    $lookup: {
      from: "business",
      localField: "_id",
      foreignField: "business_id",
      as: "business_info"
    }
  },
  {
    $project: {
      _id: 0,
      business_name: { $arrayElemAt: ["$business_info.name", 0] },
      tipCount: 1
    }
  },
  {
    $sort: {
      tipCount: -1
    }
  }
])
```
##### Ze względu na zbyt duży rozmiar pliku `trip.json`, zaimportowaliśmy tylko część dokumentów w celu przetestowania agragacji.

![alt text](img/1_2.png)

### 3.
Recenzje mogą być oceniane przez innych użytkowników jako `cool`, `funny` lub `useful` (kolekcja `review`, pole `votes`, jedna recenzja może mieć kilka głosów w każdej kategorii).  Napisz zapytanie, które zwraca dla każdej z tych kategorii, ile sumarycznie recenzji zostało oznaczonych przez te kategorie (np. recenzja ma kategorię `funny` jeśli co najmniej jedna osoba zagłosowała w ten sposób na daną recenzję)
```js
db.review.aggregate([
  {
    $group: {
      _id: null,
      total_funny_reviews: {
        $sum: { $cond: [{ $gt: ["$votes.funny", 0] }, 1, 0] }
      },
      total_useful_reviews: {
        $sum: { $cond: [{ $gt: ["$votes.useful", 0] }, 1, 0] }
      },
      total_cool_reviews: {
        $sum: { $cond: [{ $gt: ["$votes.cool", 0] }, 1, 0] }
      }
    }
  }
])
```
##### Tutaj również zaimportowaliśmy tylko część dokumentów.

![alt text](img/1_3.png)

### 4.
Zwróć dane wszystkich użytkowników (kolekcja `user`), którzy nie mają ani jednego pozytywnego głosu (pole `votes`) z kategorii (`funny` lub `useful`), wynik posortuj alfabetycznie według nazwy użytkownika.
```js
db.user.aggregate([
  {
    $match: {
      $or: [
        { "votes.funny": { $eq: 0 } },
        { "votes.useful": { $eq: 0 } }
      ]
    }
  },
  {
    $sort: { "name": 1 }
  }
])
```
#### Tutaj również zaimportowaliśmy mniej danych
![alt text](img/1_4.png)
### 5
Wyznacz, jaką średnia ocenę uzyskała każda firma na podstawie wszystkich recenzji (kolekcja `review`, pole `stars`). Ogranicz do firm, które uzyskały średnią powyżej 3 gwiazdek.

### 5a
	a) Wynik powinien zawierać id firmy oraz średnią ocenę. Posortuj wynik wg id firmy.


```js
db.review.aggregate([
  {
    $group: {
      _id: "$business_id",
      average_rating: { $avg: "$stars" }
    }
  },
  {
    $match: {
      average_rating: { $gt: 3 }
    }
  },
  {
    $sort: { _id: 1 }
  }
])
```

![alt text](img/1_5a.png)


### 5b
	b) Wynik powinien zawierać nazwę firmy oraz średnią ocenę. Posortuj wynik wg nazwy firmy.
```js
db.review.aggregate([
  {
    $group: {
      _id: "$business_id",
      average_rating: { $avg: "$stars" }
    }
  },
  {
    $match: {
      average_rating: { $gt: 3 }
    }
  },
  {
    $lookup: {
      from: "business",
      localField: "_id",
      foreignField: "business_id",
      as: "business_info"
    }
  },
  {
    $unwind: "$business_info" 
  },
  {
    $project: {
      _id: 0,
      company_name: "$business_info.name", 
      average_rating: 1
    }
  },
  {
    $sort: { company_name: 1 } 
  }
])

```

![alt text](img/1_5b.png)

---

# Zadanie 2 - modelowanie danych


Zaproponuj strukturę bazy danych dla wybranego/przykładowego zagadnienia/problemu

Należy wybrać jedno zagadnienie/problem (A lub B)

Przykład A
- Wykładowcy, przedmioty, studenci, oceny
	- Wykładowcy prowadzą zajęcia z poszczególnych przedmiotów
	- Studenci uczęszczają na zajęcia
	- Wykładowcy wystawiają oceny studentom
	- Studenci oceniają zajęcia

Przykład B
- Firmy, wycieczki, osoby
	- Firmy organizują wycieczki
	- Osoby rezerwują miejsca/wykupują bilety
	- Osoby oceniają wycieczki

a) Warto zaproponować/rozważyć różne warianty struktury bazy danych i dokumentów w poszczególnych kolekcjach oraz przeprowadzić dyskusję każdego wariantu (wskazać wady i zalety każdego z wariantów)

b) Kolekcje należy wypełnić przykładowymi danymi

c) W kontekście zaprezentowania wad/zalet należy zaprezentować kilka przykładów/zapytań/zadań/operacji oraz dla których dedykowany jest dany wariantów

W sprawozdaniu należy zamieścić przykładowe dokumenty w formacie JSON ( pkt a) i b)), oraz kod zapytań/operacji (pkt c)), wraz z odpowiednim komentarzem opisującym strukturę dokumentów oraz polecenia ilustrujące wykonanie przykładowych operacji na danych

Do sprawozdania należy kompletny zrzut wykonanych/przygotowanych baz danych (taki zrzut można wykonać np. za pomocą poleceń `mongoexport`, `mongdump` …) oraz plik z kodem operacji zapytań (załącznik powinien mieć format zip).


## Zadanie 2  - rozwiązanie

Do realizacji wybraliśmy **problem B**, firmy wycieczki, osoby.
## a)
Rozważamy dwa róże podejścia w budowaniu struktury bazy danych.

**Pierwsze** składa się z trzech kolekcji : `Firmy`, `Wycieczki` i `Osoby`.
`Firmy` to kolekcja, która zawiera dane o firmach organizujących wycieczki. Kolekcja `Wycieczki` zawiera informacje o wycieczkach, w tym nazwę, opis, datę, cenę, firmę organizującą, oceny. `Osoby` zawiera informacje o osobach rezerwujących miejsca oraz oceniających wycieczki.

Zalety: 
- struktura prosta do czytania, zrozumienia jak i do implementacji,
- korzystamy z możliwości osadzania dokumentów z różnych kolekcji w jednym dokumencie,
- możemy w łatwy sposób pozyskać wszystkie potrzbne informacje np o osobie X jednym zapytaniem.

Wady:
- utrudnione akutalizowanie/dodanie danych,
- prowadzi do powielania danych,
- może być trudne do skalowania, gdy baza danych rośnie wraz z liczbą firm, wycieczek i osób.

**Drugi** składa się z czterech kolekcji: `Firmy`, `Wycieczki`, `Osoby` i `Rezerwacje`.
Kolekcje Firmy, Wycieczki, Osoby będą pełniły taką samą role jak w podejściu pierwszym. Natomiast kolekcja `Rezerwacje` będzie zawierać inforamcje o zapisie danej osoby na wycieczkę.

Zalety:
- minimalizacjia powielania danych,
- ułatwiona aktualizacja danych,
- lepsza skalowalność.

Wady:
- zapytania są bardziej skomlikowane, złożone,
- duża liczba referencji może spowodować spadek wydajności.


### Struktura kolekcji.

##### Companies:
```json
{
  "company_id": "indetyfikator",
  "company_name": "Nazwa firmy"
}
```

#### Persons:
```json
{
  "user_id": "indetyfikator",
  "name": "Name of the person"
}
```
### Wariant 1:

#### Trips
```json
{
  "tour_id": "indetyfikator",
  "tour_name":  "nazwa wycieczki",
  "date": "data",
  "price": "Cena",
  "company_id": "indetyfikator firmy",
  "ratings": [
    {
      "user_id": "identyfikator osoby",
      "rating": "ocena"
    },
  ],
  "reservations": [
    {
      "user_id": "identyfikator osoby",
      "date": "data rezerwacji"
    },
  ]
}
```

### Wariant 2:

#### Trips
```json
{
  "tour_id": "indetyfikator",
  "tour_name":  "nazwa wycieczki",
  "date": "data",
  "price": "Cena",
  "company_id": "indetyfikator firmy",
  "ratings": [
    {
      "user_id": "identyfikator osoby",
      "rating": "ocena"
    }
  ]
}
```

#### Reservations
```json
{
  "reservation_id": "indetyfikator",
  "tour_id": "indetyfikator wycieczki",
  "user_id": "identyfikator osoby",
  "date": "data rezerwacji"
}
```

W celu przetestowania obu wariantów stworzyliśmy 2 bazy.

## b)

Przykładowe dane dla kolekcji `Companies` i `Persons`:
```mongodb
db.companies.insertMany([
  { company_id: "1", company_name: "Adventure Excursions Inc." },
  { company_id: "2", company_name: "Exploration Tours Ltd." },
  { company_id: "3", company_name: "Discover Destinations LLC" }
]);

db.persons.insertMany([
  { user_id: "101", name: "John Smith" },
  { user_id: "102", name: "Emily Johnson" },
  { user_id: "103", name: "Michael Brown" },
  { user_id: "104", name: "Jessica Davis" },
  { user_id: "105", name: "Christopher Wilson" },
  { user_id: "106", name: "Amanda Martinez" },
  { user_id: "107", name: "David Anderson" },
  { user_id: "108", name: "Jennifer Taylor" },
  { user_id: "109", name: "Daniel Thomas" },
  { user_id: "110", name: "Linda Garcia" }
]);
```

### Wariant 1:

```mongodb
db.tours.insertMany([
  {
    "tour_id": "1",
    "tour_name": "Excursion to Grand Canyon",
    "date": "2024-05-15",
    "price": 150,
    "company_id": "1",
    "ratings": [
      { "user_id": "105", "rating": 5 }
    ],
    "reservations": [
      { "user_id": "101", "date": "2024-05-10" },
      { "user_id": "105", "date": "2024-05-14" }
    ]
  },
  {
    "tour_id": "2",
    "tour_name": "Safari Adventure in Africa",
    "date": "2024-06-20",
    "price": 300,
    "company_id": "2",
    "ratings": [
      { "user_id": "106", "rating": 5 },
      { "user_id": "109", "rating": 5 }
    ],
    "reservations": [
      { "user_id": "108", "date": "2024-06-12" },
      { "user_id": "109", "date": "2024-06-14" }
    ]
  },
  {
    "tour_id": "3",
    "tour_name": "Historical Tour in Europe",
    "date": "2024-07-25",
    "price": 200,
    "company_id": "3",
    "ratings": [
      { "user_id": "106", "rating": 4 }
    ],
    "reservations": [
      { "user_id": "106", "date": "2024-07-24" }
    ]
  }
]);
```

### Wariant 2:

```mongodb
db.tours.insertMany([
  {
    "tour_id": "1",
    "tour_name": "Excursion to Grand Canyon",
    "date": "2024-05-15",
    "price": 150,
    "company_id": "1",
    "ratings": [
      { "user_id": "105", "rating": 5 }
    ]
  },
  {
    "tour_id": "2",
    "tour_name": "Safari Adventure in Africa",
    "date": "2024-06-20",
    "price": 300,
    "company_id": "2",
    "ratings": [
      { "user_id": "106", "rating": 5 },
      { "user_id": "109", "rating": 5 }
    ]
  },
  {
    "tour_id": "3",
    "tour_name": "Historical Tour in Europe",
    "date": "2024-07-25",
    "price": 200,
    "company_id": "3",
    "ratings": [
      { "user_id": "106", "rating": 4 }
    ]
  }
]);
```

```mongodb
db.reservations.insertMany([
  {
    "reservation_id": "1",
    "tour_id": "1",
    "user_id": "101", 
    "date": "2024-05-10" 
  },
  {
    "reservation_id": "2",
    "tour_id": "1",
    "user_id": "105", 
    "date": "2024-05-14" 
  },
  {
    "reservation_id": "3",
    "tour_id": "2",
    "user_id": "108", 
    "date": "2024-06-12"
  },
  {
    "reservation_id": "4",
    "tour_id": "2",
    "user_id": "109", 
    "date": "2024-06-14" 
  },
  {
    "reservation_id": "5",
    "tour_id": "3",
    "user_id": "106", 
    "date": "2024-07-24"
  }
]);
```

## c)

#### Dodanie nowej rezerwacji:

##### Wariant 1:

```mongodb
db.tours.updateOne(
  { 
    "tour_id": "1"
  },
  {
    $addToSet: {
      "reservations": { "user_id": "103", "date": "2024-05-11" }
    }
  }
);
```

##### Wariant 2:
```mongodb
db.reservations.insertOne({
  "reservation_id": "6",
  "tour_id": "1",
  "user_id": "103", 
  "date": "2024-05-11" 
});
```


---

Punktacja:

|         |     |
| ------- | --- |
| zadanie | pkt |
| 1       | 0,6 |
| 2       | 1,4 |
| razem   | 2   |



