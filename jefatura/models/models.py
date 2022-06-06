# -*- coding: utf-8 -*-

from odoo import models, fields, api


class alumno(models.Model):
    _name = 'jefatura.alumno'
    _description = 'Permite definir un alumno'
    _order = 'apellidos'
    _rec_name = 'apellidos'

    nombre = fields.Char('Nombre', required = True)
    apellidos = fields.Char('Apellidos', required = True)
    email = fields.Char('Email', required = True)
    telefono = fields.Char('Teléfono', required = True)










#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
