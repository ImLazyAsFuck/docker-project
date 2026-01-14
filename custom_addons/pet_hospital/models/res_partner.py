# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pet_ids = fields.One2many(
        'pet.pet',
        'owner_id',
        string="Pets"
    )
