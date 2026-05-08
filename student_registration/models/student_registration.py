from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
import re


class StudentRegistration(models.Model):
    _name = 'student.registration'
    _description = 'Student Registration Record'
    # ── Student ID (Auto Generate) ─────────────────────────
    student_id = fields.Char(
        string='Student ID',
        readonly=True,
        copy=False,
        default='New'
    )

    name = fields.Char(string='Student Name', required=True)
    nrc_no = fields.Char(string='NRC Number')
    roll_number = fields.Char(string='Student Roll No.', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', default='male')

    father_id = fields.Many2one(
        'student.parent',
        string="Father Information",
        domain=[('relation', '=', 'father')]
    )
    mother_id = fields.Many2one(
        'student.parent',
        string="Mother Information",
        domain=[('relation', '=', 'mother')]
    )

    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', readonly=True, tracking=True)

    # ── Compute Age ────────────────────────────────────────

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.date_of_birth:
                delta = today - rec.date_of_birth
                rec.age = delta.days // 365
            else:
                rec.age = 0

    # ── Auto Generate Student ID ───────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('student_id', 'New') == 'New':
                vals['student_id'] = self.env['ir.sequence'].next_by_code(
                    'student.registration'
                ) or 'New'
        return super().create(vals_list)

    # ── Constraints ──────────────────────────────────────────

    _sql_constraints = [
        ('roll_number_unique', 'UNIQUE(roll_number)',
         'Roll Number must be unique!'),
        ('student_id_unique', 'UNIQUE(student_id)',
         'Student ID must be unique!')
    ]

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Date of Birth cannot be in the future."))

    @api.constrains('nrc_no')
    def _check_nrc_format(self):
        for record in self:
            if record.nrc_no:
                nrc_pattern = r'^([1-9][0-9]?\/[A-Za-z]{2,6}\((NAING|Eh|Pyu)\)[0-9]{6}|[၁-၉][၀-၉]?\/[က-ဩ]{2,6}\((နိုင်|ဧည့်|ပြု)\)[၀-၉]{6})$'
                if not re.match(nrc_pattern, record.nrc_no):
                    raise ValidationError(
                        "NRC ပုံစံ မှားနေသည်!"
                    )

    # ── State Actions ─────────────────────────────────────────

    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    _("Only Draft records can be confirmed. '%s' is already %s.")
                    % (rec.name, rec.state)
                )
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        for rec in self:
            if rec.state == 'cancel':
                raise UserError(
                    _("'%s' is already cancelled.") % rec.name
                )
        self.write({'state': 'cancel'})

    def action_reset_to_draft(self):
        for rec in self:
            if rec.state != 'cancel':
                raise UserError(
                    _("Only Cancelled records can be reset to Draft.")
                )
        self.write({'state': 'draft'})
