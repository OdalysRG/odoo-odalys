# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from random import randint

class EmployeesList(models.Model):
    _inherit='res.partner'
    
    