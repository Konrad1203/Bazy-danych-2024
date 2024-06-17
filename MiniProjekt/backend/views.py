from flask import Blueprint, request, render_template
from base import execute_and_render, get_table_data, call_function


views_blueprint = Blueprint('views', __name__)

views = (
    ('views.VW_MOVIE_POPULARITY', 'Movie Popularity'),
    ('views.VW_CURRENT_RESERVATIONS', 'Current Reservations'),
    ('views.VW_AVAILABLE_COPIES', 'Available Copies (filtrowanie, rezerwacja)'),
    ('views.VW_ACTOR_RENTALS', 'Actor Rentals'),
    ('views.VW_MOST_POPULAR_ACTORS_PER_CATEGORY', 'Actors Per Category'),
    ('views.VW_CLIENTS_DELAYS_SUM', 'Clients Delays Summary'),
    ('views.VW_CURRENTLY_BORROWED_COPIES', 'Currently Borrowed Copies'),
)

@views_blueprint.route('/VW_MOVIE_POPULARITY')
def VW_MOVIE_POPULARITY():
    return get_table_data('VW_MOVIE_POPULARITY', display_name='Movie Popularity')


@views_blueprint.route('/VW_CURRENT_RESERVATIONS')
def VW_CURRENT_RESERVATIONS():
    return get_table_data('VW_CURRENT_RESERVATIONS', display_name='Current Reservations')
    

@views_blueprint.route('/VW_AVAILABLE_COPIES', methods=['GET', 'POST'])   # dostępne kopie wyszukiwaniem i funkcją rezerwacji
def VW_AVAILABLE_COPIES():
    if request.method == 'GET':
        return execute_and_render("select * from VW_AVAILABLE_COPIES", 'views/available_copies.html', 'copies')
    
    movie_id = request.form.get('movie_id')
    movie_name = request.form.get('movie_name')
    print("Arguments:", movie_id, movie_name)

    if movie_id:
        print("Movie ID:", movie_id)
        result = call_function('f_get_available_copies_for_movie_id', [int(movie_id)])
        print("Result:", result)
        if 'error' in result:
            result = []
        return render_template('views/available_copies.html', copies=result)
    elif movie_name:
        print("Movie Name:", movie_name)
        result = call_function('f_get_available_copies_for_movie_name', [movie_name])
        print("Result:", result)
        if 'error' in result:
            result = []
        return render_template('views/available_copies.html', copies=result)
    else:
        return execute_and_render("select * from VW_AVAILABLE_COPIES", 'views/available_copies.html', 'copies')


@views_blueprint.route('/VW_ACTOR_RENTALS')
def VW_ACTOR_RENTALS():
    return get_table_data('VW_ACTOR_RENTALS', display_name='Actor Rentals')


@views_blueprint.route('/VW_MOST_POPULAR_ACTORS_PER_CATEGORY')
def VW_MOST_POPULAR_ACTORS_PER_CATEGORY():
    return get_table_data('VW_MOST_POPULAR_ACTORS_PER_CATEGORY', display_name='Most Popular Actors Per Category')


@views_blueprint.route('/VW_CLIENTS_DELAYS_SUM')
def VW_CLIENTS_DELAYS_SUM():
    return get_table_data('VW_CLIENTS_DELAYS_SUM',
                          display_name='Clients Delays Summary',
                          comment='This view displays the total days of delay for each client.')
    

@views_blueprint.route('/VW_CURRENTLY_BORROWED_COPIES')
def VW_CURRENTLY_BORROWED_COPIES():
    return get_table_data('VW_CURRENTLY_BORROWED_COPIES', 
                          display_name='Currently Borrowed Copies',
                          comment='This view displays all copies that are currently borrowed.')
