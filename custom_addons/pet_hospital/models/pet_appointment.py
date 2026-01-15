# -*- coding: utf-8 -*-

from odoo import models, fields


class PetAppointment(models.Model):
    _name = 'pet.appointment'
    _description = 'Pet Appointment'
    _order = 'appointment_date desc, id desc'

    pet_id = fields.Many2one(
        'pet.pet',
        string="Pet",
        required=True,
        ondelete='cascade',
    )
    owner_id = fields.Many2one(
        related='pet_id.owner_id',
        comodel_name='res.partner',
        string="Owner",
        store=True,
        readonly=True,
    )
    appointment_date = fields.Datetime(
        string="Appointment Date",
        required=True,
        default=fields.Datetime.now,
    )
    reason = fields.Char(string="Reason")
    notes = fields.Text(string="Notes")
    doctor_id = fields.Many2one(
        'res.partner',
        string="Doctor",
        domain=[('is_company', '=', False)],
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        default='draft',
    )

