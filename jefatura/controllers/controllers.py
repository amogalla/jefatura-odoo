# -*- coding: utf-8 -*-
# from odoo import http


# class Jefatura(http.Controller):
#     @http.route('/jefatura/jefatura', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jefatura/jefatura/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('jefatura.listing', {
#             'root': '/jefatura/jefatura',
#             'objects': http.request.env['jefatura.jefatura'].search([]),
#         })

#     @http.route('/jefatura/jefatura/objects/<model("jefatura.jefatura"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jefatura.object', {
#             'object': obj
#         })
