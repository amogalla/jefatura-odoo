# -*- coding: utf-8 -*-
{
    'name': "jefatura",

    'summary': "Gestión de la jefatura de estudios.",

    'description': """
        En este módulo se gestionan los siguientes trabajos de la jefatura de estudios:
        - Amonestaciones
        - Expulsiones
        - Comunicaciones con profesorado y familias
    """,

    'author': "Alejandro M. Ogalla",
    'website': "https://github.com/amogalla",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/jefatura_amonestacion_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
