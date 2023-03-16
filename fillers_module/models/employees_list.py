# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from random import randint

class EmployeesList(models.Model):
    _inherit='res.partner'
    
    rentalcus_ids = fields.One2many (comodel_name='fillers_module.pdf_generator',
                                     inverse_name='customer_id',
                                     string='Contract')