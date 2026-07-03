from odoo import fields,models,api
class saleorder(models.Model):
    _inherit = 'sale.order'
    partner_id = fields.Many2one('res.partner',string="Customer Name")
    validity_date=fields.Date(string="Warranty Date")