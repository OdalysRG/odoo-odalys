# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Books(models.Model):
    
        _name = 'book.collection'
        _description = 'Book Collection'
        
        name = fields.Char(string='Title', required= True)
        
        description = fields.Text(string='Description')
        
        author = fields.Char(string='Author', required= True)
        
        editor = fields.Char(string='Editor')
        
        publisher = fields.Char(string='Publisher')
        
        year = fields.Char(string='Year', required= True)
        
        isbn = fields.Char(string='ISBN', size=13, required= True, onchange='_onchange_isbn')
        
        genre = fields.Selection(string ='Genre',
                                selection = [('action', 'Action'),
                                            ('comedy','Comedy'),
                                            ('drama', 'Drama'),
                                            ('fantasy','Fantasy'),
                                            ('fiction','Fiction'),
                                            ('horror','Horror'),
                                            ('mystery','Mystery'),
                                            ('nonfiction','Nonfiction'),
                                            ('romance','Romance'),
                                            ('thriller','Thriller'),
                                            ('other','Other')],
                                copy= False)
        
        notes = fields.Text(string='Note')
        
        copies_ids = fields.One2many (comodel_name='book.copies',
                                      inverse_name='book_name',
                                      string='Book Copies')
        
        available = fields.Boolean(string="Available", default=True)
    
        
        
        @api.onchange('isbn')
        def _onchange_isbn(self):
            for record in self:
                if record.name and len(self.isbn) != 13:
                    raise ValidationError ('ISBN lenght has to be made of 13 digits.')
    