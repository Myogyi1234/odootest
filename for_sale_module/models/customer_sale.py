import uuid

from odoo import models, fields, api


class customersale(models.Model):
    _name = 'customer.sale'
    _description = 'Customer Sale'


_inherit = "mail.thread", "mail.activity.mixin"

# access_token = fields.Char(
#     'Security Token',
#     copy=False,
#     default=lambda self: uuid.uuid4().hex
# )

# name = fields.Char(string="Customer Name")
