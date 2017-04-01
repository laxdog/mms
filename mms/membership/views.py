# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required
from ..user.models import MembershipPlan, Membership
blueprint = Blueprint('membership', __name__, url_prefix='/membership', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html', users = User.query.all())
