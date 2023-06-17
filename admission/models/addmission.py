from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError


class ResAdmission(models.Model):
    _name = 'res.admission'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Admission'

    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Admission Number', required=True, copy=False, readonly=True,
                            default=lambda self: _('Draft'))
    partner_id = fields.Many2one('res.partner', string='Student', store=True)
    company_id = fields.Many2one('logic.branches', string="Branch")
    course_ids = fields.One2many('course.lines','res_id',string="Fee Details")
    batch_id = fields.Many2one('res.batch', string="Batch")
    product_id = fields.Many2one("product.product", string="Course", required=True,store=True)
    course_fee = fields.Float(string="Course Fee", store=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    crm_lead_id = fields.Many2one('crm.lead', string='Lead')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('transfer', 'Transfer'),('cancel','Cancel'),('drop','Dropped')], default='draft', string='Status', store=True)
    student_id = fields.Char(related='partner_id.reference', string="Student ID", store=True)
    admission_date = fields.Date(string='Admission Date', default=date.today())
    phone = fields.Char(related='partner_id.phone',string="Mobile", store=True)
    lead = fields.Integer(string='Lead')
    telecaller_id = fields.Many2one(related='crm_lead_id.telecaller_id', string="Telecaller Name", readonly=True)
    class_id = fields.Many2one('res.class', string="Class")
    cost = fields.Float(string="Total", compute='_compute_cost',store=True)
    total = fields.Float(string="Total",compute='_compute_total',store=True)
    other_fees = fields.Float(string="Total")
    amount_total = fields.Float(string="Total Amount")
    admission_fee = fields.Float(related='partner_id.admission_fee',string="Admission Fee",store=True)
    balance = fields.Float(string="Balance",compute="_compute_balance",store=True)
    # payment_term_id = fields.Many2one('account.payment.term',string="Payment Terms")
    message_ids = fields.One2many('mail.message','res_id',string="Messages")

    @api.model
    def create(self, vals):
        if vals.get('name', _('Draft')) == _('Draft'):
            vals['name'] = self.env['ir.sequence'].next_by_code('res.admission') or _('Draft')
        res = super(ResAdmission, self).create(vals)
        return res


    def action_confirm(self):
        self.state = 'confirm'
        # if self.admission_fee == 0:
        #     raise ValidationError(
        #     _("Admission Fee Not Paid"))
        if self.partner_id.contact_type == 'student':
            print('itd stud')
            if self.admission_fee == 0:
                raise ValidationError(
                    _("Admission Fee Not Paid"))
        for i in self:
            if i.batch_id.sudo().available_seats <= 0:
                raise ValidationError(
                    _("Required number of seats are not available in the batch ( %s )!") % i.batch_id.sudo().name)
            i.batch_id.sudo()._compute_seats()

    def action_transfer(self):
        self.state = 'transfer'
    def action_drop(self):
        self.state = 'drop'

    def action_cancel(self):
        self.state = 'cancel'


    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.product_id.list_price:
                self.course_fee = self.product_id.list_price
    @api.depends('course_ids.fee')
    def _compute_cost(self):
        for c in self:
            request = self.course_ids
            c.cost = False
            for sel in request:
                if sel.fee >= 0:
                    c.cost += sel.fee - sel.discount_amount
    @api.depends('course_ids.advance_fee')
    def _compute_total(self):
        for t in self:
            request = t.course_ids
            t.total = False
            for sel in request:
                if sel.advance_fee >= 0:
                    t.total += sel.advance_fee

    @api.depends('course_fee','total')
    def _compute_balance(self):
        for i in self:
            i.balance = False
            if i.course_fee >0:
                i.balance = i.cost - i.total
                bal = self.env['student.lines'].search([('student_id','=',i.partner_id.id),('batch_id','=',i.batch_id.id),('ad_id','=',i.id)])
                bal.update({
                    'pending_fee':i.balance
                 })

class CourseLines(models.Model):
    _name = "course.lines"

    res_id = fields.Many2one('res.admission')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    # invoiced_bool = fields.Boolean(string='Invoiced')
    course_id = fields.Many2one('product.product', string="Type")
    date = fields.Date(string='Due Date')
    fee = fields.Float(string="Total Course Fee")
    advance_fee = fields.Float(string="Amount Received")
    payment_status = fields.Selection([
        ('1', 'Payment Completed'),
        ('2', 'Payment Incomplete'),],default='2', string="Payment Status")
    pending_fee = fields.Float(string="Pending Fee" ,compute="_compute_pending_fee")
    discount_amount = fields.Float(string='Discount Amount')


    @api.onchange('course_id')
    def onchange_course_id(self):
        if self.course_id:
            if self.course_id.list_price:
                self.fee = self.course_id.list_price + self.course_id.list_price * self.course_id.taxes_id.amount / 100

    @api.depends('fee','advance_fee')
    def _compute_pending_fee(self):
        self.pending_fee = 0
        for i in self:
            if i.fee:
                i.pending_fee = i.fee - i.advance_fee-i.discount_amount
                # due = self.env['student.lines'].search(
                #     [('ad_id', '=', self.res_id.id), ('student_id', '=', self.res_id.partner_id.id),
                #      ('batch_id', '=', self.res_id.batch_id.id)])
                # due.update({
                #     'pending_fee': i.pending_fee
                # })
class AccountMove(models.Model):
    _inherit = "account.move"

    student = fields.Char(related='partner_id.reference', string="Student ID", store=True)
    admission_id = fields.Many2one('res.admission',string="Admission Number")
    crm_lead_id = fields.Many2one('crm.lead', string='Lead')
    company_id = fields.Many2one('res.company', string="Branch")
    product_id = fields.Many2one('product.product',related='admission_id.product_id',string = "Course")
    batch_id = fields.Many2one('res.batch',string = "Batch")
    admission_fee = fields.Float(string = "Admission Fee")
    payment_mode = fields.Selection([('bank', 'Bank'),
        ('cash', 'Cash')], string='Pyament Type', store=True)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self.admission_id = False
        self.invoice_line_ids = False
        print('partner_id')
        if self.partner_id:
            if self.partner_id.reference:
                self.student = self.partner_id.reference
                self.product_id = self.admission_id.product_id
                self.admission_fee = self.partner_id.admission_fee
                self.l10n_in_gst_treatment = 'unregistered'

    @api.onchange('partner_id', 'admission_id')
    def onchange_admission_id(self):
        self.invoice_line_ids = False
        account = self.env['account.account'].search([('name', '=', 'Local Sales')])
        # self.invoice_line_ids.unlink()
        if self.admission_id:

            # self.invoice_line_ids.unlink()
            price_unit = 0
            for line in self.admission_id.course_ids:
                # self.invoice_line_ids = [(5, 0, 0)]
                price_unit = line.pending_fee / (1 + (line.course_id.taxes_id.amount / 100))
                if line.payment_status == '2':
                    # self.invoice_line_ids.unlink()
                    self.sudo().update({'invoice_line_ids': [(0, 0, {
                        'product_id': line.course_id.id,
                        'name': line.course_id.name,
                        'total_fee': line.pending_fee,
                        'price_unit': price_unit,
                        'account_id': account.id,
                        'currency_id': self.currency_id.id,
                        'tax_ids': [(6, 0, line.course_id.product_tmpl_id.taxes_id.ids)],
                    })]})
        if self.invoice_line_ids:
            tot = 0
            for i in self.invoice_line_ids:
                print(i.total_fee)
                i._onchange_price_subtotal()
                i._onchange_mark_recompute_taxes()
            self._recompute_dynamic_lines()
            self._recompute_tax_lines()
            self._onchange_invoice_line_ids()
            self._onchange_recompute_dynamic_lines()

    def _compute_total_amount_in_words(self, doc):
        # INR = self.env['res.currency'].search([('name', '=', 'INR')])
        for move in doc:
            if move.amount_total:
                total = move.amount_total
                y = move.currency_id.amount_to_text(total)
                return str(y)

    def action_register_payment(self):
            res = super(AccountMove, self).action_register_payment()
            for i in self:
                partner = i.partner_id
                x = self.admission_id
                for k in self.invoice_line_ids:
                    for fees in x.course_ids:
                        if fees.course_id:
                            if k.product_id == fees.course_id:
                                fees.advance_fee += k.total_fee
                            if fees.pending_fee == 0:
                                 fees.payment_status = '1'
                            else:
                                fees.payment_status = '2'

                    for j in k.product_id:
                        if j.product_tmpl_id.categ_id.name == 'admission':
                            partner.sudo().write({
                                'admission_fee': k.price_subtotal
                            })
                x.action_confirm()
            return res
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    total_fee = fields.Float(string="Total Fee")

    @api.onchange('total_fee')
    def onchange_total_fee(self):
        for move in self:
            print(move)
            if move.total_fee:
                print(move.total_fee / (1 + (move.tax_ids.amount / 100)), 'kkkkk')
                move.price_unit = move.total_fee / (1 + (move.tax_ids.amount / 100))
                move.price_subtotal = move.price_unit











