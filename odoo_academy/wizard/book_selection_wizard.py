# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BookSelectionWizard(models.TransientModel):
    _name = 'book.selection.wizard'
    _description = 'Wizard: Quick Selection for Customers'
    
    def _default_books(self):
        return self.env['book.collection'].browse(self._context.get('active_id'))
    
    books_id = fields.Many2one(comodel_name ='book.collection',
                               string ='Book Title',
                               required = True,
                              default=_default_books)
    
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    
    
    def select_a_book(self):
        return
    

                