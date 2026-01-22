# -*- coding: utf-8 -*-
{
    'name': 'Pet Hospital Management',
    'summary': 'Manage pets, owners, and veterinary services',
    'description': """
Pet Hospital Management System
- Manage pets and owners
- Veterinary appointments
- Medical records
- Billing and invoices
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Services',
    'version': '17.0.1.0',

    'depends': [
        'base',
        'product',
    ],

    'data': [
        'security/pet_security.xml',
        'security/ir.model.access.csv',
        'views/pet_views.xml',
        'views/pet_type_views.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/pet_appointment_views.xml',
        'views/pet_booking_views.xml',
        'views/menus.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
}
