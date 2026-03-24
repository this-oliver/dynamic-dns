import re
from src.common.record import Record
from src.utils.ip import is_ip_address

class UpdateResult:
    """Class representing the result of a DNS record update operation."""
    def __init__(self, provider: str, old_ip: str, new_ip: str):
        self.provider = provider
        self.old_ip = old_ip
        self.new_ip = new_ip
        if not is_ip_address(old_ip):
            raise ValueError(f"Invalid old IP address: {old_ip}")
        if not is_ip_address(new_ip):
            raise ValueError(f"Invalid new IP address: {new_ip}")

class Provider:
    """Interface for DNS providers."""
    def __init__(self, name: str):
        self.name = name

    def _is_valid_record(self, record: Record):
        """Validate that the record has all necessary information."""
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def update_dns_record(self, record: Record, ip_address: str) -> UpdateResult:
        """Update the DNS record in DNS provider with the new IP address."""
        raise NotImplementedError("This method should be implemented by subclasses.")
