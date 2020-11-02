# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Test',
    'version': '1.0',
    'category': 'Base',
    'sequence': 60,
    'summary': 'Some test object',
    'description': "Some test object",
    'depends': ['base','l10n_in','crm','sale_crm','account','web'],
    'data': [
        'views/enquiry_views.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'auto_install': True,
}
