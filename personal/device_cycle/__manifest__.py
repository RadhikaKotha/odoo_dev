# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Device Cycle',
    'version': '1.0',
    'category': 'Base',
    'sequence': 60,
    'summary': 'Device Cycle',
    'description': "Some test object",
    'depends': ['base','l10n_in','crm','sale_crm','account','web'],
    'data': [
        'security/security.xml',
        'views/device_views.xml',
        'views/car_views.xml',
        'views/controller_views.xml',
'views/controller_state_history.xml',
        'views/controller_history_views.xml',
        'views/device_history_views.xml',
        'views/location_views.xml',
        'views/pond_views.xml',
        'views/pondlogs_views.xml',
        'views/customer_views.xml',
        'templates/mail_template.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'auto_install': True,
}