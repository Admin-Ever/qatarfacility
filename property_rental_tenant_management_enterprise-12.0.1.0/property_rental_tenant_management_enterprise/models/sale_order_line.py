# -*- coding: utf-8 -*-

from odoo import models, fields

class Sale(models.Model):
    _inherit = 'sale.order.line'
    
    rental_history_id = fields.Many2one(
        'property.rental',
        string='Rental History',
    )
