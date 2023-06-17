from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CRMTeamWizard(models.TransientModel):
    _name = 'crm.team.wizard'
    _description = 'CRM Team Assign Wizard'

    member_ids = fields.Many2many('res.users', string='Team Member')

    def action_change_team(self):
        stage_list = []
        stage_user_list = []
        stage_user_lists = []
        stage_users_list = []
        for j in self.member_ids:
            stage_report = self.env['crm.stage.report'].search([('user_id', '=', j.id)])
            for i in stage_report:
                stage_list.append(i)
                if i.current_stage_id.is_won:
                    stage_user_list.append(i)
                    stage_user_lists.append(i.id)
        for k in stage_user_list:
            stage_reports = self.env['crm.stage.report'].search([('crm_id', '=', k.crm_id.id)])
            for x in stage_reports:
                stage_users_list.append(x)
        x = [i for i in stage_list if i not in stage_users_list]
        for z in x:
            z.new_team_id = z.team_id