from flask import Flask, jsonify, Blueprint
from base import execute_querry

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
    


