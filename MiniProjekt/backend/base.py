import cx_Oracle
from typing import Any, List, Dict, Union

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

        lib_dir = "C:\instantclient_21_13"
        user = config_data['user']
        password = config_data['password']
        dsn = cx_Oracle.makedsn("dbmanage.lab.ii.agh.edu.pl", 1521, sid="DBMANAGE")

        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn, encoding="UTF-8")

        return conn

    except cx_Oracle.Error as error:
        print("Błąd podczas łączenia z bazą danych:", error)
        return None

def execute_querry(sql: str, parameters: tuple = None, commit: bool = False) -> Union[List[Any], Dict[str, str]]:
    try:
        cursor = conn.cursor()

        if parameters:
            cursor.callproc(sql, parameters)
        else:
            cursor.execute(sql)

        if commit:
            conn.commit()

        if cursor.description:
            rows = cursor.fetchall()
        else:
            rows = []

        cursor.close()
        return rows

    except cx_Oracle.Error as error:
        if conn:
            conn.rollback()
        print("Błąd podczas wykonania zapytania:", error)
        return {'error': str(error)}


def call_procedure(proc_name: str, args: List[Union[int, str]]) -> Dict[str, Any]:
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
    

def call_function(func_name: str, args: List[Union[int, str]]) -> Dict[str, Any]:
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
        print("Błąd podczas wykonania procedury:", error)
        return {'error': str(error)}
