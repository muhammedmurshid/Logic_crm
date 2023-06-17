from . import addmission
from . import batchmaster
from . import partner
from . import crm_logic
from . import class_master
from . import due
from . import payment_notes
from . import inherit_field


# -*- coding: utf-8 -*-
from odoo import api, fields, models, _



class CreateDueWizard(models.TransientModel):
    _name = "create.due.wizard"
    _description = "Create Due wizard"

    from_date= fields.Date(string='From Date', required=True)
    end_date= fields.Date(string='End Date')
    student = fields.Many2many('res.partner', string="Student")
    student_id = fields.Char(related='student.reference', string="Student ID")


    def action_create_due(self):
        # user = self.env.user.id
        self.env.cr.execute(("""DELETE FROM due_master"""))
        date_from = self.from_date.strftime('%Y-%m-%d 00:00:00')
        date_to = self.end_date.strftime('%Y-%m-%d 23:59:59')
        company_id = self.env.company.id
        print(company_id)
        if self.from_date > self.end_date:
            raise Warning(_("From Date is Greater Than To Date"))
        filter_cdtn = ''' and cl.date between '%s' AND '%s'
                                                  ''' % (self.from_date, self.end_date)

        query = ("""select cl.id,
        rp.name as partner,cl.date as due_date,ra.name as ad_no,pt.name as course
                   from course_lines as cl
                   left join res_admission as ra on cl.res_id = ra.id
                   left join res_partner as rp on ra.partner_id = rp.id
                   left join product_product as pp on cl.course_id = pp.id
                   left join product_template as pt on pp.product_tmpl_id = pt.id
                   where cl.payment_status = '2'  and ra.company_id = %s
        %s """%(company_id,filter_cdtn))
        self._cr.execute(query)
        move_ids = self.env.cr.dictfetchall()
        print(move_ids)
        for i in move_ids:
            x = self.env['course.lines'].sudo().search([('id', '=', i['id'])])
            # self.env['due.master'].search([]).unlink()
            if x.date:
                i['pending_fee'] = x.pending_fee
                due = self.env['due.master'].sudo().create({
                    'due_date' : i['due_date'],
                    'admission_number' : i['ad_no'],
                    'partner': i['partner'],
                    'course': i['course'],
                    'pending_fee': i['pending_fee']

                })
        view = self.env.ref('admission.due_master_tree')
        print(view)
        return {
            'name': 'Due Report',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'due.master',
            'views': [(view.id, 'tree')],
            'view_id': view.id,
        }

