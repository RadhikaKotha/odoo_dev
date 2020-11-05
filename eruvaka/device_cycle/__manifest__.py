# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'ST ResponseTracking',
    'version': '1.0',
    'category': 'Base',
    'sequence': 60,
    'summary': 'ST ResponseTracking',
    'description': "Ponds issue tracker",
    'depends': ['base','l10n_in','crm','sale_crm','account','web'],
    'data': [
        'security/security.xml',
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