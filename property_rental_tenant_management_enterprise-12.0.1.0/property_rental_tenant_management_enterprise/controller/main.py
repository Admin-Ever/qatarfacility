# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

class Websiteproperty(WebsiteSale):
    
    def _attributes_value(self, variant, attribute_value_ids,visible_attribute_ids,website_price,price, product):
        if not variant.is_reserved:
            attribute_value_ids.append([variant.id, visible_attribute_ids, variant.website_price, price])
        return attribute_value_ids
        
class ProductInquiry(http.Controller):
    @http.route(['/shop_inquiry/property_getinquiry'], type='http', auth="public", website=True)
    def create_quote(self, **kwargs):
        user_id = request.env.user
        phone = kwargs.get('phone')
        broker = kwargs.get('broker')
        product_template = int(kwargs.get('product_template'))
        comment = kwargs.get('comment')
        product_template_id = request.env['product.template'].sudo().browse(product_template)
        product_id = int(kwargs.get('product_id'))
        product = request.env['product.product'].browse(product_id)
        if request.env.ref('base.public_user') == user_id:
            email = kwargs.get('email')
            partner_id = request.env['res.partner'].sudo().search([('email', '=', email)])
            if not partner_id:
                values = {
                    'name':kwargs.get('name'),
                    'email':kwargs.get('email'),
                }
                partner_id = request.env['res.partner'].sudo().create(values)
            else:
                partner_id = partner_id[0]
        else:
            partner_id = user_id.partner_id
        
        if product.attribute_value_ids:
            description = comment + ' for ' + str(product_template_id.name) + ' - ' + str(product.attribute_value_ids.name) +' with '+ str(kwargs.get('quantity')) + ' Quantity'
            name = product_template_id.name +' - '+ product.attribute_value_ids.name
        else:
            description = comment + ' for ' + str(product_template_id.name) + ' with '+ str(kwargs.get('quantity')) + ' Quantity'
            name = product_template_id.name
        values = {
                'name': name,
                'email_from' : kwargs.get('email'),
                'partner_id' : partner_id.id,
                'phone' : phone,
                'description': description,
                'broker_name' : broker,
                'product_id' : product.id,
                'type': ('lead')
                }
        lead_id = request.env['crm.lead'].sudo().create(values)
        print ("lead_id:------------------------",lead_id)
        return request.render('property_rental_tenant_management_enterprise.inquiry_thanks')

