"""Core API structure"""

class Client:
    def __init__(self, domain, secret, host="https://customer.noda.se"):
        self.domain = domain
        self.secret = secret
        self.host = host
        self.base_path = f"{host}/{domain}/api/v1"
