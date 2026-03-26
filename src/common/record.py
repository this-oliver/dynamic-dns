class Record:
    """Class for DNS records."""
    def __init__(self, provider, domain_name, token=None):
        if not provider:
            raise ValueError("Provider is required for each record.")
        if not domain_name:
            raise ValueError("Domain name is required for each record.")
        self.provider = provider.lower()
        self.domain_name = domain_name
        self.token = token
        if self.provider == 'cloudflare' and not self.token:
            raise ValueError("Cloudflare token is required for Cloudflare records.")
        self.old_ip = None
        self.new_ip = None
        self.updated = False
