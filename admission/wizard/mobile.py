from odoo import fields, models, _


class MobileDuplicationWizard(models.TransientModel):
    _name = 'mobile.duplication.wizard'

    crm_id = fields.Many2one('crm.lead', string='CRM')

    def action_update(self):
        i = self.env['res.partner'].search([('phone', '=', self.crm_id.phone)])
        if i.id:
            for line in self.crm_id.product_order_id:
                admission = self.env['res.admission'].sudo().create({
                    'company_id': line.company_id.id,
                    'partner_id': i.id,
                    'product_id': line.product_id.id,
                    'batch_id': line.batch_id.id,
                    'course_fee': line.course_fee,
                    'crm_lead_id': self.crm_id.id,
                    'user_id': self.crm_id.user_id.id,
                    'lead': self.crm_id.id,
                })
                admission.write({
                    'course_ids': [(0, 0, {
                        'course_id': line.product_id.id,
                        'fee': line.course_fee
                        # 'taxes_id': val.tax
                    })]
                })
            self.crm_id.is_admission = True

