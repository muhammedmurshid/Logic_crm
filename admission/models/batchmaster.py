from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
from datetime import date


class ResDistrict(models.Model):
    _name = 'res.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Batch'

    name = fields.Char(string="Batch Name", index=True, required=1)
    code = fields.Char(string="Batch Code", index=True)
    product_id = fields.Many2one('product.product', string="Course", index=True, required=1)
    company_id = fields.Many2one('res.company', string="Branch", default=lambda self: self.env.company.id, required=1)
    # location = fields.Many2one('res.company',string="Branch", index=True)
    tot_seats = fields.Integer(string="Total Seats", index=True)
    # batch_id = fields.Many2one('res.batch', string="Batch Name")
    student_id = fields.Many2one('res.partner', string="Student")
    # available_seats = fields.Integer(string="Available Seats",compute='_compute_seats', readonly="1", store=True)
    available_seats = fields.Integer(string="Available Seats", compute='_compute_seats', readonly="1", store=True)
    admission_count = fields.Integer(string="Student Count", compute='_compute_student_count', readonly="1")
    approve_id = fields.Many2one('res.users', string="Approved By", default=lambda self: self.env.user.id, readonly="1")
    state = fields.Selection([('draft', 'Draft'),
                              ('active', 'Active'),
                              ('inactive', 'Inactive')], default='draft')
    from_date = fields.Date(string="Start Date")
    to_date = fields.Date(string="End Date")
    is_approve = fields.Boolean(string="Is Approve")
    class_id = fields.Many2one('res.class', string="class")
    adm_id = fields.Many2one('res.admission', string="Admission")
    message_ids = fields.One2many('mail.message', 'res_id', string="Messages")
    create_date = fields.Datetime(string="Create Date", tracking=True, default=date.today())
    approve_date = fields.Date(string="Approve Date", tracking=True)

    def action_approve(self):
        self.state = 'active'
        for i in self:
            i.approve_date = date.today()

    def rfq_approve(self):
        self.is_approve = True

    @api.model
    def test_logic_cron_code(self):
        res = self.env['res.batch'].search([])
        for i in res:
            if i.state in 'active' and i.to_date == date.today() + timedelta(days=1):
                i.state = 'inactive'

    def _compute_student_count(self):
        for i in self:
            admission_ids = self.env['res.admission'].sudo().search(
                [('batch_id', '=', i.id), ('state', '=', 'confirm')])
            if admission_ids:
                i.admission_count = len(admission_ids.mapped('partner_id'))
            else:
                i.admission_count = 0

    @api.depends('tot_seats')
    def _compute_seats(self):
        for i in self:
            count = self.env['res.admission'].sudo().search_count([('batch_id', '=', i.id), ('state', '=', 'confirm')])
            # if count:
            #     i.admission_count = count
            if i.tot_seats:
                i.available_seats = i.tot_seats - count
            if i.available_seats < 0:
                raise ValidationError(
                    _("This Batch is Already Filled"))

    def action_admissions(self):
        admission_ids = self.env['res.admission'].search([('batch_id', '=', self.id), ('state', '=', 'confirm')])
        partner_ids = admission_ids.mapped('partner_id')
        return {
            'name': _('Students'),
            'view_mode': 'kanban,tree,form',
            # 'view_mode': 'tree,form',
            'domain': [('id', '=', partner_ids.ids)],
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'active_test': False},
        }

    # def action_allocation(self):
    #     crm = self.env['classroom.allocate.student'].search([('class_id', '=', self.id)])
    #     return {
    #         'name': _('Task'),
    #         'view_mode': 'form',
    #         'res_model': 'classroom.allocate.student',
    #         'type': 'ir.actions.act_window',
    #         'target': 'new',
    #         "context": {
    #             'default_batch_id': self.id,
    #             'default_student_ids': self.student_id.id,
    #             # 'default_revenue': self.expected_revenue,
    #             # 'default_no_person': self.no_of_persons_package,
    #
    #         },
    #     }
    stu = fields.Many2one('res.partner', 'par')

