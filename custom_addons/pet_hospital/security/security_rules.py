# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    group_user = env.ref('pet_hospital.group_pet_user', raise_if_not_found=False)
    if not group_user:
        return
    
    models_to_rule = [
        ('pet.booking', 'Pet Booking: User chỉ xem của mình'),
        ('pet.appointment', 'Pet Appointment: User chỉ xem của mình'),
        ('pet.pet', 'Pet: User chỉ xem của mình'),
        ('pet.vaccination', 'Pet Vaccination: User chỉ xem của mình'),
        ('pet.medical.history', 'Pet Medical History: User chỉ xem của mình'),
    ]
    
    for model_name, rule_name in models_to_rule:
        model = env['ir.model'].search([('model', '=', model_name)], limit=1)
        if model:
            existing_rule = env['ir.rule'].search([
                ('name', '=', rule_name),
                ('model_id', '=', model.id)
            ], limit=1)
            
            if not existing_rule:
                env['ir.rule'].create({
                    'name': rule_name,
                    'model_id': model.id,
                    'domain_force': "[('create_uid', '=', user.id)]",
                    'groups': [(4, group_user.id)],
                })
