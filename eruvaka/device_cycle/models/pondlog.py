from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class Location(models.Model):
    _name = "location"
    _description = "Location details"

    name = fields.Char('Location name', required=True)

    @api.model
    def create(self, vals):
        locations = self.sudo().env['location'].search([])
        for location in locations:
            if location.name == vals['name']:
                raise UserError(
                      _('Location already exists'))
        location_object = super(Location, self).create(vals)
        return location_object

    def write(self, vals):
        locations = self.sudo().env['location'].search([])
        for location in locations:
            if location.name == vals['name']:
                raise UserError(
                      _('Location already exists'))
        location_object = super(Location, self).write(vals)
        return location_object


class Device(models.Model):
    _name = "device"
    _description = "device details"
    _rec_name = "device_id"

    device_id = fields.Char('Device ID')
    device_type = fields.Selection([('shrimp talk', 'Shrimp Talk'),
        ('pond mother', 'Pond Mother'), ('pond guard', 'Pond Guard'), ],
        copy=False, index=True, track_visibility='onchange', track_sequence=3, string='Device Type')
    partner_id = fields.Many2one('res.partner', string='Current Location', invisible=True)
    state = fields.Selection([('issued from Factory', 'Issued from Factory'),
                              ('installed at Customer Farm', 'Installed at Customer Farm'),
                              ('idle at Customer Farm', 'Idle at Customer Farm'),
                              ('returned from Customer Farm', 'Returned from Customer Farm'),
                              ('waiting for Service / Repair', 'Waiting for Service / Repair'),
                              ('refurbished (Tanguturu Warehouse)', 'Refurbished (Tanguturu Warehouse)'),
                              ('refurbished (Gudivada Warehouse)', 'Refurbished (Gudivada Warehouse)'), ],
                             string="State")
    comments = fields.Text('Comments')
    from_date = fields.Date('From Date', default=fields.Datetime.now())
    devicecycle_history = fields.One2many('devicecycle.history', 'devicecycle_id', string="Device History",
                                          readonly="True")

    pond_id = fields.Many2one('pond', string="Pond ID")

    @api.model
    def create(self, vals):
        devices = self.sudo().env['device'].search([])
        for device in devices:
            if device.device_id == vals['device_id']:
                raise UserError(
                    _('Device ID already exists'))
        device_object = super(Device, self).create(vals)
        return device_object

    def write(self, vals):
        if 'from_date' not in vals:
            to_date = None
        else:
            to_date = vals['from_date']
        for device in self:
            if 'from_date' not in device:
                from_date = None
            else:
                from_date = device.from_date
            device_prev = {
                'device_type': device.device_type,
                'device_id': device.device_id,
                'partner_id': device.partner_id.id,
                'state': device.state,
                'comments': device.comments,
                'from_date': from_date,
                'to_date': to_date,
                'devicecycle_id': device.id,
            }
            # Creating old record into devicecycle history table
            device.sudo().env['devicecycle.history'].create(device_prev)

        device_object = super(Device, self).write(vals)
        return device_object

# class Devicecycle(models.Model):
#     _name = "devicecycle"
#     _description = "device cycle details"
#     _rec_name = "device_id"
#
#     device_type = fields.Selection([('shrimp talk', 'Shrimp Talk'),
#                                     ('pond mother', 'Pond Mother'), ('pond guard', 'Pond Guard'), ],
#                                    copy=False, index=True, track_visibility='onchange', track_sequence=3,
#                                    string='Device Type')
#     device_id = fields.Char('Device ID')
#     partner_id = fields.Many2one('res.partner', string='Current Location', invisible=True)
#     state = fields.Selection([('available', 'Available'),
#                               ('installed', 'Installed'),
#                               ('returned', 'Returned'),
#                               ('refurbished', 'Refurbished'), ], string="Current State")
#     comments = fields.Text('Comments')
#     from_date = fields.Datetime('From Date', readonly="True", default=fields.Datetime.now())
#     to_date = fields.Datetime('To Date')
#     devicecycle_history = fields.One2many('devicecycle.history', 'devicecycle_id', string="Device History",
#                                       readonly="True")
#
#     @api.model
#     def create(self, vals):
#         devices = self.sudo().env['devicecycle'].search([])
#         for device in devices:
#             if device.device_id == vals['device_id']:
#                 raise UserError(
#                     _('Device ID already exists'))
#         devicecycle_object = super(Devicecycle, self).create(vals)
#         return devicecycle_object
#
#     def write(self, vals):
#         devicecycle_prev = {
#             'device_type': self.device_type,
#             'device_id': self.device_id,
#             'partner_id': self.partner_id.id,
#             'state': self.state,
#             'comments': self.comments,
#             'from_date': self.from_date,
#             'to_date': fields.Datetime.now(),
#             'devicecycle_id': self.id,
#         }
#
#         # Creating old record into devicecycle history table
#         self.sudo().env['devicecycle.history'].create(devicecycle_prev)
#
#         devicecycle_object = super(Devicecycle, self).write(vals)
#         return devicecycle_object

class DevicecycleHistory(models.Model):
    _name = "devicecycle.history"
    _description = "device history details"

    device_type = fields.Selection([('shrimp talk', 'Shrimp Talk'),
                                    ('pond mother', 'Pond Mother'), ('pond guard', 'Pond Guard'), ],
                                   copy=False, index=True, track_visibility='onchange', track_sequence=3,
                                   string='Device Type')
    device_id = fields.Char('Device ID')
    partner_id = fields.Many2one('res.partner', string='Location', invisible=True)
    state = fields.Selection([('issued from Factory', 'Issued from Factory'),
                              ('installed at Customer Farm', 'Installed at Customer Farm'),
                              ('idle at Customer Farm', 'Idle at Customer Farm'),
                              ('returned from Customer Farm', 'Returned from Customer Farm'),
                              ('waiting for Service / Repair', 'Waiting for Service / Repair'),
                              ('refurbished (Tanguturu Warehouse)', 'Refurbished (Tanguturu Warehouse)'),
                              ('refurbished (Gudivada Warehouse)', 'Refurbished (Gudivada Warehouse)'), ],
                                string="State")
    comments = fields.Text('Comments')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    no_of_days = fields.Char('No Of Days', compute="_getnumberofdays")
    devicecycle_id = fields.Many2one('device')

    def _getnumberofdays(self):
        for device in self:
            if not device.to_date:
                device.no_of_days = 0
            if not device.from_date:
                device.no_of_days = 0
            else:
                device.no_of_days = str(int((device.to_date-device.from_date).days))

class Pond(models.Model):
    _name = "pond"
    _description = "Pond details"

    location_id = fields.Many2one('location', required=True)
    name = fields.Char('Pond name', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', invisible=True)
    pondmother_count = fields.Integer('PondMother Count')
    shrimptack_count = fields.Integer('ShrimpTalk Count')
    pondguard_count = fields.Integer('PondGuard Count')
    device_pondmother = fields.Many2many('device', 'device_pondmother_rel', 'pond_id', 'device_id',
                                         string="PondMother IDs")
    device_shrimp = fields.Many2many('device', 'device_shrimp_rel', 'pond_id', 'device_id', string="ShrimpTalk IDs")
    device_pondguard = fields.Many2many('device', 'device_pondguard_rel', 'pond_id', 'device_id',
                                        string="PondGuard IDs")

    device_ids = fields.One2many('device', 'pond_id', 'Device IDs')

    pondlog_by_pond = fields.One2many('pondlog', compute='_getPondlogByPond', string='Pond logs')

    @api.constrains('device_pondguard', 'device_shrimp', 'device_pondmother')
    def updatedeviceids(self):
        devices = []
        pg = self.mapped('device_pondguard')
        pm = self.mapped('device_pondmother')
        ps = self.mapped('device_shrimp')
        # getting all the devices attached to the pond and appending to the empty list
        for pndg in pg:
            devices.append(pndg.id)
        for pndm in pm:
            devices.append(pndm.id)
        for pnds in ps:
            devices.append(pnds.id)

        # updating all the devices rows with pond_id
        self.write({
            'device_ids': [(6, 0, devices)]
        })

    @api.model
    def create(self, vals):
        pond_object = super(Pond, self).create(vals)
        return pond_object

    def write(self, vals):
        pond_object = super(Pond, self).write(vals)
        return pond_object

    @api.onchange("id")
    def _getPondlogByPond(self):
        for pond in self:
            if not pond.id:
                self.pondlog_by_pond = False
            else:
                logs = self.sudo().env['pondlog'].search([('pond_ids', '=', pond.id)])
                if not any(logs):
                    self.pondlog_by_pond = False
                else:
                    pondlogs_bypond = []
                    a = 0
                    for log in logs:
                        pondlogs_bypond.append(log.id)
                    self.pondlog_by_pond = pondlogs_bypond
    @api.model
    def _getCustomerId(self):
        x = self.env['res.partner'].search(['id', '=', self.active_ids])
        self.partner_id = x.id

class MultipleImages(models.Model):
    _name = "multiple.image"
    _description = "multiple images"

    mul_image = fields.Binary('Selected Images', max_width=30,
                               max_height=30)
    image_id = fields.Many2one('pondlog')
    image_history_id = fields.Many2one('pondlog.history')

class Label(models.Model):
    _name = "label"
    _description = "label details"

    name = fields.Char('Label name')

class IssueType(models.Model):
    _name = "issue.type"
    _description = "issue details"

    name = fields.Char('Issue Type')

class Pondlog(models.Model):
    _name = "pondlog"
    _description = "pond log details"

    location_id = fields.Many2one('location', required=True)
    pond_ids = fields.Many2many('pond', string="Ponds", required=True)
    device_ids = fields.Many2many('device', string="Device IDs")
    issue_type = fields.Many2one('issue.type', string="Issue Type", required='True')
    label_issue = fields.Many2one('label', string="Label")
    description = fields.Text('Description', required='True')
    description_file = fields.Binary('Description File')
    description_filename = fields.Char('Filename')
    user_id = fields.Many2one('res.users', string='Assigned to', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    resolution_analysis = fields.Text('Resolution/Analysis')
    ticket_status = fields.Selection([('open', 'Open'),
        ('closed', 'Closed'),],copy=False, index=True, track_visibility='onchange',
        track_sequence=2, default='open')
    priority = fields.Selection([('high', 'High'),
                                 ('medium', 'Medium'), ('low', 'Low'), ], copy=False, index=True,
                                 track_visibility='onchange', track_sequence=3)
    locations = fields.One2many('location', string='Locations', compute='_getlocationsbycustid')
    pondlog_history = fields.One2many('pondlog.history', 'pondlog_id', string="Reassignment History", readonly="True")
    mul_image = fields.One2many('multiple.image', 'image_id', auto_join=True)
    pondnames = fields.Text(compute='_getpondanmes')

    @api.onchange("partner_id")
    def _clearLocationData(self):
        self.location_id = None
        self.pond_ids = None

    @api.model
    def _getpondanmes(self):
        for pndlog in self:
            if not pndlog.pond_ids:
                pndlog.pond_ids = False
            else:
                pndnames = []
                for pnd in pndlog.pond_ids:
                    pndnames.append(pnd.name)
                pndlog.pondnames = pndnames

    @api.onchange("partner_id")
    def _getlocationsbycustid(self):
        if not self.partner_id.id:
            self.locations = False
        else:
            ponds = self.sudo().env['pond'].search([('partner_id', '=', self.partner_id.id)])
            if not any(ponds):
                self.locations = False
            else:
                distinct_locations = []
                for pond in ponds:
                    if pond.location_id.id not in distinct_locations:
                        distinct_locations.append(pond.location_id.id)
                self.locations = distinct_locations

    @api.model
    def create(self, vals):
        ponds = self.sudo().env['pond'].search([('id', 'in', vals['pond_ids'][0][2])])
        pndnames = []
        for pond in ponds:
            pndnames.append(pond.name)

        pondlog_object = super(Pondlog, self).create(vals)
        model_id = pondlog_object.id
        self.send_mail(vals['user_id'], vals['partner_id'], vals['issue_type'], pndnames, vals['location_id'],
                       vals['description'], model_id)
        return pondlog_object

    def write(self, vals):
        pondlog_prev = {
            'location_id': self.location_id.id,
            'pond_ids': self.pond_ids,
            'device_ids': self.device_ids,
            'issue_type': self.issue_type.id,
            'label_issue': self.label_issue.id,
            'description': self.description,
            'description_file': self.description_file,
            'description_filename': self.description_filename,
            'user_id': self.user_id.id,
            'partner_id': self.partner_id.id,
            'resolution_analysis': self.resolution_analysis,
            'ticket_status': self.ticket_status,
            'priority': self.priority,
            'pondlog_id': self.id,
            'mul_image': self.mul_image,
        }

        # Creating old record into pondlog history table
        self.sudo().env['pondlog.history'].create(pondlog_prev)

        if 'pondlog_id' not in vals:
            model_id = self.id
        else:
            model_id = vals['pondlog_id']

        if 'user_id' not in vals:
            user = self.user_id.id
        else:
            user = vals['user_id']

        if 'partner_id' not in vals:
            custmr = self.partner_id.id
        else:
            custmr = vals['partner_id']

        if 'description' not in vals:
            description = self.description
        else:
            description = vals['description']

        if 'issue_type' not in vals:
            issue_type = self.issue_type.id
        else:
            issue_type = vals['issue_type']

        if 'pondnames' not in vals:
            pndnames = self.pondnames
        else:
            pndnames = vals['pondnames']

        if 'location_id' not in vals:
            location = self.location_id.id
        else:
            location = vals['location_id']

        self.send_mail(user, custmr, issue_type, pndnames, location, description, model_id)

        pondlog_object = super(Pondlog, self).write(vals)
        return pondlog_object

    def send_mail(self, assigned, custmr, issue_type, pndnames, location, description, model_id):
        pndnames = str(pndnames)
        user = self.sudo().env['res.users'].search([('id', '=', assigned)])
        customer = self.sudo().env['res.partner'].search([('id', '=', custmr)])
        location = self.sudo().env['location'].search([('id', '=', location)])
        issue = self.sudo().env['issue.type'].search([('id', '=', issue_type)])
        model_id = str(model_id)
        template = self.env.ref('device_cycle.mail_template_daily_observation_users')
        template.write({
            'subject': customer.name + ': "' + issue.name + ' Issue"',
            'body_html': '<b>Dear ' + user.name + ', </b><br/><br/>'
                         'There is an issue logged for customer "' + customer.name +
                         '" in the ponds ' + pndnames + ' at location "' + location.name +
                         '". The issue is ' + '"' + description + '" and needs your attention.<br/><br/>'
                         'Please click here to go to the page: '
                         u'<a href="http://52.66.211.244:8069/web#id=' + model_id +
                         u'&action=343&model=pondlog&view_type=form&cids=1&menu_id=245">'
                         'ST Response Tracking</a><br/><br/>'
                         'Have a nice day!<br/><b>Eruvaka Team</b>',
        })
        template.send_mail(user.id, force_send=True)

class PondlogHistory(models.Model):
    _name = "pondlog.history"
    _description = "pond log history"

    location_id = fields.Many2one('location', required=True)
    pond_ids = fields.Many2many('pond', string="Ponds")
    device_ids = fields.Many2many('device', string="Device IDs")
    issue_type = fields.Many2one('issue.type', string="Issue Type")
    label_issue = fields.Many2one('label', string="Label")
    description = fields.Text('Description')
    description_file = fields.Binary('Description File')
    description_filename = fields.Char('Filename')
    user_id = fields.Many2one('res.users', string='Assigned to', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    resolution_analysis = fields.Text('Resolution/Analysis')
    ticket_status = fields.Selection([('open', 'Open'),
                                      ('closed', 'Closed'), ], copy=False, index=True, track_visibility='onchange',
                                     track_sequence=2, default='open')
    priority = fields.Selection([('high', 'High'),
                                 ('medium', 'Medium'), ('low', 'Low'), ], copy=False, index=True,
                                track_visibility='onchange', track_sequence=3)
    locations = fields.One2many('location', string='Locations', compute='_getlocationsbycustid')
    pondlog_id = fields.Many2one('pondlog')
    mul_image = fields.One2many('multiple.image', 'image_history_id')

    @api.onchange("partner_id")
    def _clearLocationData(self):
        self.location_id = None
        self.pond_ids = None

    @api.onchange("partner_id")
    def _getlocationsbycustid(self):
        if not self.partner_id.id:
            self.locations = False
        else:
            ponds = self.sudo().env['pond'].search([('partner_id', '=', self.partner_id.id)])
            if not any(ponds):
                self.locations = False
            else:
                distinct_locations = []
                for pond in ponds:
                    if pond.location_id.id not in distinct_locations:
                        distinct_locations.append(pond.location_id.id)
                self.locations = distinct_locations

class Customer(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    number_of_ponds = fields.Integer('Number of ponds', compute="_getPonds")
    pondmother_count = fields.Integer('PondMother Count', compute="_getdevicescount")
    shrimptack_count = fields.Integer('ShrimpTalk Count', compute="_getdevicescount")
    pondguard_count = fields.Integer('PondGuard Count', compute="_getdevicescount")
    customer_id = fields.Char('Customer ID')
    pondlog_ids = fields.One2many('pondlog', 'partner_id', string="Daily logs", copy=True,
                               auto_join=True)
    pond_ids = fields.One2many('pond', 'partner_id', string="Ponds", copy=True,
                                 auto_join=True)

    def _getPonds(self):
        for customer in self:
            no_of_ponds = 0
            for x in customer.pond_ids:
                no_of_ponds += 1
            customer.number_of_ponds = no_of_ponds

    @api.onchange("pond_ids")
    def _getdevicescount(self):
        for custmr in self:
            pondguardcount = len(custmr.pond_ids.mapped('device_pondguard'))
            shrimptalkcount = len(custmr.pond_ids.mapped('device_shrimp'))
            pondmothercount = len(custmr.pond_ids.mapped('device_pondmother'))

            custmr.pondmother_count = pondmothercount
            custmr.shrimptack_count = shrimptalkcount
            custmr.pondguard_count = pondguardcount




