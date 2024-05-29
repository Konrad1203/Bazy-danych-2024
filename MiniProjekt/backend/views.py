from flask import Flask, jsonify, Blueprint, request
from base import execute_querry, conn

app = Flask(__name__)

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/VW_MOVIE_POPULARITY')
def VW_MOVIE_POPULARITY():
    result = execute_querry("select * from VW_MOVIE_POPULARITY")
    if 'error' in result:
        return execute_querry('error.html', message='Wystąpił błąd: ' + result['error']), 500
    else:
        return result
    

@views_blueprint.route('/VW_CURRENT_RESERVATIONS')
def VW_CURRENT_RESERVATIONS():
    result = execute_querry("select * from VW_CURRENT_RESERVATIONS")
    if 'error' in result:
        return execute_querry('error.html', message='Wystąpił błąd: ' + result['error']), 500
    else:
        return result
    

@views_blueprint.route('/VW_AVAILABLE_COPIES')
def VW_AVAILABLE_COPIES():
    result = execute_querry("select * from VW_AVAILABLE_COPIES")
    if 'error' in result:
        return execute_querry('error.html', message='Wystąpił błąd: ' + result['error']), 500
    else:
        return result
    


@views_blueprint.route('/VW_ACTOR_RENTALS')
def VW_ACTOR_RENTALS():
    result = execute_querry("select * from VW_ACTOR_RENTALS")
    if 'error' in result:
        return execute_querry('error.html', message='Wystąpił błąd: ' + result['error']), 500
    else:
        return result
    
#chwilowo tutaj, potem przeniesc w inny moduł
@views_blueprint.route('/rent_movie', methods=['POST'])
def rent_movie():
    data = request.json
    try:
        movie_id = data['movie_id']
        user_id = data['user_id']

        sql_check_availability = f"SELECT count(*) FROM COPIES WHERE movie_id = {movie_id} AND available = 1"
        available_copies = execute_querry(sql_check_availability)
        
        if available_copies[0][0] > 0:
            sql_update_copy = f"UPDATE COPIES SET available = 0 WHERE movie_id = {movie_id} AND available = 1 AND rownum = 1"
            execute_querry(sql_update_copy)
            
            sql_rent_movie = f"INSERT INTO RENTALS (user_id, movie_id, rent_date) VALUES ({user_id}, {movie_id}, SYSDATE)"
            execute_querry(sql_rent_movie)
            
            conn.commit()
            return jsonify({"message": "Movie rented successfully"}), 200
        else:
            return jsonify({"message": "No available copies for this movie"}), 400
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@views_blueprint.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.json
    try:
        title = data['title']
        genre = data['genre']
        release_date = data['release_date']

        sql = f"INSERT INTO MOVIES (title, genre, release_date) VALUES ('{title}', '{genre}', TO_DATE('{release_date}', 'YYYY-MM-DD'))"
        execute_querry(sql)
        conn.commit()
        return jsonify({"message": "Movie added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@views_blueprint.route('/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        sql = f"DELETE FROM MOVIES WHERE id = {movie_id}"
        execute_querry(sql)
        conn.commit()
        return jsonify({"message": "Movie deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
