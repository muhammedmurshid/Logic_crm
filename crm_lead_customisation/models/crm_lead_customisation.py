from datetime import date

import dateutil.utils
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ResPartnerCustomisation(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection(
        [('finance', 'Finance'), ('student', 'Student'), ('vendor', 'Vendor'), ('employee', 'Employee'),
         ('other', 'Others'), ],
        string='Contact Type')
    employee_type = fields.Selection([('teacher','Teacher'),('non_teaching_staff','Non Teaching Staff')])


class CrmLeadCustomisation(models.Model):
    _inherit = 'crm.lead'

    opportunity_seq_no = fields.Char(string='Opportunity No:')
    student_name = fields.Char(string='Student Name')
    parent_name = fields.Char(string="Parent Name")
    parent_no = fields.Char(string="Parent No")
    last_institution = fields.Char(string="Last Institution Studied")
    course_studied = fields.Char(string="Course Studied")
    phone_same_tick = fields.Boolean(string='Whatsapp No same as Phone No')
    whatsapp_no = fields.Char(string='Whatsapp No')
    lead_source_emp_name = fields.Char(string='Employee Name')
    finance_partner = fields.Many2one('res.partner', string="Finance Partner")
    fin_partner_need = fields.Selection([('yes', 'Yes'), ('no', 'No'), ], string="Financial Partner Needed")
    mode_of_study = fields.Selection([('online', 'Online'), ('offline', 'Offline'), ],
                                     string='Mode Of Study')
    posibility = fields.Selection([ ('cold', 'Cold'), ('warm', 'Warm'), ('hot', 'Hot')], string='Possibility Of Conversion')
    telecaller_id = fields.Many2one('res.users', string="Telecaller")
    stage = fields.Char(related="stage_id.name", string="Stage")
    mother_name = fields.Char(string="Mother's Name")
    mother_no = fields.Char(string="Mother's Number")
    father_name = fields.Char(string="Father's Name")
    father_no = fields.Char(string="Father's Number")
    is_qualified = fields.Boolean(string='Is Qualified')

    # @api.constrains('phone')
    # def _check_name(self):
    #     for rec in self:
    #         if rec.phone:
    #             a = self.env.ref('crm_lead_customisation.stage_admission')
    #             number_rec = self.env['crm.lead'].search(
    #                 [('phone', '=', rec.phone),
    #                  ('stage_id', '!=', a.id)
    #                  ])
    #             if len(number_rec) > 1:
    #                 raise ValidationError(_('Student with the same Number already exists!'))

    _sql_constraints = [
        ('phone_mother_no_father_no', 'unique(phone, mother_no, father_no)', 'Phone Number is Already Present.'),
    ]
    @api.model
    def create(self, vals):
        if vals.get('opportunity_seq_no', _('New')) == _('New'):
            vals['opportunity_seq_no'] = self.env['ir.sequence'].next_by_code('sequence.number') or _('New')
        res = super(CrmLeadCustomisation, self).create(vals)
        return res

    @api.onchange('phone_same_tick')
    def onchange_mob_tick(self):
        if self.phone_same_tick:
            self.whatsapp_no = self.phone
        else:
            self.whatsapp_no = False

    def assign_lead(self):
        return {
            'name': _('Select A User'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'crm.assign.wizard',
            'context': {
                'default_crm_id': self.id,
                'default_previous_user_id': self.user_id.id,
            },
            'target': 'new',
        }

    @api.model
    def _crm_stage_update(self):
        adm_stage = self.env['crm.stage'].search([('name', '=', 'Admission')], limit=1)
        deadline = self.env['crm.lead'].search([])
        tod_date = date.today()
        for i in deadline:
            if i.stage_id != adm_stage.id:
                if i.date_deadline:
                    if i.date_deadline + relativedelta(days=1) == tod_date:
                        i.user_id = i.team_id.user_id.id

    @api.onchange('student_name')
    def _onchange_student_name(self):
        if self.student_name:
            self.name = self.student_name





    # @api.onchange('telecaller_id')
    # def onchange_telecaller_id(self):
    #     oldstage = self.user_id
    #     self.user_id = self.tele_old_id
    #     self.tele_old_id = oldstage

class CRMStage(models.Model):
    _inherit = 'crm.stage'

    # def write(self, vals):
    #     raise UserError(_('Stages cannot be edited'))
