from datetime import date

from odoo import models, fields, api, _


class CRMAssignWizard(models.TransientModel):
    _inherit = 'crm.assign.wizard'

    current_stage_id = fields.Many2one('crm.stage', string='Current Stage')

    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.crm_id and self.crm_id.stage_id:
            self.current_stage_id = self.crm_id.stage_id.id

    def assign_crm(self):
        res = super(CRMAssignWizard, self).assign_crm()
        today = date.today()
        self.crm_id.fresh_lead_date = today
        self.env['crm.stage.analysis.report'].create({
            'crm_id': self.crm_id.id,
            'student_name': self.crm_id.student_name,
            'email_from': self.crm_id.email_from,
            'phone': self.crm_id.phone,
            'phone_same_tick': self.crm_id.phone_same_tick,
            'whatsapp': self.crm_id.whatsapp_no,
            'date_deadline': self.crm_id.date_deadline,
            'create_date': self.crm_id.create_date,
            'update_date': today,
            'medium_id': self.crm_id.medium_id.id,
            'user_id': self.crm_id.user_id.id,
            'telecaller_id': self.crm_id.telecaller_id.id,
            'team_id': self.crm_id.team_id.id,
            'finance_partner': self.crm_id.finance_partner.id,
            'fin_partner_need': self.crm_id.fin_partner_need,
            'mode_of_study': self.crm_id.mode_of_study,
            'company_id': self.crm_id.company_id.id,
            'last_institution': self.crm_id.last_institution,
            'parent_name': self.crm_id.parent_name,
            'stage_id': self.crm_id.stage_id.id,
            'previous_stage_id': self.current_stage_id.id,
        })
        return res


class CRMAssignMulti(models.TransientModel):
    _inherit = 'crm.assign.multi'

    current_stage_id = fields.Many2one('crm.stage', string='Current Stage')

    # @api.onchange('user_id')
    # def _onchange_user_id(self):
    #     if self.crm_id and self.crm_id.stage_id:
    #         self.current_stage_id = self.crm_id.stage_id.id

    def assign_crm_multi(self):
        res = super(CRMAssignMulti, self).assign_crm_multi()
        print(self)
        record_ids = self._context.get('active_ids')
        print(record_ids)
        for i in record_ids:
            crm = self.env['crm.lead'].search([('id', '=', i)])
            today = date.today()
            crm.fresh_lead_date = today
            x = self.env['crm.stage.analysis.report'].create({
                'crm_id': crm.id,
                'student_name': crm.student_name,
                'email_from': crm.email_from,
                'phone': crm.phone,
                'phone_same_tick': crm.phone_same_tick,
                'whatsapp': crm.whatsapp_no,
                'date_deadline': crm.date_deadline,
                'create_date': crm.create_date,
                'update_date': today,
                'medium_id': crm.medium_id.id,
                'user_id': crm.user_id.id,
                'telecaller_id': crm.telecaller_id.id,
                'team_id': crm.team_id.id,
                'finance_partner': crm.finance_partner.id,
                'fin_partner_need': crm.fin_partner_need,
                'mode_of_study': crm.mode_of_study,
                'company_id': crm.company_id.id,
                'last_institution': crm.last_institution,
                'parent_name': crm.parent_name,
                'stage_id': crm.stage_id.id,
                # 'previous_stage_id': i.current_stage_id.id,
            })
            print(x)
        return res
