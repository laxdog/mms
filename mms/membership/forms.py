# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import DataRequired

from mms.user.models import User
from mms.membership.models import MembershipPlan
from mms.payments import types

class Join(Form):
    """Join form."""

    payment_type = SelectField("Payment Type",
                               choices=types)

    
