# -*- coding: utf-8 -*-

from odoo import fields, models

class CrmLead(models.Model):
    _inherit = "crm.lead"

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
        related='product_id.owner_id',
        store=True,
    )
    owner_email = fields.Char(
         'Email',
         related='product_id.email',
         store=True,
    )
    owner_phone = fields.Char(
        'Phone',
         related='product_id.phone',
         store=True,
        
    )
