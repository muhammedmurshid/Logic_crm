# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CRMStageReport(models.Model):
    _name = 'crm.stage.report'
    _description = 'CRM Stage Wise Report'
    _rec_name = 'crm_id'

    date = fields.Date(string='Date')
    crm_id = fields.Many2one('crm.lead', string='Lead')
    current_stage_id = fields.Many2one('crm.stage', string='Current Stage')
    previous_stage_id = fields.Many2one('crm.stage', string='Previous Stage')
    user_id = fields.Many2one('res.users', string='Salesperson')
    telecaller_id = fields.Many2one(related='crm_lead_id.telecaller_id', string="Telecaller Name", readonly=True)
    # team_id = fields.Many2one('crm.team', string='Sales Team', index=True, tracking=True)
    team_id = fields.Many2one('crm.team', string='Sales Team', compute='_compute_price', strore=True)
    start_date = fields.Date(string='Fresh Lead Date', strore=True)
    # student_id = fields.Many2one(related='crm_id.student_id', store=True)
    phone = fields.Char(related='crm_id.phone', store=True)
    new_team_id = fields.Many2one('crm.team', string='Sales Team', strore=True)

    @api.depends('user_id')
    def _compute_price(self):
        for rec in self:
            # rec.team_id = rec.user_id.sale_team_id.id
            rec.team_id = self.env['crm.team'].with_context( default_team_id=rec.team_id.id
            )._get_default_team_id(user_id=rec.user_id.id)

    def action_change(self):
        stage_report = self.env['crm.stage.report'].search([])
        for i in stage_report:
            # i.new_team_id = i.team_id
            query = 'UPDATE crm_stage_report SET new_team_id = %s where id = %s' % (i.team_id.id, i.id)
            self._cr.execute(query)
