# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from hashlib import md5
from flask_login import UserMixin
from sqlalchemy_utils.types import PhoneNumber, URLType, EmailType
from wtforms import PasswordField
from wtforms.validators import Optional, EqualTo

from mms.database import Column, Model, SurrogatePK, db, reference_col, relationship
from mms.extensions import bcrypt, ManagmentSecView

role_table = db.Table('role_table',
                      db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), nullable=False),
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
                      db.PrimaryKeyConstraint('role_id', 'user_id'))

class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    description = Column(db.Text)
    users = db.relationship('User', secondary=role_table, backref='roles')

    def __init__(self, name=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)

    def __str__(self):
        """Represent instance as a unique string."""
        return '{this.name}'.format(this=self)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    payment_email = Column(EmailType, unique=False, nullable=True)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    # Profile Attributes
    about = Column(db.UnicodeText, nullable=True)
    url = Column(URLType, nullable=True)


    def __init__(self, username=None, email='', password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def avatar(self, size):
        """Get the FQDN URL of the users avatar (defaults to gravatar)"""
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)


    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return ' '.join([n for n in [self.first_name, self.last_name] if n is not None])

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

    def __str__(self):
        """Represent instance as a unique string."""
        return '{this.username}'.format(this=self)


    def update(self, **kwargs):
        try:
            super(User, self).update(**kwargs)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True
        return False


class UserModelView(ManagmentSecView):
    form_excluded_columns = ('password')
    #  Form will now use all the other fields in the model

    #  Add our own password form field - call it password2
    form_extra_fields = {
        'new_password': PasswordField('New Password'),
        'confirm' : PasswordField('Verify password',
                            [Optional(), EqualTo('new_password', message='Passwords must match')])
    }

    def on_model_change(self, form, User, is_created):
        if form.new_password.data is not None:
            User.set_password(form.new_password.data)
            del form.new_password

