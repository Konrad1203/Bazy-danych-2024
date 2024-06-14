from flask import Flask, jsonify, Blueprint, request, render_template
from base import call_function


functions_blueprint = Blueprint('functions', __name__)

functions = (
        ('views.filter_movies', 'Search movies'),
        ('functions.client_reservations', 'Client Reservations'),
        ('procedures.rent_movie_form', 'Rent movie'),
        ('procedures.return_movie_form', 'Return movie'),
    )


@functions_blueprint.route('/client_reservations/<int:client_id>')
def client_reservations(client_id):
    result = call_function("f_get_client_reservations", [int(client_id)])
        
    if 'error' in result:
        return f"Wystąpił błąd: {result['error']}", 500
    else:
        return render_template('functions/get_client_reservations.html', reservations=result, client_id=client_id)

