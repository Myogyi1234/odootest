from odoo import models, fields, api
from odoo.release import description


class StudentRegistration(models.Model):
    _name = 'student.registration'
    _description = 'Student Registration Record'

    name = fields.Char(string='Student Name', required=True)
    roll_number = fields.Char(string='Student Roll No.', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ],string='Gender',default='male')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancelled'),

    ], string='Status',default='draft',readonly=True)

    def action_confirm(self):
        self.state = 'confirmed'