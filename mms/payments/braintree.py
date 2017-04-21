import braintree



def get_client_token():
    return braintree.ClientToken.generate()