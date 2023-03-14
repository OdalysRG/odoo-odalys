# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import randint

class BookCopies(models.Model):
    _name = 'book.copies'
    _inherits = {'book.collection': 'book_name'}
    _description = 'Copies of the book'
    
 
    book_name = fields.Many2one(comodel_name='book.collection', string="Book Name", required=True, ondelete='cascade')
    
    name = fields.Char(string='Title', related='book_name.name')
    
    book_id = fields.Char(comodel_name='book.collection',string ='Book ID')
    
    rentals_id = fields.Many2one(comodel_name ='book.rental', inverse_name='books_id', string ='Rented Book Title')
    
    rented_id = fields.Boolean(string='Rented', related='rentals_id.rented')
    
    obtainable = fields.Boolean(string='Obtainable', compute='_book_rental_status')
                
    @api.model
    def create(self, vals):
        vals['book_id']= self.env['ir.sequence'].next_by_code('book.id')
        return super(BookCopies, self).create(vals)
    
    @api.depends('rented_id')
    def _book_rental_status(self):
        for record in self:
            if record.rented_id == True: 
                record.obtainable = False
            else:
                record.obtainable = True
    
    
    

    

    
    
    
    