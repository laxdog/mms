import stripe
from flask import request
import os
from mms.membership.models import MembershipPlan
from mms.user.models import User

stripe_keys = {
  'secret_key': os.environ['STRIPE_KEY'],
  'publishable_key': os.environ['STRIPE_PUB']
}

stripe.api_key = stripe_keys['secret_key']


stripe_interval_map={
    'MONTHLY':'month',
    'ANNUAL':'year'
}
#todo cache these
def get_current_plans():
    #todo Deal with "has_more"
    return stripe.Plan.list()['data']

def get_current_customers():
    #todo Deal with "has_more"
    return stripe.Customer.list()['data']

def plan_id_hash(plan:MembershipPlan):
    return "{name}-{interval}-{price}".format(plan)

def create_membership_plan(plan:MembershipPlan):
    """
    Create a stripe plan if an existing plan does not have an appropriate plan id
    otherwise return the matching stripe plan id (as defined in plan_id_hash)
    :param plan: 
    :return: 
    """
    proposed_id = plan_id_hash(plan)
    for p in get_current_plans():
        if p.id==proposed_id:
            return p.id

    stripe_plan = stripe.Plan.create(
        name=plan.name,
        id=proposed_id,
        interval=stripe_interval_map[plan.interval],
        currency='GBP',
        amount=plan.price
    )
    return proposed_id

def create_customer(user:User):
    """
    Create a stripe customer if an existing membership does not have an appropriate payment id
    otherwise return the customers existing stripe customer id
    :param user: 
    :return: 
    """
    for m in user.membership:
        if m.payment_processor=='Stripe' and m.payment_id in get_current_customers():
            return m.payment_id

    stripe_customer = stripe.Customer.create(
        email=user.payment_email if user.payment_email is not None else user.email,
        source=request.form['stripeToken']
    )
    return stripe_customer.id

def create_subscription(user:User, plan:MembershipPlan):
    stripe_customer_id=create_customer(user)
    stripe_plan_id=create_membership_plan(plan)
    stripe_subscription = stripe.Subscription.create(
        customer=stripe_customer_id,
        plan=stripe_plan_id
    )

    return dict(payment_processor='Stripe', payment_id=stripe_subscription.id)


