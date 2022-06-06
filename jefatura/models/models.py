# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests


class alumno(models.Model):
    _name = 'jefatura.alumno'
    _description = 'Permite definir un alumno'
    _order = 'apellidos'
    _rec_name = 'apellidos'

    nombre = fields.Char('Nombre', required = True)
    apellidos = fields.Char('Apellidos', required = True)
    email = fields.Char('Email', required = True)
    telefono = fields.Char('Teléfono', required = True)
    
    #Relaciones con otras tablas
    asignatura_ids = fields.Many2many('jefatura.asignatura', string = 'Asignaturas')
    amonestacion_ids = fields.One2many('jefatura.amonestacion', 'alumno_id', string = 'Amonestaciones')
    
    

class profesor(models.Model):
    _name = 'jefatura.profesor'
    _description = 'Permite definir un profesor'
    _order = 'apellidos'
    _rec_name = 'apellidos'

    nombre = fields.Char('Nombre', required = True)
    apellidos = fields.Char('Apellidos', required = True)
    email = fields.Char('Email', required = True)
    telefono = fields.Char('Teléfono', required = True)
    alias_telegram =  fields.Char('Alias en Telegram', required = True)

    #Relaciones con otras tablas
    asignatura_ids = fields.One2many('jefatura.asignatura', 'profesor_id', string = 'Asignaturas')
    amonestacion_ids = fields.One2many('jefatura.amonestacion', 'profesor_id', string = 'Amonestaciones')
    curso_ids = fields.Many2many('jefatura.curso', string = 'Cursos')
    

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
    


class curso(models.Model):
    _name = 'jefatura.curso'
    _description = 'Permite definir un curso'
    _order = 'nombre'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre', required = True)
    letra = fields.Char('Letra')

    #Relaciones con otras tablas
    profesor_ids = fields.Many2many('jefatura.profesor', string = 'Profesores')
    asignatura_ids = fields.One2many('jefatura.asignatura', 'curso_id', string = 'Asignaturas')
    
    def mensaje_tgram(self, nombre_curso):
        TOKEN = "<<TOKEN>>"
        chat_id = "<<ID_CHAT>>"
        text = "Curso " + nombre_curso + " añadido con éxito"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
        r = requests.get(url)


class amonestacion(models.Model):
    _name = 'jefatura.amonestacion'
    _description = 'Permite definir una amonestación'
    _order = 'fecha'
    _rec_name = 'fecha'

    fecha = fields.Date(string='Fecha de la infracción')
    #hora = fields.
    motivo = fields.Char(string='Motivo de la amonestación')
    

    #Relaciones con otras tablas
    profesor_id = fields.Many2one('jefatura.profesor', string = 'Profesor', required = True)
    alumno_id = fields.Many2one('jefatura.alumno', string = 'Alumno', required = True)
    



#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
