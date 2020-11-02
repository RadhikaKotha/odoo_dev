from odoo import api, fields, models, tools

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'openacademy courses'

    name = fields.Char(string = 'Title', required=True, help='Name of the course')
    description = fields.Text()