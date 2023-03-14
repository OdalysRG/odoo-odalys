# -*- coding: utf-8 -*-

{
    'name': 'Odoo Library Module',
    
    'summary': """Public library module where you can manage the books that have been rent, their due dates, 
    and the ones that have been returned with their respective customers""",
    
    'description': """
            Library Management System module where you can:
            -Store their entire book collection by different types of filters.
            -Have a record of the books that are rented, and their due times.
            -Keep record of the customers that are pending to return the books.
    """,
    'autor': 'Odalys',
    
    'website': 'https://www.centrallibrarymodule.com',
    
    'category': 'Book Rental',
    'version': '0.1',
    
    'depends': ['base' , 'web_map'],
    
    'data':[
        'data/sequence_data.xml',
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'wizard/book_selection_wizard_view.xml',
        'views/library_menuitems.xml',
        'views/collection_views.xml',
        'views/rental_views.xml',
        'views/customer_rental_views.xml',
        'views/book_copies.xml',
    ],
    
    'demo': ['demo/library_demo.xml'],
    
    'license': 'LGPL-3',
    
    
}