from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StudentCheckIn(models.Model):
    _name = 'student.check_in'  # XML ထဲက res_model နဲ့ တစ်ထပ်တည်း တူရပါမယ်
    _description = 'Student Check-In Records'
    _order = 'check_in_time desc'

    # Database Fields (Columns)
    name = fields.Char(string='Student Name', required=True)
    roll_no = fields.Char(string='Roll Number', required=True)
    check_in_time = fields.Datetime(
        string='Check-In Time',
        default=fields.Datetime.now,
        readonly=True
    )

    # ကျောင်းသားအမျိုးအစား (ဥပမာ- Final Year, Second Year စသဖြင့်)
    student_type = fields.Selection([
        ('cs', 'Computer Science'),
        ('ct', 'Computer Technology')
    ], string='Major', default='cs')

    # အခြေအနေပြ Field
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checked_in', 'Checked In'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    # မှတ်ချက်
    remark = fields.Text(string='Remark')

    # ခလုတ်နှိပ်ရင် Status ပြောင်းပေးမယ့် Function
    def action_confirm(self):
        for record in self:
            record.state = 'checked_in'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'