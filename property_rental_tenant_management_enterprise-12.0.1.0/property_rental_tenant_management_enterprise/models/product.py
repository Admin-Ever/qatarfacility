# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Property(models.Model):
    _inherit = 'product.product'
    
    @api.depends('rental_ids')
    def compute_reserve(self):
        for rec in self:
            for rental in rec.rental_ids:
                if rental.is_reserved:
                    rec.is_reserved = True
    
    is_rental_product = fields.Boolean(
        string='Is Rental Product',
        help='Checked if it was for rent'
    )
    rental_ids = fields.One2many(
        'property.rental',
        'product_id',
    )
    is_reserved = fields.Boolean(
        'Is Reserved ?',
        compute='compute_reserve',
        help='Checked if reserved on this day'
    )
    property_description_ids = fields.One2many(
        'property.description',
        'product_id',
    )
    owner_id = fields.Many2one(
        'res.partner',
        'Owner',
    )
    email = fields.Char(
        'Email',
    )
    phone = fields.Char(
        'Phone',
    )
