# -*- coding: utf-8 -*-

from odoo import models, fields


class PetVaccination(models.Model):
    _name = 'pet.vaccination'
    _description = 'Pet Vaccination'
    _order = 'date desc, id desc'

    pet_id = fields.Many2one(
        'pet.pet',
        string="Pet",
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(string="Vaccination Date", required=True)
    vaccine_type = fields.Char(string="Vaccine Type", required=True)
    next_date = fields.Date(string="Next Vaccination Date")
    notes = fields.Text(string="Notes")
    doctor_id = fields.Many2one(
        'res.partner',
        string="Doctor",
        domain=[('is_company', '=', False)],
    )


class PetMedicalHistory(models.Model):
    _name = 'pet.medical.history'
    _description = 'Pet Medical History'
    _order = 'date desc, id desc'

    pet_id = fields.Many2one(
        'pet.pet',
        string="Pet",
        required=True,
        ondelete='cascade',
    )
    date = fields.Datetime(string="Examination Date", default=fields.Datetime.now, required=True)
    symptoms = fields.Text(string="Symptoms", required=True)
    diagnosis = fields.Text(string="Diagnosis")
    treatment = fields.Text(string="Treatment")
    doctor_id = fields.Many2one(
        'res.partner',
        string="Doctor",
        domain=[('is_company', '=', False)],
    )

