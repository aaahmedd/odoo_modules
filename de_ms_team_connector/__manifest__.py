{
    'name': 'Microsoft Teams Integration',
    'version': '14.0.0.0.0',
    'author': 'Dynexcel',
    'website': 'https://www.dynexcel.com',
    'depends': ['calendar'],
    'license': '',
    'category': 'Meetings',
    'company': 'Dynexcel',
    'summary': 'Join Microsoft Team Meetings Via Odoo',
    'description': '''
        Join Microsoft Team meetings Via Odoo
''',
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/de_company_view.xml',
        'views/meeting.xml',
        'demo/demo.xml',
        'views/de_temp_view.xml',
        # 'wizard/message_wizard.xml',
    ],
    'currency': 'USD',
    'price': 0,
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png','static/description/main_screenshot.png']
}