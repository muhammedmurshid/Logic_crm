# -*- coding: utf-8 -*-
from odoo import models, fields, _,api
# from odoo.tools.misc import format_date as fd
from babel.dates import format_datetime, format_date as ddd
# from odoo.exceptions import UserError
import xlsxwriter
import datetime
from pytz import timezone
import pytz
from io import BytesIO

try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes
from odoo.exceptions import Warning


class ConversionRatioWizard(models.TransientModel):
    _name = 'conversion.ratio.wizard'

    fileout = fields.Binary('File', readonly=True)
    fileout_filename = fields.Char('Filename', readonly=True)
    from_date1 = fields.Date(string='From Date', required=True)
    to_date1 = fields.Date(string='To Date', required=True)
    telecaller_ids = fields.Many2many('res.users', string='Telecaller',readonly =True)
    lead_id = fields.Many2one('crm.lead',string='Lead')


    def action_orders(self):
        if self.from_date1 > self.to_date1:
            raise Warning(_("From Date is Greater Than To Date"))
        filter_cdtn = ''
        if self.from_date1 and self.to_date1:
            filter_cdtn += '''cl.date_deadline between '%s'  and '%s' 
                          ''' % (self.from_date1, self.to_date1)
        if self.telecaller_ids:
            if len(self.telecaller_ids) == 1:
                filter_cdtn += ''' and cl.telecaller_id = '%s'
                ''' % (self.telecaller_ids.ids[0])
            else:
                filter_cdtn += ''' and cl.telecaller_id in {}
                '''.format(tuple(self.cl.telecaller_ids.ids))
        print(filter_cdtn)
        query = ("""SELECT cl.date_deadline::timestamp::date,cl.name as student,rp.name as telecaller, cl.is_admission
                                   FROM crm_lead as cl
                                   left join res_users as rs on cl.telecaller_id = rs.id
                                   left join res_partner as rp on rs.partner_id = rp.id
                                   where rp.name is not null and %s""") % (filter_cdtn)
        self._cr.execute(query)
        move_ids = self.env.cr.dictfetchall()
        rows = []
        lead_dict = {}
        admission_dict = {}
        count = 0
        for move in move_ids:
            if move['telecaller'] in lead_dict.keys():
                lead_dict[move['telecaller']] = lead_dict[move['telecaller']] + 1
            else:
                lead_dict[move['telecaller']] = count + 1
            if move['is_admission'] == True:
                if move['telecaller'] in admission_dict.keys():
                    admission_dict[move['telecaller']] = admission_dict[move['telecaller']] + 1
                else:
                    admission_dict[move['telecaller']] = count + 1
        data = {'pros': lead_dict,
                'kit' : admission_dict,
                'keys': lead_dict.keys()
                }
        file_io = BytesIO()
        workbook = xlsxwriter.Workbook(file_io)

        self.generate_xlsx_report(workbook, data=data)

        workbook.close()
        fout = encodebytes(file_io.getvalue())
        datetime_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = 'Gst 3B Report'
        filename = '%s_%s' % (report_name, datetime_string)
        self.write({'fileout': fout, 'fileout_filename': filename})
        file_io.close()
        filename += '%2Exlsx'

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=fileout&download=true&filename=' + filename,
            # "context": {
            #     'default_class_id': self.id,
            #     'default_batch_id': self.batch_id.id,
            # }
        }


    def generate_xlsx_report(self, workbook, data=None, objs=None):
        master_head1 = workbook.add_format({'font_size': 11, 'bg_color': '#b3c6ff', 'align': 'center',
                                            'valign': 'vcenter', 'bold': True, 'border': 1, })
        master_head1.set_font_name('Times New Roman')
        master_head = workbook.add_format({'font_size': 11, 'align': 'center',
                                           'valign': 'vcenter', 'bold': True, 'border': 1, })
        master_head.set_font_name('Calibri')
        master_head_arial = workbook.add_format({'font_size': 11, 'align': 'center',
                                                 'valign': 'vcenter', 'bold': True, 'border': 1, })
        master_head_arial.set_font_name('Arial')
        b2b_head = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'font_color': 'white',
                                        'border': 1, 'bg_color': '#007acc', 'bold': True})
        b2b_head.set_font_name('Times New Roman')
        amt_head = workbook.add_format({'font_size': 11, 'align': 'right', 'font_color': 'white',
                                        'valign': 'vcenter', 'border': 1, 'bg_color': '#007acc', 'bold': True})
        amt_head.set_font_name('Times New Roman')
        center_head = workbook.add_format({'font_size': 11, 'align': 'center', 'font_color': 'white',
                                           'valign': 'vcenter', 'border': 1, 'bg_color': '#007acc', 'bold': True})
        center_head.set_font_name('Times New Roman')
        b2b_body = workbook.add_format({'font_size': 11, 'align': 'vcenter',
                                        'valign': 'vcenter', 'bg_color': '#ecc6c6', 'border': 1})
        b2b_body.set_font_name('Times New Roman')
        amt_body = workbook.add_format({'font_size': 11, 'align': 'right',
                                        'valign': 'vcenter', 'bg_color': '#ecc6c6', 'border': 1})
        amt_body.set_font_name('Times New Roman')
        center_body = workbook.add_format({'font_size': 11, 'align': 'center',
                                           'valign': 'vcenter', 'bg_color': '#ecc6c6', 'border': 1})
        center_body.set_font_name('Times New Roman')
        format3 = workbook.add_format({'font_size': 10, 'valign': 'vcenter'})
        format3.set_font_name('Times New Roman')
        center_format3 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': True})
        center_format3.set_font_name('Arial')
        total_amt = workbook.add_format({'font_size': 10, 'valign': 'vcenter', 'border': 1})
        total_amt.set_font_name('Times New Roman')
        total_no = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        total_no.set_font_name('Times New Roman')
        in_out_1_sheet = workbook.add_worksheet('in_out-')
        in_out_1_sheet.write(0, 0, 'Lead Conversion Report', center_head)
        in_out_1_sheet.write(1, 0, 'Telecaller Name', master_head)
        in_out_1_sheet.write(1, 1, 'Total Leads', master_head)
        in_out_1_sheet.write(1, 2, 'Total Admission', master_head)
        in_out_1_sheet.write(1, 3, 'Conversion Ratio', master_head)
        in_out_1_sheet.write(1, 4, 'Incentive', master_head)
        in_out_1_sheet.set_column('A:A', 24)
        in_out_1_sheet.set_column('B:B', 24)
        in_out_1_sheet.set_column('C:C', 24)
        in_out_1_sheet.set_column('D:D', 24)
        in_out_1_sheet.set_column('E:E', 24)
        row = 2
        col = 0
        conversion = 0
        incentive = 0
        for k in data['pros'].keys():
            in_out_1_sheet.write(row, col + 0, k, center_format3)
            in_out_1_sheet.write(row, col + 1, data['pros'][k], center_format3)

            if k in data['kit']:
                conversion = data['kit'][k] / data['pros'][k]*100
                if data['kit'][k] <= 20:
                    incentive =  0
                elif data['kit'][k] > 20 and data['kit'][k] <= 30:
                    incentive = 100 * data['kit'][k]
                    print(data['kit'][k])
                    print(incentive)
                elif data['kit'][k] > 30:
                    incentive = 200 * data['kit'][k]
                in_out_1_sheet.write(row, col + 2, data['kit'][k], center_format3)
                in_out_1_sheet.write(row, col + 3, conversion, center_format3)
                in_out_1_sheet.write(row, col + 4, incentive, center_format3)
            else:
                in_out_1_sheet.write(row, col + 2, 0, center_format3)
                in_out_1_sheet.write(row, col + 3, 0, center_format3)
                in_out_1_sheet.write(row, col + 4, 0, center_format3)
            row += 1
