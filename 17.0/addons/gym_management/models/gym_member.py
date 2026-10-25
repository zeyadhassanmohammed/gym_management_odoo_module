import re
from datetime import date

from odoo.exceptions import ValidationError
from odoo import fields,models,api
from dateutil.relativedelta import relativedelta

class GymMember(models.Model):
    _name='gym.member'
    _description='gym member'

    ref=fields.Char(default="new",readonly=True)
    name=fields.Char()
    phone=fields.Char()
    email=fields.Char()
    birth_date=fields.Date()
    image=fields.Image(string="Image", max_width=1920, max_height=1920)
    join_date=fields.Date()
    active=fields.Boolean(default=True)
    state=fields.Selection([('active','Active'),('expired','Expired'),('frozen','Frozen')],default='active')
    membership_plan_id=fields.Many2one('membership.plan', string="Membership Plan")
    class_ids = fields.Many2many('gym.class', string='class')
    payment_ids = fields.One2many('gym.payment', 'member_id', string='payment')
    membership_end_date=fields.Date(compute='_compute_membership_end_date') #computed field
    days_remaining = fields.Integer(compute='_compute_days_remaining')
    remaining_credits = fields.Integer(compute='check_remaining_credits', string='Remaining Credits') #computed field
    attendance_ids = fields.One2many('gym.attendance', 'member_id', string='Attendance Records')
    plan_price = fields.Float(related='membership_plan_id.price', string='Plan Price') #=> related field to display the price of the selected membership plan

    @api.constrains('email')
    def __check_email_format__(self):
        for rec in self:
            if rec.email:
                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

                if not re.match(email_regex,rec.email):
                    raise ValidationError('Invalid Email Format! Please enter a valid email address (e.g., name@gmail.com).')

    @api.depends('join_date','membership_plan_id.duration_months')
    def _compute_membership_end_date(self):
        for rec in self:
            if rec.join_date and rec.membership_plan_id.duration_months:
                rec.membership_end_date= rec.join_date + relativedelta(months= rec.membership_plan_id.duration_months)
            else:
                rec.membership_end_date = False


    @api.depends('membership_end_date')
    def _compute_days_remaining(self):
        for rec in self: 
            if rec.membership_end_date:
                if rec.membership_end_date>=date.today():
                    rec.days_remaining = (rec.membership_end_date - date.today()).days

                else:
                    rec.days_remaining = 0

            else:
                rec.days_remaining = 0

    def action_active(self):
        for rec in self:
            rec.state='active'

    def action_expired(self):
        for rec in self:
            rec.state='expired'

    def action_frozen(self):
        for rec in self:
            rec.state='frozen'

    @api.constrains('birth_date')
    def check_birth_date(self):
        for rec in self:
            if rec.birth_date:
                age = relativedelta(date.today(),rec.birth_date).years
                if age < 16:
                    raise ValidationError("The member must be at least 16 years old.")

    _sql_constraints =[
        ('unique_email','UNIQUE(email)','this email already exists')
    ]

    @api.depends('membership_plan_id.class_credits','attendance_ids')
    def check_remaining_credits(self):
        for rec in self:
            if rec.membership_plan_id:
                days_attended = len(rec.attendance_ids)
                plan_credits = rec.membership_plan_id.class_credits
                remaining_credits = plan_credits - days_attended
                rec.remaining_credits = remaining_credits
            else:
                rec.remaining_credits = 0
                




    @api.model
    def _cron_update_expired_memberships(self):
        expired_members=self.search([('active','=',True),('membership_end_date','<',date.today())])


        if expired_members:
            expired_members.write({'state':'expired'})



    @api.model_create_multi
    def create(self,vals):
        member_record=super().create(vals)
        print("member record=====>",member_record)
        if member_record.ref=="new":
            member_record.ref= self.env["ir.sequence"].next_by_code("seq_gym_member")

        return member_record