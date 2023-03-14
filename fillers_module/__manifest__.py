# -*- coding: utf-8 -*-

{
    'name': 'Odoo Filler Module',
    
    'summary': """  Odoo Fillers Module where you can autofill a contract's blanks""",
    
    'description': """
            This module makes easier to fill an employees contract.
    """,
    'autor': 'Odoo Developers',
    
    'website': 'https://www.odoofiller.com',
    
    'category': 'Human Resources',
    'version': '0.1',
    
    'depends': ['base' , 'web_map', 'project', 'website', 'hr'],
    
    'data': [
        'security/fillers_module_groups.xml',
        'security/ir.model.access.csv',
        'views/fillers_module_menuitems.xml',
        'views/pdf_views.xml',
    ],
    
     'assets': {},
    
     'installable': True,
     'application': True,
     'auto_install': False,
    
        'license': 'OPL-1',
}



