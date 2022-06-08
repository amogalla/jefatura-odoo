import xmlrpc.client
import psycopg2
from datetime import datetime
from acceso_postgres import conectar_psql

def registrar_log_expulsion(conexion):
    try:
        # create a cursor
        cursor = conexion.cursor()

        sql = "INSERT INTO ir_logging(create_uid, create_date, name, type, dbname, level, message, path, func, line) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"# RETURNING id"
        query = cursor.mogrify(sql, ("1", str(datetime.now()).replace("-", "/"), "odoo.addons.base.models.ir_actions", "server", "edu-instituto", "info", f"Añadido log en prueba de volumen", "action", "Log de prueba", "329"))
        cursor.execute(query)
        #id_of_new_row = str(cursor.fetchone()[0])

        conexion.commit()
        cursor.close()

    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        conexion = None


if __name__ == '__main__':
    for iter in range(1,10):
        print(iter)
        registrar_log_expulsion(conectar_psql())

