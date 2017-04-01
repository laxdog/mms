# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from mms.database import Column, Model, SurrogatePK, db, reference_col, relationship
from mms.extensions import bcrypt, admin, sqla, ManagmentSecView
from mms.user.models import User

class MembershipPlan(SurrogatePK, Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), nullable=False)
    description = Column(db.Text)
    price = Column(db.Float)
    payment_key = Column(db.Text)
    interval_months = Column(db.Integer,default=1)

    def __str__(self):
        return '%s' % (self.name)

class Membership(SurrogatePK, Model):
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref='membership')

    membership_type_id = Column(db.Integer, db.ForeignKey(MembershipPlan.id))
    membership_type = db.relationship(MembershipPlan, backref='membership')

    started = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    ended = Column(db.DateTime, nullable=True, default=None)

    def __repr__(self):
        return "%s: %s (%s-%s)" % (self.membership_type.name,
                                   self.user.name,
                                   self.started, self.ended)


admin.add_view(ManagmentSecView(MembershipPlan, db.session, endpoint="membership_plans"))
admin.add_view(ManagmentSecView(Membership, db.session, endpoint="memberships"))