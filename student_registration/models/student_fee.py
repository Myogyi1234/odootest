from odoo import api, fields, models, tools


class StudentFee(models.Model):
    _name = 'student.fee'
    _description = 'Student Fee'

    student_id = fields.Many2one('student.registration', string='Student', required=True, ondelete='cascade')
    academic_year = fields.Char(string='Academic Year', required=True)
    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'),
        ('4', 'April'), ('5', 'May'), ('6', 'June'),
        ('7', 'July'), ('8', 'August'), ('9', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ], string='Month', required=True)
    amount = fields.Float(string='Fee Amount', required=True)
    paid_amount = fields.Float(string='Paid Amount')
    due_amount = fields.Float(string='Due Amount', compute='_compute_due', store=True)
    payment_date = fields.Date(string='Payment Date')
    state = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ], string='Payment Status', compute='_compute_due', store=True)

    @api.depends('amount', 'paid_amount')
    def _compute_due(self):
        for rec in self:
            rec.due_amount = rec.amount - rec.paid_amount
            if rec.paid_amount <= 0:
                rec.state = 'unpaid'
            elif rec.paid_amount < rec.amount:
                rec.state = 'partial'
            else:
                rec.state = 'paid'
