from odoo import fields, models, _


class InheritField(models.Model):
    _inherit = 'crm.lead'

    name_in = fields.Char(string='Mobile Number')
    email_from = fields.Char(string='Mobile Number')


class AccountantPhoneNumber(models.Model):
    _inherit = 'res.company'

    acc_number = fields.Char(string='Accountant Number')
