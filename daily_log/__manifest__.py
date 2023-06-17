{
    "name": "daily_log",
    "summary": """Daily Log Details""",
    "category": "Crm",
    "version": "1.1.1",
    "sequence": 4,
    'description': """Attendance""",
    'depends': ['contacts', 'base'],
    'data': ['security/ir.model.access.csv',
             # 'security/log_rule.xml',
             'views/log.xml'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
