from flask import Flask, jsonify, Blueprint, request, render_template
from base import execute_querry, call_procedure, call_function, execute_and_render, get_table_data


views_blueprint = Blueprint('views', __name__)

views = (
    ('views.VW_MOVIE_POPULARITY', 'Movie Popularity'),
    ('views.VW_CURRENT_RESERVATIONS', 'Current Reservations'),
    ('views.VW_AVAILABLE_COPIES', 'Available Copies'),
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
    

@views_blueprint.route('/VW_AVAILABLE_COPIES')
def VW_AVAILABLE_COPIES():
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


@views_blueprint.route('/filter_movies', methods=['GET', 'POST'])
def filter_movies():
    if request.method == 'POST':
        category_id = request.form['category_id']
        result = call_function('f_get_movies_by_category', [int(category_id)])
        
        if 'error' in result:
            return f"Error: {result['error']}", 500
        else:
            movies = result
    else:
        movies = get_all_movies()

    return render_template('views/movie_filter_form.html', categories=get_categories(), movies=movies)

def get_all_movies():
    query = "SELECT * FROM vw_movies_with_category"
    movies = execute_querry(query)
    return movies

def get_categories():
    query = "SELECT category_id, name FROM Categories"
    categories = execute_querry(query)
    return categories
