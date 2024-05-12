from flask import Flask, jsonify, render_template
import cx_Oracle

app = Flask(__name__)


with open('MiniProjekt/backend/config.txt', 'r') as file:
    lines = file.readlines()

config_data = {}
for line in lines:
    key, value = line.strip().split(' = ')
    config_data[key] = value

lib_dir="C:\instantclient_21_13"
user = config_data['user']
password = config_data['password']
dsn = cx_Oracle.makedsn("dbmanage.lab.ii.agh.edu.pl", 1521, sid="DBMANAGE")

cx_Oracle.init_oracle_client(lib_dir="C:\instantclient_21_13")



def execute_query(sql):
    try:
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn, encoding="UTF-8")
        cursor = conn.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    except cx_Oracle.Error as error:
        return {'error': str(error)}

@app.route('/')
def index():
    result = execute_query("SELECT * FROM MOVIES")
    if 'error' in result:
        return render_template('error.html', message='Wystąpił błąd: ' + result['error']), 500
    else:
        return result
        table = '<table border="1"><tr><th>ID</th><th>Name</th><th>Email</th></tr>'
        for row in result:
            table += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(row[0], row[1], row[2])
        table += '</table>'
        return table
    
@app.route('/VW_MOVIE_POPULARITY')
def VW_MOVIE_POPULARITY():
    result = execute_query("select * from VW_MOVIE_POPULARITY")
    if 'error' in result:
        return render_template('error.html', message='Wystąpił błąd: ' + result['error']), 500
    else:
        return result
    

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

