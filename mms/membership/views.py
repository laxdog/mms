# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import MembershipPlan, Membership, db
from ..user.models import User
from ..payments.stripe import stripe_keys
from ..payments.braintree import get_client_token
blueprint = Blueprint('membership', __name__, url_prefix='/membership', static_folder='../static')


@blueprint.route('/')
@login_required
def plans():
    """List available membership plans."""
    return render_template('membership/index.html', plans=MembershipPlan.query.all(), purchasables=[])

@blueprint.route('/join')
@login_required
def join():
    """
    Join or Change to a particular membership plan or purchase
    :param plan: 
    :param user: 
    :return: 
    """
    plan=request.args['plan']
    plan = MembershipPlan.query.filter_by(name=plan).first()

    return render_template('membership/join.html', plan=plan,
                           stripe_key=stripe_keys['publishable_key'],
                           braintree_key=get_client_token())

@blueprint.route('/charge', methods=['POST'])
@login_required
def charge():
    """Action a Membership Charge"""
    flash("Everyones a freeloading bastard! :D")
    plan=request.args['plan']
    plan = MembershipPlan.query.filter_by(name=plan).first()

    Membership.create(
        user=current_user,
        membership_type=plan,
        payment_processor='FAKE',
        payment_id='FAKE'
    )
    return redirect(url_for('plans'))




@blueprint.route('/cancel', methods=['POST', 'GET'])
@login_required
def cancel():
    plan=request.args['plan']
    if request.form.get('check', False):
        plan = MembershipPlan.query.filter_by(name=plan).first()
        deleted=False
        if current_user.is_current_member(plan):
            for m in current_user.membership:
                if m.membership_type==plan:
                    try:
                        current_user.membership.remove(m)
                        Membership.query.filter_by(id=m.id).delete()
                        db.session.commit()
                    except:
                        db.session.rollback()
                        raise
                    return redirect(url_for('membership'))
            if not deleted:
                flash("Couldn't find a membership to delete even though you're a member!", category='error')
                return redirect(url_for('membership'))
        else:
            flash("You're not that type of member so you can't cancel nothing", category='warning')
            return redirect(url_for('membership'))
    else:
        return render_template('membership/cancel.html', plan=plan)
