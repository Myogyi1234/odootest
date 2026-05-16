# import re
# from odoo import fields,models,api
# from odoo.exceptions import ValidationError
# class StudentParent(models.Model):
#     _name = 'student.parent'
#     _description = 'Student Parent information'
#
#
#     name = fields.Char(string='Parent Name')
#     nrc_no = fields.Char(string='NRC Number')
#     job_title = fields.Char(string='Job Title/Employment')
#     phone_number = fields.Char(string='Phone Number')
#     relation=fields.Selection([
#         ('father', 'Father'),
#         ('mother', 'Mother'),
#         ('guardian','Guardian'),
#     ], string='Relationship',required=True)
#
#     @api.constrains('nrc_no')
#     def _check_nrc_format(self):
#         for record in self:
#             if record.nrc_no:
#                 # မြန်မာမှတ်ပုံတင် Format ကို စစ်ဆေးသည့် Regular Expression
#                 # ဥပမာ - ၁၂/မရက(နိုင်)၁၂၃၄၅၆
#                 nrc_pattern = r'^[0-9၀-၉]{1,2}\/[က-အ]{2,6}\((နိုင်|ဧည့်|ပြု)\)[0-9၀-၉]{6}$'
#
#                 if not re.match(nrc_pattern, record.nrc_no):
#                     raise ValidationError(
#                         "မှတ်ပုံတင်နံပါတ် ပုံစံမမှန်ပါ။ ဥပမာ - '၁၂/မရက(နိုင်)၁၂၃၄၅၆' ဟု ရိုက်ထည့်ပါ။"
#                     )

import re
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class StudentParent(models.Model):
    _name = 'student.parent'
    _description = 'Student Parent information'

    # ── အခြေခံ အချက်အလက် ──────────────────────────────────
    name = fields.Char(string='Parent Name', required=True)
    nrc_no = fields.Char(string='NRC Number')
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)


    # ── အလုပ်အကိုင် အချက်အလက် ─────────────────────────────
    job_title = fields.Char(string='Job Title / Employment')
    monthly_income = fields.Float(string='Monthly Income')
    workplace = fields.Char(string='Workplace')

    # ── ဆက်သွယ်ရေး အချက်အလက် ──────────────────────────────
    phone_number = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    address = fields.Char(string='Address')

    # ── ဆက်နွယ်မှု ────────────────────────────────────────
    relation = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ], string='Relationship', required=True)

    # ── ကျောင်းသားများ (One2many) ───────────────────────────
    student_ids = fields.One2many(
        'student.registration',
        compute='_compute_student_ids',
        string='Students'
    )
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_student_ids'
    )

    # ── Compute Methods ────────────────────────────────────

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.date_of_birth:
                delta = today - rec.date_of_birth
                rec.age = delta.days // 365
            else:
                rec.age = 0

    def _compute_student_ids(self):
        for rec in self:
            fathers = self.env['student.registration'].search(
                [('father_id', '=', rec.id)]
            )
            mothers = self.env['student.registration'].search(
                [('mother_id', '=', rec.id)]
            )
            all_students = fathers | mothers
            rec.student_ids = all_students
            rec.student_count = len(all_students)

    # ── Smart Button ───────────────────────────────────────

    def action_view_students(self):
        self.ensure_one()
        fathers = self.env['student.registration'].search(
            [('father_id', '=', self.id)]
        )
        mothers = self.env['student.registration'].search(
            [('mother_id', '=', self.id)]
        )
        all_students = fathers | mothers
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'student.registration',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', all_students.ids)],
        }

    # ── Constraints ────────────────────────────────────────

    @api.constrains('nrc_no')
    def _check_nrc_format(self):
        for record in self:
            if record.nrc_no:
                nrc_pattern = r'^([1-9][0-9]?\/[A-Za-z]{2,6}\((NAING|Eh|Pyu)\)[0-9]{6}|[၁-၉][၀-၉]?\/[က-ဩ]{2,6}\((နိုင်|ဧည့်|ပြု)\)[၀-၉]{6})$'
                if not re.match(nrc_pattern, record.nrc_no):
                    raise ValidationError(
                        "NRC ပုံစံ မှားနေသည်!"
                    )

    @api.constrains('phone_number')
    def _check_phone_number(self):
        for rec in self:
            if rec.phone_number:
                phone_pattern = r'^(\+?၉၅|0)?[0-9၀-၉]{7,11}$'
                if not re.match(phone_pattern, rec.phone_number):
                    raise ValidationError(
                        "ဖုန်းနံပါတ် ပုံစံမမှန်ပါ။ ဥပမာ - 09123456789"
                    )

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError("မွေးသက္ကရာဇ် နောင်ကာလ ဖြစ်မနေနိုင်ပါ။")

    # ── SQL Constraints ────────────────────────────────────

    _sql_constraints = [
        ('nrc_no_unique', 'UNIQUE(nrc_no)',
         'ဤမှတ်ပုံတင်နံပါတ် ရှိပြီးသားဖြစ်သည်။'),
    ]