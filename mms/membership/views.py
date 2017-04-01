# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required
from ..membership.models import MembershipPlan
blueprint = Blueprint('membership', __name__, url_prefix='/membership', static_folder='../static')


@blueprint.route('/')
@login_required
def membership_plans():
    """List available membership plans."""
    return render_template('membership/index.html', plans=MembershipPlan.query.all())

