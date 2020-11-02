from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError, UserError
import re


class Device(models.Model):
    _name = "device"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [('controller_unique', 'unique(controller_id)', 'That Particular Controller is already assigned .')]

    name = fields.Char('Name')
    device_type = fields.Selection([('pondmother', 'PondMother'),
        ('shrimptalk', 'ShrimpTalk'),
        ('pondguard', 'PondGuard'),],copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='pondmother')
    controller_id = fields.Many2one('controller',string="Current Controller")
    active = fields.Boolean('Active', default=True, track_visibility=True)
    customer_id = fields.Many2one('res.partner',string="Current Customer")
    user_id = fields.Many2one('res.users')
    history = fields.One2many('device.history','device_id',string='Device History')
    controller_history = fields.One2many('controller.history', 'device_id')
    controller_ids = fields.One2many('controller', string='IDS',
                                               compute='getControllerIds')


    @api.onchange('device_type')
    def getControllerIds(self):
        print("ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooovvvvvo")
        print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooovvvvvv")
        print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        # self.controller_id = None
        products = self.sudo().env['controller'].search([('type', '=', self.device_type)])
        lis = []
        for val in products:
            lis.append(val.id)
        self.controller_ids = lis

        print(self.controller_ids)
        print(self.controller_id.type)

    # @api.model
    # def create(self, vals):
    #     # context: no_log, because subtype already handle this
    #     print("???????????????????????????????????????")
    #     controller = self.sudo().env['controller'].search([('id', '=', vals['controller_id'])])
    #     print(vals['device_type'], "----------------", controller.type)
    #     if controller.type != vals['device_type']:
    #         print("@@@@@@@@@@@@@@@@@@@@@@@222222222222222222222222222222222222")
    #         print(vals['device_type'],"-------error------",controller.type)
    #     print(vals)
    #     res = super(Device, self).create(vals)
    #     return res

    # @api.multi
    # def write(self, vals):
    #     # context: no_log, because subtype already handle this
    #     print("???????????????????????????????????????")
    #     controller = self.sudo().env['controller'].search([('id', '=', vals['controller_id'])])
    #     print(vals['device_type'], "----------------", controller.type)
    #     if controller.type != vals['device_type']:
    #         print("@@@@@@@@@@@@@@@@@@@@@@@222222222222222222222222222222222222")
    #         print(vals['device_type'], "-------error------", controller.type)
    #     print(vals)
    #     res = super(Device, self).write(vals)
    #     return res
    #
    # def write(self, vals):
    #     print("==================================================pppppppppp")
    #     print(vals)
    #     rslt = super(Device, self).write(vals)
    #     if 'device_type' in vals:
    #         # controller = self.sudo().env['controller'].search([('id', '=', vals['controller_id'])])
    #         # print(vals['device_type'], "----------------", controller.type)
    #         if self.controller_id.type != rslt.device_type:
    #             raise UserError(_('Please select controller id of type'))
    #             # print("@@@@@@@@@@@@@@@@@@@@@@@222222222222222222222222222222222222")
    #             # print(vals['device_type'], "-------error------")
    #         print(vals)
    #     return rslt


class Controller(models.Model):
    _name = "controller"
    name = fields.Char('Unique ID')
    type = fields.Selection([('pondmother', 'PondMother'),
                                    ('shrimptalk', 'ShrimpTalk'),
                                    ('pondguard', 'PondGuard'), ])
    state = fields.Selection([('available', 'Available'),
                              ('installed', 'Installed'),
                             ('returned', 'Returned'),
                              ('refurbished', 'Refurbished'),],string="Current State")
    expected_availabilty = fields.Datetime('Expected Availability')
    state_history = fields.One2many('controller.state.history', 'controller_id')

class DeviceHistory(models.Model):
    _name = "device.history"
    device_id = fields.Many2one('device','Device ID')
    customer_id = fields.Many2one('res.partner')
    date_from = fields.Datetime('Date From')
    date_to = fields.Datetime('Date To')
    comments = fields.Text('Comments')
class ControllerHistory(models.Model):
    _name="controller.history"
    device_id = fields.Many2one('device', 'Device ID')
    controller_id = fields.Many2one('controller','Controller')
    reason_for_replacement = fields.Selection([('physical_damage', 'Physical Damage'),
        ('option2', 'Option2'),
        ('option3', 'Option3'),])
    replacement_date = fields.Datetime('Replacement Date')
    customer_id = fields.Many2one('res.partner')

class DeviceImages(models.Model):
    _name = "device.image"
    history_id = fields.Many2one('device.history','history_id')

class ControllerStateHistory(models.Model):
    _name = "controller.state.history"
    name = fields.Char()
    controller_id = fields.Many2one('controller')
    state = fields.Selection([('available', 'Available'),
                              ('installed', 'Installed'),
                              ('returned', 'Returned'),
                              ('refurbished', 'Refurbished'), ], string="State")
    from_date = fields.Datetime('From Date')
    to_date = fields.Datetime('To Date')
    @api.model
    def create(self, vals):
        controller = self.sudo().env['controller'].search([('id', '=', vals['controller_id'])])
        vals['name'] = controller.name
        res = super(ControllerStateHistory, self).create(vals)
        return res


