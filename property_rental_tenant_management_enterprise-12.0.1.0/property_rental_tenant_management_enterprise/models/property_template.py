# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Property(models.Model):
    _inherit = 'product.template'
    
    property_type_id = fields.Many2one(
        'property.type',
        string='Property Type'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Property Location',
        help='Add Location of property which will be show on website shop on product page.'
    )
    website_product_attachment = fields.Many2many(
        'ir.attachment',
        copy=True,
        help="Select attachment/documents which will be show on website shop on product page.",
        string="Website Attachments"
    )
    
    @api.multi
    def google_map_img(self, zoom=8, width=298, height=298):
        partner = self.sudo().partner_id
        return partner and partner.google_map_img(zoom, width, height) or None

    @api.multi
    def google_map_link(self, zoom=8):
        partner = self.sudo().partner_id
        return partner and partner.google_map_link(zoom) or None
