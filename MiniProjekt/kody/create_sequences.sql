create sequence seq_clients_id
start with 1
increment by 1;

alter table Clients
modify client_id integer default seq_clients_id.nextval;


create sequence seq_reservation_id
start with 1
increment by 1;

alter table Reservation
modify reservation_id integer default seq_reservation_id.nextval;


create sequence seq_rental_id
start with 1
increment by 1;

alter table Rental
modify rental_id integer default seq_rental_id.nextval;


create sequence seq_copy_id
start with 1
increment by 1;

alter table Copy
modify copy_id integer default seq_copy_id.nextval;


create sequence seq_categories_id
start with 1
increment by 1;

alter table Categories
modify category_id integer default seq_categories_id.nextval;


create sequence seq_movies_id
start with 1
increment by 1;

alter table Movies
modify movie_id integer default seq_movies_id.nextval;


create sequence seq_actors_id
start with 1
increment by 1;

alter table Actors
modify actor_id integer default seq_actors_id.nextval;
