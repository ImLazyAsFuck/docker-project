# -*- coding: utf-8 -*-

from . import controllers
from . import models

def post_init_hook(env):
    """Hook được gọi sau khi module được install"""
    from .security import security_rules
    security_rules.post_init_hook(env.cr, env.registry)
