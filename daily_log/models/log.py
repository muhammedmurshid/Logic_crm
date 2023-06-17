from odoo import models, fields, api, _
from datetime import date, datetime


# from datetime import date, datetime, timedelta


class LoginLogout(models.Model):
    _name = 'res.log'
    _rec_name = 'user_id'
    _description = 'log'

    login_time = fields.Datetime(string='Login Time')
    logout_time = fields.Datetime(string='Logout Time')
    company_id = fields.Many2one('res.company', string="Branch", default=lambda self: self.env.company.id)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user.id)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ], default='draft')
    line_ids = fields.One2many('medium.lines', 'student_id', string="Medium Lines")
    total = fields.Integer(string='Total Leads', compute='compute_total')

    @api.depends('line_ids.count')
    def compute_total(self):
        for j in self:
            t = 0
            for i in j.line_ids:
                t += i.count
            j.total = t

    def action_login(self):
        self.login_time = datetime.now()
        list = ['Direct call', 'Indirect call', 'Whatsapp']

        for i in self:
            for list1 in list:
                i.write({'line_ids': [(0, 0,
                                       {'medium': list1})
                                      ]})

        print(self.line_ids)

        self.state = 'login'

    def action_logout(self):
        self.logout_time = datetime.now()
        self.state = 'logout'

    class ParticipantLines(models.Model):
        _name = "medium.lines"
        _description = "Medium"

        medium = fields.Char(string="Medium")
        count = fields.Integer(string="Count")
        student_id = fields.Many2one('res.log', string="Student")

    class TotalLeads(models.Model):
        _name = 'total.leads'
        _description = 'Total Leads'

        total = fields.Integer(string="Total")
