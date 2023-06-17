from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
from datetime import date


class DueMaster(models.Model):
    _name = 'due.master'
    # _rec_name = 'name'
    _description = 'Due'

    due_date = fields.Date(string="Due Date")
    admission_number = fields.Char(string="Admission Number")
    partner = fields.Char(string="Student")
    course = fields.Char(string='Course')
    pending_fee = fields.Float(string="Fee To Be Paid")