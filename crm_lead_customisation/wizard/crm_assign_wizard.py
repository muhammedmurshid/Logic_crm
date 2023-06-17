# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CRMAssignWizard(models.TransientModel):
    _name = 'crm.assign.wizard'
    _description = 'CRM User Assign Wizard'

    crm_id = fields.Many2one('crm.lead', string='Lead')
    user_id = fields.Many2one('res.users', string='Assign To')
    assign_deadline = fields.Date(string='Deadline')
    previous_user_id = fields.Many2one('res.users', string='Previous User')
    # telecaller_id = fields.Many2one('res.users', string='Telecaller')


    def assign_crm(self):
        drop_stage_id = self.env.ref('crm_lead_customisation.stage_drop')
        later_stage_id = self.env.ref('crm_lead_customisation.stage_later')
        current_stage_id = self.env.ref('crm_lead_customisation.stage_fresh_lead')
        to_assign_stage_id = self.env.ref('crm_lead_customisation.stage_to_assign')
        to_registration_stage_id = self.env.ref('crm_lead_customisation.stage_qualified')
        to_admission_stage_id = self.env.ref('crm_lead_customisation.stage_admission')


        if self.user_id.id != self.previous_user_id.id:
            if self.crm_id.stage_id not in (to_registration_stage_id , to_admission_stage_id) :
                self.crm_id.date_deadline = self.assign_deadline
                self.crm_id.user_id = self.user_id.id
                self.crm_id.telecaller_id = self.user_id.id
                current_stage_id = self.env.ref('crm_lead_customisation.stage_fresh_lead')
                previous_stage_id = self.env.ref('crm_lead_customisation.stage_to_assign')
                var = self.crm_id.stage_id
                self.crm_id.stage_id = current_stage_id.id
            elif self.crm_id.stage_id == to_registration_stage_id:
                pre_user = self.crm_id.user_id
                self.crm_id.telecaller_id = pre_user.id
                self.crm_id.user_id = self.user_id.id




            elif (self.crm_id.stage_id == drop_stage_id) or (self.crm_id.stage_id == later_stage_id):
                self.crm_id.date_deadline = fields.Date.today()
                self.crm_id.user_id = self.user_id.id
                stage = self.crm_id.stage_id

                self.crm_id.stage_id = current_stage_id.id



                self.crm_id.telecaller_id = self.telecaller_id
                self.env['crm.user.report'].create({
                    'date': fields.Date.today(),
                    'crm_id': self.crm_id.id,
                    'assigned_stage_id': current_stage_id.id,
                    'status': 'in_progress',
                    'user_id': self.user_id.id,

                })
                res_model_id = self.env['ir.model'].search(
                    [('model', '=', 'crm.lead')]).id
                activity_type_id = self.env['mail.activity.type'].search(
                    [('name', '=', 'Call')], limit=1).id
                self.env['mail.activity'].create({
                    'res_model_id': res_model_id,
                    'activity_type_id': activity_type_id,
                    'res_id': self.crm_id.id,
                    'date_deadline': self.assign_deadline,
                    'user_id': self.user_id.id,
                })

            else:
                print('else')

                self.crm_id.user_id = self.user_id.id
            return
        elif self.user_id.id == self.previous_user_id.id:
            raise ValidationError(_('You can not Assign with the same User!'))


class CRMAssignMulti(models.TransientModel):
    _name = 'crm.assign.multi'
    _description = 'CRM User Assign Wizard'

    @api.model
    def default_get(self, fields):
        record_ids = self._context.get('active_ids')
        result = super(CRMAssignMulti, self).default_get(fields)

        if record_ids:
            opp_ids = self.env['crm.lead'].browse(record_ids).ids
            result['opportunity_ids'] = [(6, 0, opp_ids)]
        return result

    crm_id = fields.Many2one('crm.lead', string='Lead')
    user_id = fields.Many2one('res.users', string='Assign To')
    previous_user_id = fields.Many2one('res.users', string='Previous User')
    opportunity_ids = fields.Many2many('crm.lead', 'assign_opportunity_rel', 'assign_id', 'opportunity_id', string='Leads/Opportunities')
    assign_deadline = fields.Date(string='Deadline')


    def assign_crm_multi(self):

        for lead in self.opportunity_ids:
            drop_stage_id = self.env.ref('crm_lead_customisation.stage_drop')
            later_stage_id = self.env.ref('crm_lead_customisation.stage_later')
            current_stage_id = self.env.ref('crm_lead_customisation.stage_fresh_lead')
            # to_stage_rnr_id = self.env.ref('crm_lead_customisation.stage_rnr')
            to_stage_not_interested_id = self.env.ref('crm_lead_customisation.stage_not_interested')

            var = lead.stage_id

            if not lead.date_deadline:
                lead.date_deadline = fields.Date.today()
                lead.user_id = self.user_id.id
                stage = lead.stage_id
                lead.stage_id = current_stage_id.id
                res_model_id = self.env['ir.model'].search(
                    [('model', '=', 'crm.lead')]).id
                activity_type_id = self.env['mail.activity.type'].search(
                    [('name', '=', 'Call')], limit=1).id
                self.env['mail.activity'].create({
                    'res_model_id': res_model_id,
                    'activity_type_id': activity_type_id,
                    'res_id': lead.id,
                    'date_deadline': fields.Date.today(),
                    'user_id': self.user_id.id,
                })

            elif lead.stage_id == to_stage_not_interested_id:
                lead.user_id = self.user_id.id
                previous_stage_id = self.env.ref('crm_lead_customisation.stage_to_assign')

            elif (lead.stage_id == drop_stage_id) or (lead.stage_id == later_stage_id):
                lead.date_deadline = fields.Date.today()
                lead.user_id = self.user_id.id
                stage = lead.stage_id
                lead.stage_id = current_stage_id.id


                res_model_id = self.env['ir.model'].search(
                    [('model', '=', 'crm.lead')]).id
                activity_type_id = self.env['mail.activity.type'].search(
                    [('name', '=', 'Call')], limit=1).id
                self.env['mail.activity'].create({
                    'res_model_id': res_model_id,
                    'activity_type_id': activity_type_id,
                    'res_id': lead.id,
                    'date_deadline': fields.Date.today(),
                    'user_id': self.user_id.id,
                })

            else:
                 lead.user_id = self.user_id.id






