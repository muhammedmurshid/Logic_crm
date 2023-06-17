import datetime

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    product_order_id = fields.One2many('product.order.line', 'pro_order_id', string='course Order')
    total = fields.Float('Total', compute="_compute_get_total")
    is_admission = fields.Boolean(string='Is Admission', copy=False)
    invoice_id = fields.Many2one('account.move', string="Invoice")
    email_fromm = fields.Char('Email')

    def action_admission(self):
        if len(self.product_order_id.batch_id) == 0:
            raise ValidationError(
                _("Batch is Mandatory For Admission"))
        # for line in self.product_order_id:
        #     if not line.batch_id:
        #         raise ValidationError(
        #             _("Please select Batch for Each courses."))
        if self.phone:
            partner_rec = self.env['res.partner'].search([('phone', '=', self.phone)])
            if partner_rec:
                return {
                    'name': 'Warning',
                    'type': 'ir.actions.act_window',
                    'res_model': 'mobile.duplication.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_crm_id': self.id}
                }
            else:
                student_name = self.env['res.partner'].sudo().create({
                    'company_type': 'person',
                    'name': self.student_name,
                    'phone': self.phone,
                    'street': self.street,
                    'street2': self.street2,
                    'city': self.city,
                    'state_id': self.state_id.id,
                    'zip': self.zip,
                    'country_id': self.country_id.id,
                    'parent_name': self.parent_name,
                    'mother_name': self.mother_name,
                    'mother_no': self.mother_no,
                    'father_name': self.father_name,
                    'father_no': self.father_no,
                    'mobile': self.whatsapp_no,
                    'contact_type': 'student',
                    'type': 'contact',
                })

                for line in self.product_order_id:
                    admission = self.env['res.admission'].sudo().create({
                        'company_id': line.company_id.id,
                        'partner_id': student_name.id,
                        'product_id': line.product_id.id,
                        'batch_id': line.batch_id.id,
                        'course_fee': line.course_fee,
                        'amount_total': line.course_fee,
                        'crm_lead_id': self.id,
                        'user_id': self.user_id.id,
                        'lead': self.id,
                    })
                    admission.write({
                        'course_ids': [(0, 0, {
                            'course_id': line.product_id.id,
                            'fee': line.course_fee
                            # 'taxes_id': val.tax
                        })]
                    })
            self.is_admission = True

    def admission_action(self):
        admission_ids = self.env['res.admission'].search(
            [('batch_id', '=', self.id), ('crm_lead_id', '=', self.id), ('state', '=', 'draft'), ])
        partner_ids = admission_ids.mapped('partner_id')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Admission',
            'res_model': 'res.admission',
            'domain': [('crm_lead_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
        self.is_admission = True
    @api.depends('product_order_id.course_fee')
    def _compute_get_total(self):
        request = self.product_order_id
        self.total = False
        for sel in request:
            if sel.course_fee >= 0:
                self.total += sel.course_fee


    @api.onchange('total')
    def onchange_total(self):
        if self.total:
            self.expected_revenue = self.total


class ProductOrderLine(models.Model):
    _name = "product.order.line"
    _description = "Product Order Line"

    pro_order_id = fields.Many2one('crm.lead', required=True)
    product_id = fields.Many2one("product.product", string="Course", required=True, track=True)
    batch_id = fields.Many2one('res.batch', string="Batch" )
    course_fee = fields.Float(string="Course Fee")
    course_id = fields.Many2one('crm.lead', string='Add Course')
    company_id = fields.Many2one('res.company', string="Branch", track=True)
    slno = fields.Integer('No.', compute="_compute_get_number", store=True)
    available_seats = fields.Integer(related='batch_id.available_seats', string="Available Seats")
    stage_id = fields.Many2one('crm.stage', string='Stage', related='pro_order_id.stage_id')
    category_id = fields.Many2one('product.category', string='Category')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.product_id.list_price:
                self.course_fee = self.course_fee = self.product_id.list_price + self.product_id.list_price * self.product_id.taxes_id.amount/100

    @api.depends('pro_order_id.product_order_id', 'pro_order_id.product_order_id.product_id')
    def _compute_get_number(self):
        for line in self:
            no = 0
            line.slno = no
            for l in line.pro_order_id.product_order_id:
                no += 1
                l.slno = no
