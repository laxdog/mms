# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from mms.database import Column, Model, SurrogatePK, db, reference_col, relationship
from mms.extensions import bcrypt, admin, sqla, ManagmentSecView
from mms.user.models import User

membership_intervals = db.Enum('DAILY','MONTHLY','ANNUAL')

class MembershipPlan(SurrogatePK, Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), nullable=False)
    description = Column(db.Text)
    price = Column(db.Float)
    periodic = Column(db.Boolean, default=True)
    interval = Column(membership_intervals,default='MONTHLY')


    def has_member(self, user:User):
        for member in self.membership:
            if member.user == user:
                return True
        return False

    def __str__(self):
        return '%s' % (self.name)

class Membership(SurrogatePK, Model):
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref('memberships',
                                                 cascade='all, delete-orphan'))

    payment_processor = Column(db.String(16), nullable=True)
    payment_id = Column(db.String(80), nullable=True)

    membership_type_id = Column(db.Integer, db.ForeignKey(MembershipPlan.id))
    membership_type = db.relationship(MembershipPlan, backref='membership')

    started    = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    ended = Column(db.DateTime, nullable=True, default=None)

    def is_current(self):
        if self.ended is None:
            return True
        elif self.ended > dt.datetime.now():
            return True
        else:
            return False




    def __repr__(self):
        return "%s: %s (%s-%s)" % (self.membership_type.name,
                                   self.user.username,
                                   self.started, self.ended)


admin.add_view(ManagmentSecView(MembershipPlan, db.session, endpoint="plans"))
admin.add_view(ManagmentSecView(Membership, db.session, endpoint="memberships"))