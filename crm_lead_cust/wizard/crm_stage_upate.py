from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CRMStageUpdate(models.TransientModel):
    _name = 'crm.stage.update'
    _description = 'CRM Stage Update Wizard'

    current_stage_id = fields.Many2one('crm.stage', string='Current Stage')
    new_stage_id = fields.Many2one('crm.stage', string='New Stage')
    crm_id = fields.Many2one('crm.lead', string='CRM Id')

    def update_stage(self):
        self.crm_id.stage_id = self.new_stage_id.id
        if self.crm_id.stage_id.name == 'Qualified' or 'Admission':
            self.crm_id.is_qualified = True
            if len(self.crm_id.product_order_id) == 0:
                raise ValidationError(
                    _("Course Details is Mandatory For Admission"))
        today = date.today()
        self.env['crm.stage.analysis.report'].create({
            'crm_id': self.crm_id.id,
            'student_name': self.crm_id.student_name,
            'email_from': self.crm_id.email_from,
            'phone': self.crm_id.phone,
            'phone_same_tick': self.crm_id.phone_same_tick,
            'whatsapp': self.crm_id.whatsapp_no,
            'date_deadline': self.crm_id.date_deadline,
            'update_date': today,
            'create_date': self.crm_id.create_date,
            'user_id': self.crm_id.user_id.id,
            'telecaller_id':self.crm_id.telecaller_id.id,
            'medium_id': self.crm_id.medium_id.id,
            'team_id': self.crm_id.team_id.id,
            'finance_partner': self.crm_id.finance_partner.id,
            'fin_partner_need': self.crm_id.fin_partner_need,
            'mode_of_study': self.crm_id.mode_of_study,
            'company_id': self.crm_id.company_id.id,
            'last_institution': self.crm_id.last_institution,
            'parent_name': self.crm_id.parent_name,
            'stage_id': self.new_stage_id.id,
            'previous_stage_id': self.current_stage_id.id,
        })
