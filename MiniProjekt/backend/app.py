from flask import Flask, url_for
from base import connect_to_data_base
from views import views_blueprint
from procedures import procedures_blueprint
from functions import functions_blueprint

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

conn = connect_to_data_base()
app.register_blueprint(views_blueprint)
app.register_blueprint(procedures_blueprint)
app.register_blueprint(functions_blueprint)

# http://localhost:5000
@app.route('/')
def index():
    views = [
        ('views.VW_MOVIE_POPULARITY', 'Movie Popularity'),
        ('views.VW_CURRENT_RESERVATIONS', 'Current Reservations'),
        ('views.VW_AVAILABLE_COPIES', 'Available Copies'),
        ('views.VW_ACTOR_RENTALS', 'Actor Rentals'),
        ('views.filter_movies', 'Movies')
    ]
    
    functions = [
        ('functions.client_reservations', 'Client Reservations')
    ]

    links = []
    for view in views:
        links.append(f'<a href="{url_for(view[0])}">{view[1]}</a>')
    
    views_html = '<br>'.join(links)
    views_info_text = '<h2>Lista dostępnych widoków:</h2>'
    
    default_client_id = 1  # Ustaw domyślną wartość client_id
    functions_links = []
    for func in functions:
        url = url_for(func[0], client_id=default_client_id)
        functions_links.append(f'<a href="{url}">{func[1]}</a>')

    functions_html = '<br>'.join(functions_links)
    functions_info_text = '<h2>Lista dostępnych Funckji:</h2>'
    html_content = f"{views_info_text}{views_html}<br><br>{functions_info_text}{functions_html}"

    return html_content


if __name__ == '__main__':
    app.run(debug=True)
