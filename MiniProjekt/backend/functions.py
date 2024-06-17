from flask import Blueprint, request, render_template, redirect, url_for
from base import call_function, execute_querry


functions_blueprint = Blueprint('functions', __name__)

functions = (
        ('functions.filter_movies', 'Search movies (po kategoriach)'),
        ('functions.client_reservations', 'Client Reservations (po id klienta)'),
        ('procedures.rent_movie_form', 'Rent movie (formularz do wypożyczania)'),
        ('procedures.return_movie_form', 'Return movie (formularz do zwrotów)'),
    )


@functions_blueprint.route('/filter_movies', methods=['GET', 'POST'])
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


@functions_blueprint.route('/client_reservations/<int:client_id>')
def client_reservations(client_id):
    result = call_function("f_get_client_reservations", [int(client_id)])
        
    if 'error' in result:
        return f"Wystąpił błąd: {result['error']}", 500
    else:
        return render_template('functions/get_client_reservations.html', reservations=result, client_id=client_id)

@functions_blueprint.route('/client_reservations', methods=['POST'])
def redirect_client_reservations():
    client_id = request.form.get('client_id')
    return redirect(url_for('functions.client_reservations', client_id=client_id))
