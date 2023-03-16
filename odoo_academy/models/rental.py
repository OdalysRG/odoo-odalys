# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

class Rental(models.Model):
    _name = 'book.rental'
    _description = 'Rental System'
    
    books_id = fields.Many2one(comodel_name ='book.copies',
                             string ='Book Title',
                             required=True)

    book_id = fields.Char(comodel_name='book.copies', string="Book ID", related='books_id.book_id')
    
    
    name = fields.Char(string='Title', related='books_id.name')
    
    
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    
    
    contacts_ids = fields.Many2many(comodel_name='res.partner', string='Contacts') 

    
    start_date = fields.Date(string='Handing Date',
                            default=fields.Date.today)
    
    duration = fields.Integer(string='Rental Days',
                             default=1)
    
    end_date = fields.Date(string='Return Date',
                           compute='_compute_end_date',
                           inverse='_inverse_end_date',
                           store=True)
    
    rented = fields.Boolean(string='Rented')
    
    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for record in self:
            if not (record.start_date and record.duration):
                record.end_date = record.start_date
            else:
                duration = timedelta(days=record.duration)
                record.end_date = record.start_date + duration
    
    @api.depends('start_date', 'end_date')
    def _inverse_end_date(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration = (record.end_date - record.start_date).days + 1
            else:
                continue 
             
            
            
                
                  