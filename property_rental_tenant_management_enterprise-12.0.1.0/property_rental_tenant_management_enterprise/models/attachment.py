# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def _hook_warning_employee_check(self, require_employee):
        return True
