from odoo import fields, models, api
class MembershipPlan(models.Model):
    _inherit = 'membership.plan'
    loyalty_discount = fields.Float('Loyalty Discount')