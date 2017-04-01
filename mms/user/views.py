# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from mms.database import db
from mms.extensions import ManagmentSecView, admin
from mms.user.models import UserModelView
from mms.utils import *
from .forms import EditForm
from .models import User, Role

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html', users = User.query.all())


@blueprint.route('/<username>')
@login_required
def member(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash_errors('Member {username} not found'.format(username))
        return redirect('/')
    else:
        return render_template('users/profile.html', user=user)

@blueprint.route('/<username>/edit', methods=['GET','POST'])
@login_required
def edit(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash_warn('Member {username} not found'.format(username), category='warning')
        return redirect('/')
    else:
        form = EditForm(request.form, obj=user)
        if form.validate_on_submit():
            user.update(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                about=form.about.data,
                url=form.url.data

            )
            user.save()
            return redirect(url_for('user.member', username=user.username))
        else:
            flash_errors(form)
        return render_template('users/edit.html', form=form)


# Add views
admin.add_view(UserModelView(User, db.session, endpoint="users"))
admin.add_view(ManagmentSecView(Role, db.session, endpoint="roles"))
