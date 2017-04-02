#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys

from flask.helpers import get_debug_flag
from mms.user.models import User, Role, db, bcrypt

from mms.app import create_app
from mms.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig


def main():
    """Main entry point for script."""
    app=create_app(CONFIG)
    email='admin@farsetlabs.org.uk'

    password='Fhearsaid'

    with app.app_context():
        db.metadata.create_all(db.engine)

        if email is None:
            if User.query.all():
                create = input('A user already exists! Create another? (y/n):')
                if create == 'n':
                    return
            email = input('Enter email address')
        if password is None:
            password = getpass()
            assert password == getpass('Password (again):')

        user = User.query.filter_by(username='admin').first()
        if user is not None:
            print(user)
            user.update(email=email)
            user.set_password(password)
        else:
            user = User(username='admin', email=email, password=password, active=True)
        role = Role.query.filter_by(name='admin').first()
        if role is not None:
            role.users.append(user)
        else:
            role = Role(name='admin', description="Administrative Superuser", users=[user])
        db.session.add(user)
        db.session.add(role)
        db.session.commit()
        print('User added.')





if __name__ == '__main__':
    sys.exit(main())