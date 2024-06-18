import cx_Oracle
from flask import render_template


global conn


def connect_to_data_base():
    global conn
    try:
        with open('MiniProjekt/backend/config.txt', 'r') as file:
            lines = file.readlines()

        config_data = {}

        for line in lines:
            key, value = line.strip().split(' = ')
            config_data[key] = value

        lib_dir = "C:/instantclient_21_13/"
        user = config_data['user']
        password = config_data['password']
        dsn = cx_Oracle.makedsn("dbmanage.lab.ii.agh.edu.pl", 1521, sid="DBMANAGE")

        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn, encoding="UTF-8")

        return conn

    except cx_Oracle.Error as error:
        print("Błąd podczas łączenia z bazą danych:", error)
        exit()


def execute_querry(sql: str) -> list[any] | dict[str, str]:
    if conn is None:
        return {'error': 'Błąd podczas łączenia z bazą danych'}
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() if cursor.description else []
        cursor.close()
        return rows

    except cx_Oracle.Error as error:
        if conn:
            conn.rollback()
        print("Błąd podczas wykonania zapytania:", error)
        return {'error': str(error)}


def execute_and_render(query: str, template_url: str, value_name: str = 'data') -> str:
    result = execute_querry(query)
    if 'error' in result:
        return f"Wystąpił błąd: {result['error']}", 500
    else:
        return render_template(template_url, **{value_name: result})


def get_table_data(table_name: str, display_name: str = "", comment: str = "") -> str:
    column_names_packed = execute_querry(
        f"SELECT column_name FROM USER_TAB_COLUMNS WHERE table_name = '{table_name.upper()}'"
    )
    column_names = [item for sublist in column_names_packed for item in sublist]
    data = execute_querry(f"SELECT * FROM {table_name}")
    return render_template('table.html',
                           table_name=table_name,
                           column_names=column_names,
                           data=data,
                           comment=comment,
                           display_name=display_name,
                           )


def call_procedure(proc_name: str, args: list[int | str]) -> dict[str, any]:
    if conn is None:
        return {'error': 'Błąd podczas łączenia z bazą danych'}

    try:
        cursor = conn.cursor()
        cursor.callproc(proc_name, args)
        conn.commit()
        cursor.close()
        return {'message': f'Procedure {proc_name} executed successfully'}
    except cx_Oracle.Error as error:
        if conn:
            conn.rollback()
        print("Błąd podczas wykonania procedury:", error)
        return {'error': str(error)}
    

def call_function(func_name: str, args: list[int | str]) -> dict[str, any]:
    if conn is None:
        return {'error': 'Błąd podczas łączenia z bazą danych'}

    try:
        cursor = conn.cursor()
        result_cursor = cursor.var(cx_Oracle.CURSOR)
        cursor.callfunc(func_name, result_cursor, args)
        result_cursor = result_cursor.getvalue()
        rows = result_cursor.fetchall() if result_cursor else []
        cursor.close()
        return rows
    except cx_Oracle.Error as error:
        if conn:
            conn.rollback()
        print("Błąd podczas wykonania funckji:", error)
        return {'error': str(error)}
