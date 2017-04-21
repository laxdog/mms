# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required
from .paypal import get_current_plans
blueprint = Blueprint('payments', __name__, url_prefix='/payments', static_folder='../static')


@blueprint.route('/')
@login_required
def billingplans():
    """List members."""
    return render_template('payments/index.html', plans_created=get_current_plans())
