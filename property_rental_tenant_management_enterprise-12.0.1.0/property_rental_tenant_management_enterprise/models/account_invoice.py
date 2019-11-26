# -*- coding: utf-8 -*-

from odoo import models, fields

class Invoices(models.Model):
    _inherit = 'account.invoice'
    
    rent_start_date = fields.Date(
        string='Rent Start date',
        help="Start date of property on rent",
    )
    rent_end_date = fields.Date(
        string='Rent End Date',
        help="End date of property on rent",
    )
    recurring_rule_type = fields.Selection([
        ('daily', 'Day(s)'),
        ('weekly', 'Week(s)'),
        ('monthly', 'Month(s)'),
        ('yearly', 'Year(s)'), ],
        string='Recurring Period',
        copy=False,
        help="This will show Recurring time for rent."
    )
    recurring_interval = fields.Integer(
        string="Repeat Every",
        copy=False,
    )
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
