# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import urllib.parse
import json


class telegram():
    TOKEN = "<<TOKEN>>"
    chat_id = "<<chat_id>>"
    def codificar_diccionario(diccionario):
        # dict_reply_json = json.dumps(diccionario)
        # reply = urllib.parse.quote_plus(dict_reply_json)
        return json.dumps(diccionario)

    def mensaje_telegram_expulsion(texto, id_alumno, tupla_amonestaciones):
        TOKEN = telegram.TOKEN
        chat_id = telegram.chat_id
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={texto}"
        respuesta = requests.get(url)
        json_data = respuesta.json()
        id_mensaje_enviado = str(json_data['result']['message_id'])

        botones = {
            "inline_keyboard": [
                [
                    {
                        "text": "Expulsar alumno",
                        'callback_data': "{'alumno': '" + id_alumno + "', 'amonestaciones': '(" + tupla_amonestaciones + ")', 'msg': '" + id_mensaje_enviado + "'}"
                    }
                ],
                [
                    {
                        "text": "Indultar alumno",
                        "callback_data": "{'alumno': '0', 'msg': '" + id_mensaje_enviado + "'}"
                    }
                ]
            ]
        }

        reply = json.dumps(botones)

        url = f"https://api.telegram.org/bot{TOKEN}/editMessageText?chat_id={chat_id}&message_id={id_mensaje_enviado}&text={texto}" \
            f"&'parse_mode': 'markdown'" \
            f"&reply_markup={reply}"

        requests.get(url)

    def mensaje_telegram_jefe_estudios(texto):
        TOKEN = telegram.TOKEN
        chat_id = telegram.chat_id
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={texto}"
        requests.get(url)

    def mensaje_telegram_personal(texto, id_chat):
        TOKEN = telegram.TOKEN
        chat_id = telegram.chat_id
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id_chat}&text={texto}"
        requests.get(url)


class alumno(models.Model):
    _name = 'jefatura.alumno'
    _description = 'Permite definir un alumno'
    _order = 'apellidos'
    _rec_name = 'nombre_completo'

    nombre = fields.Char('Nombre', required = True)
    apellidos = fields.Char('Apellidos', required = True)
    nombre_completo = fields.Char('Nombre completo')
    email = fields.Char('Email', required = True)
    alias_telegram = fields.Char('Alias en Telegram', required = True)
    chat_id_telegram = fields.Char('ID Chat en Telegram')
    telefono = fields.Char('Teléfono', required = True)
    #nombre_completo = fields.Char('Nombre completo')
    imagen = fields.Binary(string ="Imagen del alumno")
    num_amonestaciones = fields.Integer('Número de amonestaciones', default = 0)
    num_amonestaciones_sin_computar = fields.Integer('Número de amonestaciones sin computar', default = 0)
    num_expulsiones = fields.Integer('Número de expulsiones', default = 0)
    
    #Relaciones con otras tablas
    asignatura_ids = fields.Many2many('jefatura.asignatura', string = 'Asignaturas')
    amonestacion_ids = fields.One2many('jefatura.amonestacion', 'alumno_id', string = 'Amonestaciones')
    expulsion_ids = fields.One2many('jefatura.expulsion', 'alumno_id', string = 'Expulsiones')

    def rellenar_nombre_completo(self, nombre, apellidos):
        self.nombre_completo = nombre + " " + apellidos


    def inc_amonestaciones(self):
        self.num_amonestaciones += 1
        self.num_amonestaciones_sin_computar += 1
        #telegram.mensaje_telegram_jefe_estudios(self.amonestacion_ids)
        
        if self.num_amonestaciones_sin_computar >= 3:
            id_alumno = str(self.id)
            tupla_amonestaciones = ""
            texto = "El alumno " + self.nombre_completo + " ha recibido una amonestación que podría suponer la expulsión del centro. \n\nActualmente tiene estas amonestaciones sin computar:\n"
            for amonestacion in self.amonestacion_ids:
                if amonestacion.estado == 'Validada' and amonestacion.computada == False:
                    texto += str(amonestacion.fecha) + " - " + amonestacion.motivo + "\n"
                    tupla_amonestaciones = tupla_amonestaciones + str(amonestacion.id) + ","

            telegram.mensaje_telegram_expulsion(texto, id_alumno, tupla_amonestaciones[:-1])


class profesor(models.Model):
    _name = 'jefatura.profesor'
    _description = 'Permite definir un profesor'
    _order = 'apellidos'
    _rec_name = 'nombre_completo'

    nombre = fields.Char('Nombre', required = True)
    apellidos = fields.Char('Apellidos', required = True)
    nombre_completo = fields.Char('Nombre completo')
    email = fields.Char('Email', required = True)
    telefono = fields.Char('Teléfono', required = True)
    alias_telegram = fields.Char('Alias en Telegram', required = True)
    chat_id_telegram = fields.Char('ID Chat en Telegram')
    imagen = fields.Binary(string ="Imagen del profesor")

    #Relaciones con otras tablas
    asignatura_ids = fields.One2many('jefatura.asignatura', 'profesor_id', string = 'Asignaturas')
    amonestacion_ids = fields.One2many('jefatura.amonestacion', 'profesor_id', string = 'Amonestaciones')
    #curso_ids = fields.One2many('jefatura.curso', 'profesor_id', string = 'Cursos')
    curso_id = fields.Many2one('jefatura.curso', string = 'Curso')

    def rellenar_nombre_completo(self, nombre, apellidos):
        self.nombre_completo = nombre + " " + apellidos

class asignatura(models.Model):
    _name = 'jefatura.asignatura'
    _description = 'Permite definir una asignatura o módulo'
    _order = 'nombre'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre', required = True)

    #Relaciones con otras tablas
    alumno_ids = fields.Many2many('jefatura.alumno', string = 'Alumnos')
    profesor_id = fields.Many2one('jefatura.profesor', string = 'Profesor')
    curso_id = fields.Many2one('jefatura.curso', string = 'Curso')


class tarea(models.Model):
    _name = 'jefatura.tarea'
    _description = 'Permite definir una tarea'
    _order = 'asignatura'
    _rec_name = 'asignatura'

    descripcion = fields.Char('Descripción', required=True)
    asignatura = fields.Char('Asignatura', required=True)

    # Relaciones con otras tablas
    expulsion_id = fields.Many2one('jefatura.expulsion', string='Expulsion')


class curso(models.Model):
    _name = 'jefatura.curso'
    #_inherit = 'jefatura.profesor'
    #_inherits = {'jefatura.profesor': "profesor_id"}
    _description = 'Permite definir un curso'
    _order = 'nombre'
    _rec_name = 'nombre_completo'

    nombre = fields.Char('Nombre', required = True)
    aclarador = fields.Char('Aclarador')
    nombre_completo = fields.Char('Nombre curso completo')

    #Relaciones con otras tablas
    profesor_ids = fields.One2many('jefatura.profesor', 'curso_id', string = 'Tutor/es')
    asignatura_ids = fields.One2many('jefatura.asignatura', 'curso_id', string = 'Asignaturas')

    def rellenar_nombre_completo(self, nombre, aclarador):
        self.nombre_completo = nombre + " " + aclarador

class amonestacion(models.Model):
    _name = 'jefatura.amonestacion'
    _description = 'Permite definir una amonestación'
    _order = 'fecha'
    _rec_name = 'fecha'

    fecha = fields.Date(string='Fecha de la infracción', required = True)
    motivo = fields.Char(string='Motivo de la amonestación', required = True)
    estado = fields.Char(string='Estado', default='Borrador')
    medida_propuesta = fields.Char(string='Medida educativa propuesta', required = True)
    computada = fields.Boolean(string='¿Amonestación ya computada?', required = True, default = False)

    #Relaciones con otras tablas
    profesor_id = fields.Many2one('jefatura.profesor', string = 'Profesor', required = True)
    alumno_id = fields.Many2one('jefatura.alumno', string = 'Alumno', required = True)
    expulsion_id = fields.Many2one('jefatura.expulsion', string = 'Expulsión', required = True)
    
    def hacer_definitiva(self):
        self.estado = 'Validada'
        self.alumno_id.inc_amonestaciones()
    
    
    def inc_amonestacion_alumno(self):
        self.alumno_id.inc_amonestaciones()


class expulsion(models.Model):
    _name = 'jefatura.expulsion'
    _description = 'Permite definir una expulsión'
    _order = 'fecha'
    _rec_name = 'fecha'

    fecha = fields.Date(string='Fecha de la infracción', required = True)
    estado = fields.Char(string='Estado', default='Borrador')
    num_dias = fields.Integer(string='Período de expulsión', default=3, required = True)

    #Relaciones con otras tablas
    alumno_id = fields.Many2one('jefatura.alumno', string = 'Alumno', required = True)
    amonestacion_ids = fields.One2many('jefatura.amonestacion', 'expulsion_id', string = 'Amonestaciones')
    tarea_ids = fields.One2many('jefatura.tarea', 'expulsion_id', string='Tareas')

    def aviso_profesores_expulsion(self):
        texto = "Se ha propuesto una expulsión al alumno " + self.alumno_id.nombre + " " + self.alumno_id.apellidos + ". Recuerde indicar la tarea correspondiente a su asignatura."

        for alumno in self.alumno_id:
            for asignatura in alumno.asignatura_ids:
                for profesor in asignatura.profesor_id:
                    telegram.mensaje_telegram_personal(texto, profesor.chat_id_telegram)



    def hacer_definitiva(self):
        texto = "El alumno " + self.alumno_id.nombre + " " + self.alumno_id.apellidos + " ha sido expulsado del centro durante" \
                " " + str(self.num_dias) + " días."

        for amonestacion in self.amonestacion_ids:
            if amonestacion.computada == False:
                amonestacion.computada = True
            #texto += str(amonestacion.fecha) + " - " + amonestacion.motivo + "\n"


        self.estado = 'Validada'
        self.alumno_id.num_amonestaciones_sin_computar = 0
        self.alumno_id.num_expulsiones += 1

        telegram.mensaje_telegram_jefe_estudios(texto)

        texto_familia = texto + " Deberá recoger la tarea correspondiente en Conserjería."
        telegram.mensaje_telegram_personal(texto_familia, self.alumno_id.chat_id_telegram)