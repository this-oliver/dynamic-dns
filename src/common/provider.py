class Provider:
    """Interface for DNS providers."""
    def __init__(self, name: str):
        self.name = name

    def _is_valid_record(self, record):
        """Validate that the record has all necessary information."""
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def update_dns_record(self, record, ip_address):
        """Update the DNS record in DNS provider with the new IP address."""
        raise NotImplementedError("This method should be implemented by subclasses.")
