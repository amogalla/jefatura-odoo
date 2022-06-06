import xmlrpc.client
import psycopg2
from datetime import datetime

def registrar_log_expulsion(conexion, nombre_alumno):
    try:
        # create a cursor
        cursor = conexion.cursor()

        sql = "INSERT INTO ir_logging(create_uid, create_date, name, type, dbname, level, message, path, func, line) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"# RETURNING id"
        query = cursor.mogrify(sql, ("1", str(datetime.now()).replace("-", "/"), "odoo.addons.base.models.ir_actions", "server", "edu-instituto", "info", f"Creada expulsión desde Telegram al alumno {nombre_alumno}", "action", "Log expulsión creada", "329"))
        cursor.execute(query)
        #id_of_new_row = str(cursor.fetchone()[0])

        conexion.commit()
        cursor.close()

    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        conexion = None



def insertar_expulsion(conexion, id_alumno, ids_amonestaciones):
    try:
        # create a cursor
        cursor = conexion.cursor()

        sql = "INSERT INTO jefatura_expulsion(fecha, estado, num_dias, alumno_id) VALUES (%s, %s, %s, %s) RETURNING id"
        query = cursor.mogrify(sql, (str(datetime.today().strftime('%Y/%m/%d')), "Borrador", "3", id_alumno))
        cursor.execute(query)
        id_of_new_row = str(cursor.fetchone()[0])

        sql2 = "UPDATE jefatura_amonestacion SET expulsion_id = %s WHERE id IN " + ids_amonestaciones
        query2 = cursor.mogrify(sql2, (id_of_new_row,))
        cursor.execute(query2)

        registrar_log_expulsion(conexion, get_nombre_completo_alumno(conexion, id_alumno))
        cursor.close()

    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        conexion = None


def insertar_chat_id(conexion, chat_id, alias_telegram):
    try:
        # create a cursor
        cursor = conexion.cursor()

        sql = "SELECT id FROM jefatura_profesor WHERE alias_telegram = %s"
        query = cursor.mogrify(sql, (alias_telegram,))
        cursor.execute(query)

        row = cursor.fetchone()
        if row is None:
            return False

        sql = "UPDATE jefatura_profesor SET chat_id_telegram = %s WHERE alias_telegram = %s"
        query = cursor.mogrify(sql, (chat_id, alias_telegram))
        cursor.execute(query)

        conexion.commit()
        cursor.close()
        return True


    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        conexion = None
        return False


def chats_telegram_profesores(conexion, id_alumno):
    try:
        # create a cursor
        cursor = conexion.cursor()

        sql = f"select array(SELECT jefatura_asignatura_id FROM jefatura_alumno_jefatura_asignatura_rel WHERE jefatura_alumno_id = {id_alumno})"
        #query = cursor.mogrify(sql, (chat_id, alias_telegram))
        cursor.execute(sql)

        id_asignaturas = str(cursor.fetchone()[0]).replace("[", "(").replace("]", ")")
        #print("Asignaturas: " + id_asignaturas)

        sql2 = f"select array(SELECT profesor_id FROM jefatura_asignatura WHERE id IN {id_asignaturas})"
        cursor.execute(sql2)

        id_profesores= str(set(cursor.fetchone()[0])).replace("{", "(").replace("}", ")")
        #print("Profesores: " + id_profesores)


        sql3 = f"select array(SELECT chat_id_telegram FROM jefatura_profesor WHERE id IN {id_profesores} AND chat_id_telegram IS NOT NULL)"
        cursor.execute(sql3)

        chats_telegram_profesores= set(cursor.fetchone()[0]) #str(set(cursor.fetchone()[0])).replace("{", "(").replace("}", ")").replace("'", "")
        #print("Chats telegram: " + str(chats_telegram_profesores))

        cursor.close()

        return chats_telegram_profesores

    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        conexion = None

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
