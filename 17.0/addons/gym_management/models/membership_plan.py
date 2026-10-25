from odoo import fields,models,api
from odoo.exceptions import ValidationError

class MembershipPlan(models.Model):
    _name='membership.plan'
    _description='Membership Plan'

    name=fields.Char()
    duration_months=fields.Integer(string="Duration (Months)")
    price=fields.Float()
    class_credits=fields.Integer(string="Class Credits")
    gym_member_ids = fields.One2many('gym.member', 'membership_plan_id', string="Gym Members")
    payment_ids = fields.One2many('gym.payment', 'plan_id', string='payment')


    @api.constrains('name')
    def check_name(self):
        for rec in self:
            if not self.name:
                raise ValidationError("The Membership Plan name cannot be empty.")

    _sql_constraints =[
        ('unique_name','UNIQUE(name)','this name already exists')
    ]