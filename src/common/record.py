class Record:
    """Class for DNS records."""
    def __init__(self, provider, domain, token=None, old_ip=None, new_ip=None, updated=False):
        if not provider:
            raise ValueError("Provider is required for each record.")
        if not domain:
            raise ValueError("Domain name is required for each record.")
        self.provider = provider.lower()
        self.domain = domain
        self.token = token
        if self.provider == 'cloudflare' and not self.token:
            raise ValueError("Cloudflare token is required for Cloudflare records.")
        self.old_ip = old_ip
        self.new_ip = new_ip
        self.updated = updated
