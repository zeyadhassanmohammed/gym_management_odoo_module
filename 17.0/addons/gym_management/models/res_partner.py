from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit='res.partner'

    is_vip = fields.Boolean('VIP Member')
    vip_discount = fields.Float('VIP Discount (%)', default=0.0)