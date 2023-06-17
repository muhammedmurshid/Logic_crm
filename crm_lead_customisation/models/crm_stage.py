# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, api, _


class CRMStage(models.Model):
    _inherit = 'crm.stage'

    def write(self, vals):
        raise UserError(_('Stages cannot be edited'))

