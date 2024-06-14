from flask import Flask, Blueprint, request, render_template, redirect, url_for
from base import execute_querry, call_procedure


procedures_blueprint = Blueprint('procedures', __name__)

@procedures_blueprint.route('/reserve', methods=['POST'])
def reserve():
    copy_id = request.form['copy_id']
    return render_template('procedures/reservation_form.html', copy_id=copy_id)


@procedures_blueprint.route('/add_reservation', methods=['POST'])
def add_reservation():
    client_id = request.form['client_id']
    copy_id = request.form['copy_id']
    rental_duration = request.form['rental_duration']
    
    result = call_procedure('p_add_reservation', [int(client_id), int(copy_id), int(rental_duration)])
    
    if 'error' in result:
        return "Error: " + result['error'], 500
    else:
        return redirect(url_for('views.VW_AVAILABLE_COPIES'))



@procedures_blueprint.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    client_id = request.form.get('data-client-id')  # Odczytaj client_id z atrybutu data-client-id

    if client_id is None:
        return "Error: Client ID is missing", 400
    
    new_status = 'C'

    result = call_procedure('p_change_reservation_status', [int(reservation_id), new_status])
    if 'error' in result:
        return "Error: " + result['error'], 500
    else:
        return redirect(url_for('functions.client_reservations', client_id=client_id))


@procedures_blueprint.route('/rent_movie_form', methods=['GET'])
def rent_movie_form():
    return render_template('functions/rent_movie_form.html')

@procedures_blueprint.route('/rental', methods=['POST'])
def rental():
    client_id = request.form['client_id']
    copy_id = request.form['copy_id']
    rental_duration = request.form['rental_duration']

    result = call_procedure('p_add_new_rental', [int(client_id), int(copy_id), int(rental_duration)])
    
    if 'error' in result:
        return "Error: " + result['error'], 500
    else:
        return redirect('http://localhost:5000')
    


@procedures_blueprint.route('/return_movie_form', methods=['GET'])
def return_movie_form():
    return render_template('procedures/return_movie_form.html')


@procedures_blueprint.route('/return_movie', methods=['POST'])
def return_movie():
    rental_id = request.form['rental_id']

    result = call_procedure('P_RETURN_RENTAL', [int(rental_id)])
    
    if 'error' in result:
        return "Error: " + result['error'], 500
    else:
        return redirect('http://localhost:5000')
