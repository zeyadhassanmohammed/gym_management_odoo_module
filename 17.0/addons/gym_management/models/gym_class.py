from odoo import fields,models,api


class GymClass(models.Model):
    _name='gym.class'
    _description='gym class'

    name=fields.Char(string='Class Name',required=True)
    trainer_id = fields.Many2one('gym.trainer', string='Trainer')
    room = fields.Char('Room')
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')
    capacity = fields.Integer('Capacity')
    member_ids = fields.Many2many('gym.member', string='Members')    


    # On gym.class
    def action_take_attendance(self):
        self.ensure_one()
        lines = [(0, 0, {'member_id': m.id, 'present': False}) for m in self.member_ids]
        wizard = self.env['gym.attendance.wizard'].create({
            'class_id': self.id,
            'line_ids': lines,
        })
        return {
            'name': 'Take Attendance',
            'type': 'ir.actions.act_window',
            'res_model': 'gym.attendance.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
        }