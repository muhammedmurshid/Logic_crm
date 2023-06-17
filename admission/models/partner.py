from odoo import models, fields, api, _, exceptions


class ResPartner(models.Model):
    _inherit = "res.partner"

    parent_name = fields.Char(string='Parent Name')
    whats_app = fields.Char(string='Whats App No')
    reference = fields.Char(string='Student ID', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    aadhar_no = fields.Char(string='Aadhar Number')
    mother_name = fields.Char(string="Mother's Name")
    mother_no = fields.Char(string="Mother's Number")
    father_name = fields.Char(string="Father's Name")
    father_no = fields.Char(string="Father's Number")
    admission_fee = fields.Float(string="Admission_fee")
    admission_id = fields.Many2one('res.admission',string="Admission")
    amount_due = fields.Float(string="Amount Due",compute='_compute_pending')
    class_ids = fields.Many2many('res.class',string="Class")

    @api.constrains('phone', 'aadhar_no')
    def check_mobile(self):
        for rec in self:
            if rec.phone:
                partner_rec = self.env['res.partner'].search(
                    [('phone', '=', rec.phone),
                     ('id', '!=', rec.id)])
                if partner_rec:
                    raise exceptions.ValidationError(_('Exists ! Already a contact exists in this phone number'))
            if rec.aadhar_no:
                partner_rec = self.env['res.partner'].search(
                    [('aadhar_no', '=', rec.aadhar_no),
                     ('id', '!=', rec.id)])
                if partner_rec:
                    raise exceptions.ValidationError(_('Exists ! Aadhar Number Already Exists '))

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New') and vals.get('contact_type') == 'student':
            vals['reference'] = self.env['ir.sequence'].next_by_code('res.partner') or _('New')
        res = super(ResPartner, self).create(vals)
        return res

    @api.depends('admission_id')
    def _compute_pending(self):
        for k in self:
            partner = self.env['res.admission'].sudo().search([('partner_id', '=', k.id)])
            tot = 0
            for i in partner:
                if i.balance:
                    tot += i.balance
            k.amount_due = tot

        # for tot in self.partner_id.admission_id.balance:
        #     if tot.balance:
        #         self.amount_due += tot.balance

    def action_open_admission(self):
        print("ooooooooooooooooooo")
        for i in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Admission',
                'res_model': 'res.admission',
                'view_mode': 'tree,form',
                'target': 'current',
                'domain': [('partner_id', '=', i.id)]
                # 'domain' : 'admission_id'= self.partner_id
        }

    def action_open_class(self):
        x = self.env['student.lines'].search([('student_id', '=', self.id)])
        y = x.mapped('line_id')
        print(y, x)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Class',
            'res_model': 'res.class',
            'view_mode': 'tree',
            'target': 'current',
            'domain': [('id', 'in', y.ids)]
        }

