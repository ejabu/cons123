# -*- coding: utf-8 -*-
{
    'name': "Web UI Eja",

    'summary': """
        Demo showing you how to add JS, CSS and images to an Odoo module!""",

    'description': """
         Demo showing you how to add JS, CSS and images to an Odoo module!
    """,

    'author': "Muhammad Fahreza",
    # Categories can be used to filter modules in modules listing

    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/static_resources_demo_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'qweb' : [
        "static/src/xml/base.xml",
    ],
}
