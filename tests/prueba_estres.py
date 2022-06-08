import xmlrpc.client
import psycopg2
from acceso_postgres import conectar_psql

def get_nombre_completo_alumno(conexion, id_alumno):
    try:
        # create a cursor
        cursor = conexion.cursor()

        sql = f"select nombre FROM jefatura_alumno WHERE id = {id_alumno}"
        cursor.execute(sql)
        nombre_alumno = cursor.fetchone()[0]

        sql = f"select apellidos FROM jefatura_alumno WHERE id = {id_alumno}"
        cursor.execute(sql)
        apellidos_alumno = cursor.fetchone()[0]

        cursor.close()

        return nombre_alumno + " " + apellidos_alumno

    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        conn = None



if __name__ == '__main__':
    for iter in range(1,10000):
        print(str(iter) + ": " + get_nombre_completo_alumno(conectar_psql(), "1"))
