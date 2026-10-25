from odoo import fields,models,api


class GymPayment(models.Model):
    _name='gym.payment'
    _description= 'gym payment'

    member_id = fields.Many2one('gym.member', string='Gym Member',required=True)
    plan_id = fields.Many2one('membership.plan', string='Plan ID')
    amount = fields.Float(related='plan_id.price', string='Amount')
    payment_date = fields.Date(string='Payment Date')
    method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('transfer', 'Transfer'),
    ], string='Method')