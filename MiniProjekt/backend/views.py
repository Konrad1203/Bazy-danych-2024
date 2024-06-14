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


#chwilowo tutaj, potem przeniesc w inny moduł
@views_blueprint.route('/rent_movie', methods=['POST'])
def rent_movie():
    data = request.json
    try:
        movie_id = data['movie_id']
        user_id = data['user_id']

        sql_check_availability = f"SELECT count(*) FROM COPIES WHERE movie_id = {movie_id} AND available = 1"
        available_copies = execute_querry(sql_check_availability, True)
        
        if available_copies[0][0] > 0:
            sql_update_copy = f"UPDATE COPIES SET available = 0 WHERE movie_id = {movie_id} AND available = 1 AND rownum = 1"
            execute_querry(sql_update_copy, True)
            
            sql_rent_movie = f"INSERT INTO RENTALS (user_id, movie_id, rent_date) VALUES ({user_id}, {movie_id}, SYSDATE)"
            execute_querry(sql_rent_movie, True)
            
            # conn.commit()
            return jsonify({"message": "Movie rented successfully"}), 200
        else:
            return jsonify({"message": "No available copies for this movie"}), 400
        
    except Exception as e:
        # conn.rollback()
        return jsonify({"error": str(e)}), 500


@views_blueprint.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.json
    try:
        title = data['title']
        genre = data['genre']
        release_date = data['release_date']

        sql = f"INSERT INTO MOVIES (title, genre, release_date) VALUES ('{title}', '{genre}', TO_DATE('{release_date}', 'YYYY-MM-DD'))"
        execute_querry(sql, True)
        # conn.commit()
        return jsonify({"message": "Movie added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@views_blueprint.route('/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        sql = f"DELETE FROM MOVIES WHERE id = {movie_id}"
        execute_querry(sql, True)
        # conn.commit()
        return jsonify({"message": "Movie deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
