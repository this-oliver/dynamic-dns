class Record:
    """Base class for DNS records."""
    def __init__(self, provider, domain_name):
        self.provider = provider
        self.domain_name = domain_name
        if not self.provider:
            raise ValueError("Provider is required for each record.")
        if not self.domain_name:
            raise ValueError("Domain name is required for each record.")