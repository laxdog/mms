# -*- coding: utf-8 -*-
"""Payment Relationship models."""
import datetime as dt

from mms.database import Column, Model, SurrogatePK, db, reference_col, relationship
from mms.extensions import bcrypt, admin, sqla, ManagmentSecView
from mms.user.models import User

class PaymentID(SurrogatePK, Model):
    user = db.relationship(User, backref='paymentids')
    payment_processor = Column(db.String(16), nullable=False)
