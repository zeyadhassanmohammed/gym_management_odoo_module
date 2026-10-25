from odoo import fields,models,api

class GymTrainer(models.Model):
    _name='gym.trainer'
    _description='gym trainer'

    name = fields.Char('name',required=True)
    specialty = fields.Char('specialty')
    user_id = fields.Many2one('res.users', string='Login Account')
    class_ids = fields.One2many('gym.class', 'trainer_id', string='Classes')