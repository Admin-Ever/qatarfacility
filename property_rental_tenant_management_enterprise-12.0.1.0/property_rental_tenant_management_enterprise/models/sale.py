# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class Sale(models.Model):
    _inherit = 'sale.order'
    
    start_date = fields.Date(
        string='Start Date',
        help='Manually set the start date of the rent which property on rent.'
    )
    end_date = fields.Date(
        'End Date',
        help="Manually set the end date of the rent which property on rent."
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
                
    @api.multi
    def action_confirm(self):
        result = super(Sale, self).action_confirm()
        for res in self:
            if res.analytic_account_id:
                if res.owner_id:
                    # related_project_id is become as analytic_account_id
                    # res.related_project_id.owner_id = res.owner_id.id
                    res.analytic_account_id.owner_id = res.owner_id.id
                if res.owner_email:
                    res.analytic_account_id.owner_email = res.owner_email
                if res.owner_phone:
                    res.analytic_account_id.owner_phone = res.owner_phone
                if res.recurring_rule_type:
                    res.analytic_account_id.recurring_rule_type = res.recurring_rule_type
                if res.recurring_interval:
                    res.analytic_account_id.recurring_interval = res.recurring_interval
                if res.tenant_type:
                    res.analytic_account_id.tenant_type = res.tenant_type
                if res.number_of_tenants:
                    res.analytic_account_id.number_of_tenants = res.number_of_tenants
                if res.broker_name:
                    res.analytic_account_id.broker_name = res.broker_name
                if res.product_id:
                    res.analytic_account_id.product_id = res.product_id
        rental_ids = []
        
        for sale_order in self:
            if not sale_order.start_date:
                raise ValidationError("Please Select Start date.")
            elif not sale_order.end_date:
                raise ValidationError("Please Select End date.")
        for order_line in self.order_line:
            product_id = order_line.product_id
            qty = order_line.product_uom_qty
            if product_id.is_rental_product and not qty == 1:
                raise UserError(_("You are allowed to add only one property at one time for rent."))
                
            if product_id.is_rental_product:
                if product_id.rental_ids:
                    for rental_id in product_id.rental_ids:
                        rental_ids.append(rental_id.id)
                rental_obj = self.env['property.rental']
                vals = {
                    'start_date' : self.start_date,
                    'end_date' : self.end_date,
                    'partner_id' : self.partner_id.id,
                    'product_id' : order_line.product_id.id,
                    'quotation_id' : self.id,
                    'lead_id' : self.opportunity_id.id,
                    'state' : 'allocated',
                }
                rental_id = rental_obj.create(vals)
                rental_ids.append(rental_id.id)
                
                rental_history_vals = {
                    'rental_ids' : [(6, 0, rental_ids)],
                }
                rental_history_id = product_id.sudo().write(rental_history_vals)
                for order_lines in self.order_line:
                    order_lines.rental_history_id = rental_id.id
                    order_lines.rental_history_id.order_line_id = order_lines.id
        return result
    
    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(Sale, self)._prepare_invoice()
        for rec in self:
            rental_invoice = {
                'rent_start_date' : rec.start_date,
                'rent_end_date' : rec.end_date,
                'tenant_type': rec.tenant_type,
                'number_of_tenants': rec.number_of_tenants,
                'broker_name': rec.broker_name,
                'product_id': rec.product_id.id,
            }
            if rec.owner_id:
                rental_invoice.update({'owner_id' : rec.owner_id.id})
            if rec.owner_email:
               rental_invoice.update({'owner_email' : rec.owner_email})
            if rec.owner_phone:
                rental_invoice.update({'owner_phone' : rec.owner_phone})
            invoice_vals.update(rental_invoice)
        return invoice_vals
    
    @api.multi
    def action_cancel(self):
        super(Sale, self).action_cancel()
        for order_line in self.order_line:
            for rental_id in order_line.rental_history_id:
                rental_id.state = 'cancel'
    
    
