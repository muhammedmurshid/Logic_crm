# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Education CRM',
    'version': '14.0.1.0.0',
    'summary': 'Additions and modifications in CRM module.',
    'author': 'Divergent Catalist ERP Solutions',
    'company': 'Divergent Catalist ERP Solutions',
    'maintainer': 'Divergent Catalist ERP Solutions',
    'sequence': 14,
    'description': """Inventory Valuation Customisation""",
    'website': 'https://www.catalisterp.com/',
    'depends': ['base', 'crm', 'stock'],
    'data': [
        'data/crm_stage.xml',
        'data/ir_cron.xml',
        'data/data.xml',
        # 'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/crm_lead_customisation_view.xml',
        # 'views/crm_stage_report.xml',
        'wizard/crm_assign_wizard.xml',
        'wizard/crm_stage_update.xml',
        # 'wizard/crm_team_wizard_views.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
