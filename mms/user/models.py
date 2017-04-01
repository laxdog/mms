# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from mms.database import Column, Model, SurrogatePK, db, reference_col, relationship
from mms.extensions import bcrypt, admin, sqla


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username=None, email='', password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class MembershipPlan(SurrogatePK, Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), nullable=False)
    description = Column(db.Text)
    price = Column(db.Float)
    payment_key = Column(db.Text)
    interval_months = Column(db.Integer,default=1)

    def __str__(self):
        return '%s - £%.2f' % (self.name, self.price)

class Membership(SurrogatePK, Model):
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref='membership')

    membership_type_id = Column(db.Integer, db.ForeignKey(MembershipPlan.id))
    membership_type = db.relationship(MembershipPlan, backref='membership')

    started = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    ended = Column(db.DateTime, nullable=True, default=None)

    def __str__(self):
        return "%s: %s (%s-%s)" % (self.membership_type.name,
                                   self.user.name,
                                   self.started, self.ended)


# Add views
admin.add_view(sqla.ModelView(User, db.session, endpoint="users"))
admin.add_view(sqla.ModelView(Role, db.session, endpoint="roles"))
admin.add_view(sqla.ModelView(MembershipPlan, db.session, endpoint="membership_plans"))
admin.add_view(sqla.ModelView(Membership, db.session, endpoint="memberships"))
