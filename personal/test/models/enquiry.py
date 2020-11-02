from odoo import api, fields, models, tools, SUPERUSER_ID, _

from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError, UserError
import re


class Enquiry(models.Model):
    _name = "enquiry"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Enquiry', index=True)
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange', track_sequence=1,
                                 index=True,
                                 help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
    active = fields.Boolean('Active', default=True, track_visibility=True)
    # team_id = fields.Many2one('crm.team', string='Sales Team', oldname='section_id',
    #                           default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(
    #                               user_id=self.env.uid),
    #                           index=True, track_visibility='onchange',
    #                           help='When sending mails, the default email address is taken from the Sales Team.')
    # user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange',
    #                           default=lambda self: self.env.user)

    # @api.model
    # def return_self(self):
    #     return self