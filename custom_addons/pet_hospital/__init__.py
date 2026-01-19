# -*- coding: utf-8 -*-

from . import controllers
from . import models

def post_init_hook(cr, registry):
    """Hook được gọi sau khi module được install"""
    from .security import security_rules
    security_rules.post_init_hook(cr, registry)
