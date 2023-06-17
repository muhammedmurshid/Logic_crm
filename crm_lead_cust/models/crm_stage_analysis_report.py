from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CrmStageAnalysisReport(models.Model):
    _name = 'crm.stage.analysis.report'
    _rec_name = 'crm_id'

    student_name = fields.Char(string='Student')
    crm_id = fields.Many2one('crm.lead', string='CRM Id')
    email_from = fields.Char(string='Email')
    phone = fields.Char('Phone')
    phone_same_tick = fields.Boolean(string='Whatsapp No same as Phone No')
    whatsapp = fields.Char(string='Whatsapp')

    date_deadline = fields.Date('Expected Closing')
    create_date = fields.Date('Create Date')
    update_date = fields.Date('Update Date')
    medium_id = fields.Many2one('utm.medium', string='Medium')

    user_id = fields.Many2one('res.users', string='Sales Person')
    team_id = fields.Many2one('crm.team', string='Team')
    finance_partner = fields.Many2one('res.partner', string="Finance Partner")
    fin_partner_need = fields.Selection([('yes', 'Yes'), ('no', 'No'), ], string="Financial Partner Needed")
    mode_of_study = fields.Selection([('online', 'Online'), ('offline', 'Offline'), ],
                                     string='Mode Of Study')

    company_id = fields.Many2one('res.company', string='Company')
    last_institution = fields.Char(string="College")
    parent_name = fields.Char(string="Parent Name")
    stage_id = fields.Many2one('crm.stage', 'Current Stage')
    previous_stage_id = fields.Many2one('crm.stage', 'Previous Stage')
    telecaller_id = fields.Many2one('res.users', string="Telecaller Name", readonly=True)





