from flask import Flask, render_template
from base import connect_to_data_base
from tables import tables, tables_blueprint
from views import views, views_blueprint
from procedures import procedures_blueprint
from functions import functions, functions_blueprint


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

conn = connect_to_data_base()
app.register_blueprint(tables_blueprint)
app.register_blueprint(views_blueprint)
app.register_blueprint(procedures_blueprint)
app.register_blueprint(functions_blueprint)

# http://localhost:5000
@app.route('/')
def index():
    return render_template(
            'main.html',
            tables=tables,
            views=views,
            functions=functions,
            default_client_id=1   # Ustaw domyślną wartość client_id
            )


if __name__ == '__main__':
    app.run(debug=True)
