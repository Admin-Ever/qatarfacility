# -*- coding: utf-8 -*-

from odoo import models, fields

class Property(models.Model):
    _name = 'property.description'
    
    name = fields.Char(
        string='Name'
    )
    value = fields.Char(
        string='Value'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )
