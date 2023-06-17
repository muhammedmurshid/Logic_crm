{
    'name': 'CRM stage customisation',
    'version': '14.0.1.0.0',
    'summary': 'Additions and modifications in CRM module.',
    'sequence': 14,
    'description': """Inventory Valuation Customisation""",
    'depends': ['base', 'crm', 'stock', 'crm_lead_customisation', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/crm_stage_update_views.xml',
        'wizard/crm_assign_wizard_views.xml',
        'views/crm_stage_analysis_report_views.xml',
        'views/crm_lead_views.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
