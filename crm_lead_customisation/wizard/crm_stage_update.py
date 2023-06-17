# -*- coding: utf-8 -*-
from odoo import models, fields,_
from odoo.exceptions import ValidationError

class CRMStageUpdate(models.TransientModel):
    _name = 'crm.stage.update'
    _description = 'CRM Stage Update'

    crm_id = fields.Many2one('crm.lead', string='Lead')
    current_stage_id = fields.Many2one('crm.stage', string='Current Stage')
    target_stage_id = fields.Many2one('crm.stage', string='Target Stage')
    student_id = fields.Many2one('res.student', string='Student')

    def change_stage(self):
        drop_stage_id = self.env.ref('crm_ims.stage_drop')
        later_stage_id = self.env.ref('crm_ims.stage_later')
        fresh_stage_id = self.env.ref('crm_ims.stage_fresh_lead')
        to_assign_stage_id = self.env.ref('crm_ims.stage_to_assign')
        if self.target_stage_id == fresh_stage_id:
            self.crm_id.assigned_date = fields.Date.today()
        #user_report
        self.crm_id.stage_id = self.target_stage_id.id
        if self.current_stage_id.name != 'Registration' and self.target_stage_id.name == 'Admission':
            stage_register = self.env.ref('crm_ims.stage_registration')
        if self.crm_id.stage_id.name == 'Admission':
            self.crm_id.status_adm = 'admission'

        if self.target_stage_id.name == 'Drop':
            self.crm_id.drop_date = fields.Date().today()

        if self.target_stage_id.name == 'Interested':
            self.crm_id.interested_date = fields.Date().today()

        if self.target_stage_id.name == 'Intermediate':
            self.crm_id.intermediate_date = fields.Date().today()

        if self.target_stage_id.name == 'RNR':
            self.crm_id.rnr_date = fields.Date().today()

        if self.target_stage_id.name == 'Not Interested':
            self.crm_id.not_interested_date = fields.Date().today()

        if self.target_stage_id.name == 'Later':
            self.crm_id.later_date = fields.Date().today()

        if self.target_stage_id.name == 'Registration':
            if self.student_id.student_status in ('register', 'admission'):
                raise ValidationError(_('Please choose any other state'))
            self.student_id.student_status = 'register'
            self.crm_id.registration_date = fields.Date().today()
            vals = {
                     'name': self.student_id.name,
                     'user_id': self.student_id.user_id.id,
                     'street': self.student_id.street,
                     'street2': self.student_id.street2,
                     'zip': self.student_id.zip,
                     'city': self.student_id.city,
                     'state_id': self.student_id.state_id.id,
                     'country_id': self.student_id.country_id.id,
                     'district': self.student_id.district_id.id,
                     'email': self.student_id.email,
                     'phone': self.student_id.phone,
                     'mobile': self.student_id.mobile,
                     'customer_code': self.student_id.customer_code,
                     'parent_name_ims': self.student_id.parent_name_ims,
                     'parent_occupation': self.student_id.parent_occupation,
                     'parent_phone': self.student_id.parent_phone,
                     'date_of_birth': self.student_id.date_of_birth,
                     'student_status': self.student_id.student_status,
                     'payment_status': self.student_id.payment_status,
                     'student_cost': self.student_id.student_cost,
                     'id_type': self.student_id.id_type,
                     'id_number': self.student_id.id_number,
                     'year_pass': self.student_id.year_pass,
                     'year_experience': self.student_id.year_experience,
                     'website': self.student_id.website,
                     'title': self.student_id.title.id,
                     'category_id': self.student_id.category_id.id,
                     'student_income': self.student_id.student_income,
                     'employee_id': self.student_id.employee_id.id,
                     'batch_id': self.student_id.batch_id.id,
                     'currently_studying': self.student_id.currently_studying,
                     'work_experience': self.student_id.work_experience,
                     'relevant_experience': self.student_id.relevant_experience,
                     'sibling_info': self.student_id.sibling_info,
                     'res_student_id': self.student_id.id,

            }
            partner_id = self.env['res.partner'].sudo().create(vals)
            self.env['res.student'].search([('id', '=', self.student_id.id)]).write({'partner': partner_id})
            return True



        if self.target_stage_id.name == 'Admission':
            if self.student_id.student_status == 'admission':
                raise ValidationError(_('Please choose any other state'))

            if not self.student_id.student_status == 'register':
                self.student_id.student_status = 'admission'
                vals = {
                    'name': self.student_id.name,
                    'user_id': self.student_id.user_id.id,
                    'street': self.student_id.street,
                    'street2': self.student_id.street2,
                    'zip': self.student_id.zip,
                    'city': self.student_id.city,
                    'state_id': self.student_id.state_id.id,
                    'country_id': self.student_id.country_id.id,
                    'district': self.student_id.district_id.id,
                    'email': self.student_id.email,
                    'phone': self.student_id.phone,
                    'mobile': self.student_id.mobile,
                    'customer_code': self.student_id.customer_code,
                    'parent_name_ims': self.student_id.parent_name_ims,
                    'parent_occupation': self.student_id.parent_occupation,
                    'parent_phone': self.student_id.parent_phone,
                    'date_of_birth': self.student_id.date_of_birth,
                    'student_status': self.student_id.student_status,
                    'payment_status': self.student_id.payment_status,
                    'student_cost': self.student_id.student_cost,
                    'id_type': self.student_id.id_type,
                    'id_number': self.student_id.id_number,
                    'year_pass': self.student_id.year_pass,
                    'year_experience': self.student_id.year_experience,
                    'website': self.student_id.website,
                    'title': self.student_id.title.id,
                    'category_id': self.student_id.category_id.id,
                    'student_income': self.student_id.student_income,
                    'employee_id': self.student_id.employee_id.id,
                    'batch_id': self.student_id.batch_id.id,
                    'currently_studying': self.student_id.currently_studying,
                    'work_experience': self.student_id.work_experience,
                    'relevant_experience': self.student_id.relevant_experience,
                    'sibling_info': self.student_id.sibling_info,
                    'res_student_id': self.student_id.id,
                }
                partner_id = self.env['res.partner'].sudo().create(vals)
            else:
                self.student_id.student_status = 'admission'
                vals = {
                    'student_status': self.student_id.student_status
                }
            self.crm_id.admission_date = fields.Date().today()
            if not self.crm_id.registration_date:
                self.crm_id.registration_date = fields.Date().today()

            partner_id = self.env['res.partner'].sudo().search([
                ('res_student_id', '=', self.student_id.id)]).update(vals)
            self.env['res.student'].search([('id', '=', self.student_id.id)]).write({'partner': partner_id})
            return True
