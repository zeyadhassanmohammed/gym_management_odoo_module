from odoo import fields, models

class GymAttendanceWizard(models.TransientModel):
    _name = 'gym.attendance.wizard'
    _description = 'Take Attendance Wizard'

    class_id = fields.Many2one('gym.class', string='Class', required=True)
    line_ids = fields.One2many('gym.attendance.wizard.line', 'wizard_id', string='Members')

    def action_confirm_attendance(self):
        for line in self.line_ids:
            if line.present:
                self.env['gym.attendance'].create({
                    'member_id': line.member_id.id,
                    'class_id': self.class_id.id,
                    'check_in_datetime': fields.Datetime.now(),
                    'present': True,
                })


class GymAttendanceWizardLine(models.TransientModel):
    _name = 'gym.attendance.wizard.line'
    _description = 'Attendance Wizard Line'

    wizard_id = fields.Many2one('gym.attendance.wizard')
    member_id = fields.Many2one('gym.member', string='Member')
    present = fields.Boolean(string='Present', default=False)