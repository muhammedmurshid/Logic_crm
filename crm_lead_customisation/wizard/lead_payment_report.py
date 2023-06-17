# -*- coding: utf-8 -*-

from odoo import models, fields
# from odoo.exceptions import UserError


class LeadPaymentReport(models.TransientModel):
    _name = 'lead.payment.report'
    _description = 'Sales Executive Report'

    date_from = fields.Date(string="Date From", help='Select start date here')
    date_to = fields.Date(string="Date To", help='Select end date here')
    #
    # access_lead_payment_report_admin, lead_payment_report_admin, model_lead_payment_report, base_ims.group_ims_admin, 1, 1, 1, 1
    # access_lead_payment_report_manager, lead_payment_report_manager, model_lead_payment_report, base_ims.group_ims_manager, 1, 1, 1, 1
    # access_lead_payment_report_user, lead_payment_report_user, model_lead_payment_report, base_ims.group_ims_user, 1, 1, 1, 1



    def print_lead_xls(self):
        data = {
            'doc_ids': self.ids,
            'model': self._name,
            'start_date': self.date_from,
            'end_date': self.date_to,

        }
        return self.env.ref('crm_ims.report_sales_executive_xlsx_report').report_action(self, [], data)
