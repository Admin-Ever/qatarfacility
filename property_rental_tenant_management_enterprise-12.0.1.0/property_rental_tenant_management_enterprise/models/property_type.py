# -*- coding: utf-8 -*-

from odoo import models, fields

class PropertyType(models.Model):
    _name = "property.type"

    name = fields.Char(
        string='Property Type',
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
