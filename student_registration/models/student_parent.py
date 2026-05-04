import re
from odoo import fields,models,api
from odoo.exceptions import ValidationError
class StudentParent(models.Model):
    _name = 'student.parent'
    _description = 'Student Parent information'


    name = fields.Char(string='Parent Name')
    nrc_no = fields.Char(string='NRC Number')
    job_title = fields.Char(string='Job Title/Employment')
    phone_number = fields.Char(string='Phone Number')
    relation=fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian','Guardian'),
    ], string='Relationship',required=True)

    @api.constrains('nrc_no')
    def _check_nrc_format(self):
        for record in self:
            if record.nrc_no:
                # မြန်မာမှတ်ပုံတင် Format ကို စစ်ဆေးသည့် Regular Expression
                # ဥပမာ - ၁၂/မရက(နိုင်)၁၂၃၄၅၆
                nrc_pattern = r'^[0-9၀-၉]{1,2}\/[က-အ]{2,6}\((နိုင်|ဧည့်|ပြု)\)[0-9၀-၉]{6}$'

                if not re.match(nrc_pattern, record.nrc_no):
                    raise ValidationError(
                        "မှတ်ပုံတင်နံပါတ် ပုံစံမမှန်ပါ။ ဥပမာ - '၁၂/မရက(နိုင်)၁၂၃၄၅၆' ဟု ရိုက်ထည့်ပါ။"
                    )