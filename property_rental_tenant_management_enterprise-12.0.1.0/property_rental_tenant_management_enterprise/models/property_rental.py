# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date

from odoo import models, fields, api, _

class PropertyRental(models.Model):
    _name = 'property.rental'
#     _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin'] #odoo11
    _rec_name = 'product_id'
    _description = 'Property Rental History'
    
    @api.depends('start_date','end_date')
    def compute_reserve(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                duration = datetime.strptime(str(rec.end_date), "%Y-%m-%d") - datetime.strptime(str(rec.start_date), "%Y-%m-%d")
                days = abs(duration.days)
                day = 1
                rec.reserved = rec.start_date
                while day <= days and datetime.date(datetime.strptime(str(rec.reserved), "%Y-%m-%d"))  < date.today():
                    rec.reserved = datetime.strptime(str(rec.reserved), "%Y-%m-%d").date() + timedelta(1)
                    day += 1
                reserved = datetime.date(datetime.strptime(str(rec.reserved), "%Y-%m-%d"))
                if reserved == date.today():
                    rec.is_reserved = True
                else:
                    rec.is_reserved = False
                if rec.state != 'allocated':
                    rec.is_reserved = False
        
    start_date = fields.Date(
        'Start Date',
        required=True,
    )
    end_date = fields.Date(
        'End Date',
        required=True,
    )
    product_id = fields.Many2one(
        'product.product',
        'Property',
        required=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Tenant',
        required=True,
    )
    reserved = fields.Date(
        string='Reserved',
    )
    is_reserved = fields.Boolean(
        'Is Reserved',
        compute='compute_reserve',
        stored=True,
    )
    quotation_id = fields.Many2one(
        'sale.order',
        'Quotation'
    )
    lead_id = fields.Many2one(
        'crm.lead',
        'Lead',
    )
    state = fields.Selection(
        [('new','New'),
         ('allocated','Allocated'),
         ('cancel','Cancelled'),
         ('done','Done'),
        ],
        track_visibility='onchange',
        default=lambda self: _('new'),
    )
    order_line_id = fields.Many2one(
        'sale.order.line',
        string='Order Line',
    )
    
    @api.multi
    def action_new(self):
        self.write({'state': 'new'})
        
    @api.multi
    def action_allocated(self):
        self.write({'state': 'allocated'})
        
    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
        
    @api.multi
    def action_done(self):
        self.write({'state': 'done'})
