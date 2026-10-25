from odoo import fields,models,api
from odoo.exceptions import ValidationError

class GymAttendance(models.Model):
    _name='gym.attendance'
    _description='gym attendance'

    member_id=fields.Many2one('gym.member', string='Member')
    class_id=fields.Many2one('gym.class', string='Class')
    check_in_datetime=fields.Datetime(string='Check In Time', default=fields.Datetime.now)
    present = fields.Boolean(string='Present', default=True)