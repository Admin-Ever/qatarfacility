# -*- coding: utf-8 -*-

from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsitepropertyVariant(WebsiteSale):
    
    def _attributes_value(self, variant, attribute_value_ids,visible_attribute_ids,website_price,price, product):
        return attribute_value_ids
    
    def get_attribute_value_ids(self, product):
        product = product.with_context(quantity=1)
        visible_attrs_ids = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped('attribute_id').ids
        to_currency = request.website.get_current_pricelist().currency_id
        attribute_value_ids = []
        for variant in product.product_variant_ids:
            if to_currency != product.currency_id:
                price = variant.currency_id.compute(variant.website_public_price, to_currency)
            else:
                price = variant.website_public_price
            visible_attribute_ids = [v.id for v in variant.attribute_value_ids if v.attribute_id.id in visible_attrs_ids]
            website_price = variant.website_price
            attribute_value_ids = self._attributes_value(variant, attribute_value_ids,visible_attribute_ids,website_price,price, product)
        return attribute_value_ids
    
