# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Device Cycle',
    'version': '1.0',
    'category': 'Base',
    'sequence': 60,
    'summary': 'ST ResponseTracking',
    'description': "Ponds issue tracker",
    'depends': ['base', 'l10n_in', 'crm', 'sale_crm', 'account', 'web', 'board'],
    'data': [
        'security/security.xml',
        'data/sequence.xml',
        'views/location_views.xml',
        'views/pond_views.xml',
        'views/pondlogs_views.xml',
        'views/customer_views.xml',
        'views/devicecycle_views.xml',
        'views/farmactivities_views.xml',
        'views/servicerequest_views.xml',
        'views/dashboard_views.xml',
        'templates/mail_template.xml',
        # 'reports/issue_analysis_views.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'auto_install': True,
}