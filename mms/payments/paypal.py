import paypalrestsdk
from paypalrestsdk import BillingPlan, BillingAgreement
from ..user.models import MembershipPlan


api = paypalrestsdk.Api({
  'mode': 'sandbox',
  'client_id': 'AS6BGmUdoBXLhbOva4zTlakpC6cb6IA_sovlZed-dd4BOkQZuFPtlPKn5RloYi3Zze57cIUHKmSH4EiI',
  'client_secret': 'EMiyfLU4uEN_755tgdoeGOcpzghPInxYFNpqaBYQgHYSECSMZTklkHND1iqCVNcdpyEAcjydXkXc4_tI'})

def getplans():
    plans = BillingPlan.all(api=api)
    if 'plans' in plans:
        return plans['plans']
    else:
        return None


def generate_billing_plan(membershipplan:MembershipPlan, replace=False):
    base_plan = {
        "name": membershipplan.name,
        "description": membershipplan.description,
        "merchant_preferences": {
            "auto_bill_amount": "yes",
            "cancel_url": "http://www.paypal.com/cancel",
            "initial_fail_amount_action": "continue",
            "max_fail_attempts": "0",
            "return_url": "http://www.paypal.com/execute",
        },
        "payment_definitions": [
            {
                "amount": {
                    "currency": "GBP",
                    "value": membershipplan.price
                },
                "cycles": "0",
                "frequency": "MONTH",
                "frequency_interval": membershipplan.interval_months,
                "name": "{} Monthly".format(membershipplan.interval_months),
                "type": "REGULAR"
            }
        ],
        "type": "INFINITE"
    }

    if membershipplan.payment_key and not replace:
        raise ValueError("This membership plan already has a membership key, may need replacing")
    draft_plan = BillingPlan(base_plan, api=api)
    do_replace = False
    current_plan = None
    for current_plan in getplans()['plans']:
        if current_plan['name'] == draft_plan['name']:
            if not replace:
                raise ValueError("A plan with that name already exists at id {}")
            else:
                do_replace = True
    if do_replace:
        current_plan.replace([{
        "op": "replace",
        "path": "/",
        "value": draft_plan.to_dict()
        }])
        plan_id = current_plan['id']
    else:
        draft_plan.create()
        for current_plan in getplans()['plans']:
            if current_plan['name'] == draft_plan['name']:
                plan_id = current_plan['id']
                break
    membershipplan.payment_key = plan_id
    membershipplan.save()


def delete_plan(plan_id):
    p=BillingPlan.find(plan_id, api=api)
    p.replace([{
            "op": "replace",
            "path": "/",
            "value": {
                "state": "DELETED"
            }
        }]
    )