# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    tenant_type = fields.Selection([
        ('businessman','Business Man'),
        ('bachelors','Bachelors'),
        ('family','Family'),
        ],
        string='Tenant Type',
        copy=False,
        help="This will show which type of Tenant is there."
    )
    number_of_tenants = fields.Char(
        string='Number of Tenants',
    )
    broker_name = fields.Char(
        'Broker / Agent',
    )
    product_id = fields.Many2one(
        'product.product',
        'Requested For',
    )
    owner_id = fields.Many2one(
        'res.partner',
        'Owner',
    )
    owner_email = fields.Char(
         'Email',
    )
    owner_phone = fields.Char(
        'Phone',
    )
