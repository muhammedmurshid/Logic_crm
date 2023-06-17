# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError

class LeadConversionWizard(models.TransientModel):
    _name = 'lead.conversion.wizard'

    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    user_ids = fields.Many2many('res.users', string="Salesperson")
    team_ids = fields.Many2many('crm.team', string="Sales Team")
    source_id = fields.Many2one('utm.source', "Source")
    conversion_stage_from = fields.Selection([('fresh_lead', 'Fresh Lead'),('registration', 'Registration')])
    conversion_stage_to = fields.Selection([('registration', 'Registration'), ('admission', 'Admission'),('drop', 'Drop'), ('later', 'Later')])
    based_on = fields.Selection([('salesperson','Salesperson'), ('salesteam','Sales Team')], string="Based On", default='salesperson')

