from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError


class PaymentNotes(models.Model):
    _inherit = 'res.partner'

    due_ids = fields.One2many('due.notes', 'due_id', string='Due')
    amount_due_cus = fields.Float(string='Amount Due')


class DueNotes(models.Model):
    _name = 'due.notes'

    student = fields.Many2one('res.partner', string='Student')
    course_id = fields.Many2one('product.product', string='Course')
    total_amount = fields.Float(string='Total')
    amount_due = fields.Float(string='Amount Due')
    due_id = fields.Many2one('res.partner')


class ActionPaymentDue(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        print('kkk')
        ss = self.env['res.partner'].search([])
        bb = self.env['account.move'].search([])
        oo = []
        for ii in bb:
            # print(bb.partner_id.name, 'par')
            if ii.name == self.communication:
                for j in ss:
                    if ii.partner_id.id == j.id:

                        print('yes')
                        print(j.name, 'paar')
                        res_list = {
                            'student': ii.partner_id.id,
                            # 'classroom_id': self.class_room.name,
                            'course_id': ii.product_id.id,
                            'total_amount': ii.amount_total,
                            'amount_due': self.payment_difference,
                        }
                        oo.append((0, 0, res_list))
                        j.due_ids = oo
                        j.amount_due_cus = self.payment_difference
                        res = super(ActionPaymentDue, self).action_create_payments()
                        return res

            else:
                print('no')
                res = super(ActionPaymentDue, self).action_create_payments()
                return res


class ActionPaymentChange(models.Model):
    _inherit = 'account.move'

    def action_register_payment(self):
        if self.partner_id.contact_type == 'student':
            if not self.admission_id:
                raise UserError(_("Admission Fee Not Paid"))
            else:
                res = super(ActionPaymentChange, self).action_register_payment()
                return res
        else:
            res = super(ActionPaymentChange, self).action_register_payment()
            return res





