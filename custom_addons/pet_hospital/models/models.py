# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class PetPet(models.Model):
    _name = 'pet.pet'
    _description = 'Pet'

    code = fields.Char(
        string="Code",
        required=True,
        copy=False,
        readonly=True,
        default='New',
    )
    name = fields.Char(string="Pet Name", required=True)
    image = fields.Image(string="Image")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        store=True
    )

    owner_id = fields.Many2one(
        'res.partner',
        string="Owner"
    )

    owner_phone = fields.Char(string="Owner Phone")
    owner_address = fields.Char(string="Owner Address")

    pet_type_id = fields.Many2one('pet.type', string="Type")
    pet_breed_id = fields.Many2one('pet.breed', string="Breed")

    vaccination_ids = fields.One2many(
        'pet.vaccination',
        'pet_id',
        string="Vaccination History",
    )
    medical_history_ids = fields.One2many(
        'pet.medical.history',
        'pet_id',
        string="Medical History",
    )
    appointment_ids = fields.One2many(
        'pet.appointment',
        'pet_id',
        string="Appointments",
    )

    _sql_constraints = [
        (
            'pet_code_unique',
            'unique(code)',
            'Mã thú cưng (Code) phải là duy nhất.',
        ),
    ]

    @api.depends('dob')
    def _compute_age(self):
        for pet in self:
            if pet.dob:
                pet.age = relativedelta(fields.Date.today(), pet.dob).years
            else:
                pet.age = 0

    @api.onchange('owner_id')
    def _onchange_owner_id(self):
        if self.owner_id:
            self.owner_phone = self.owner_id.phone
            self.owner_address = self.owner_id.contact_address

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('pet.pet') or _('New')
        return super(PetPet, self).create(vals)
