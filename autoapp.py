# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from mms.app import create_app
from mms.settings import DevConfig, ProdConfig
from mms.user.models import User, Role

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

