from odoo import api, fields, models, tools

class Location(models.Model):
    _name = "location"
    _description = "Location details"

    locationname = fields.Char(string='Location name', required=True, help='Name of the location')
    description = fields.Text()
    customer_id = fields.Many2one('Customer')

class Ponds(models.Model):
    _name = "ponds"
    _description = "Ponds list by location"

    pondname = fields.Char('Pond name')
    location_id = fields.Many2one('location')
    log_list = fields.One2many('log', 'pond_id')

class Log(models.Model):
    _name = "log"
    _description = "log details"

    pond_id = fields.Many2one('pond')
    user_id = fields.Many2one('res.users')
    description = fields.Text('description')
    pond_list = fields.One2many('pond', 'location_id')

class Customer(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    _description = "customer list by location"

    location = fields.One2many('location', 'partner_id')