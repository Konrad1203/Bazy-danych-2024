from flask import Blueprint
from base import get_table_data


tables_blueprint = Blueprint('tables', __name__)

tables = (
    ('tables.get_Clients', 'Clients'),
    ('tables.get_Reservation', 'Reservation'),
    ('tables.get_Rental', 'Rental'),
    ('tables.get_Copy', 'Copy'),
    ('tables.get_Categories', 'Categories'),
    ('tables.get_Movies', 'Movies'),
    ('tables.get_Actors', 'Actors'),
    ('tables.get_Actors_in_movie', 'Actors_in_movie'),
)


@tables_blueprint.route('/tables/Clients')
def get_Clients():
    return get_table_data('Clients')

@tables_blueprint.route('/tables/Reservation')
def get_Reservation():
    return get_table_data('Reservation')

@tables_blueprint.route('/tables/Rental')
def get_Rental():
    return get_table_data('Rental')

@tables_blueprint.route('/tables/Copy')
def get_Copy():
    return get_table_data('Copy')

@tables_blueprint.route('/tables/Categories')
def get_Categories():
    return get_table_data('Categories')

@tables_blueprint.route('/tables/Movies')
def get_Movies():
    return get_table_data('Movies')

@tables_blueprint.route('/tables/Actors')
def get_Actors():
    return get_table_data('Actors')

@tables_blueprint.route('/tables/Actors_in_movie')
def get_Actors_in_movie():
    return get_table_data('Actors_in_movie')
