from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError



class CrmLead(models.Model):
    _inherit = 'crm.lead'

    student_name = fields.Char(string='Candidate')
    fresh_lead_date = fields.Date('Fresh Lead Date')

    def crm_update_stage(self):
        view = self.env.ref('crm_lead_cust.crm_stage_update_wizard_view_form')
        return {
            'name': _('Update Stage'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view.id,
            'res_model': 'crm.stage.update',
            'context': {
                'default_crm_id': self.id,
                'default_current_stage_id': self.stage_id.id,
            },
            'target': 'new',
        }
