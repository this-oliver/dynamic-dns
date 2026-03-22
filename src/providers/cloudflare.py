import requests
from ..common.provider import Provider

BASE_URL="https://api.cloudflare.com/client/v4"


class CloudflareApiZone:
    """Class representing a Cloudflare DNS zone."""
    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status # e.g., "active", "pending", "moved" etc. caution if not active!


class CloudflareApiRecord:
    """Class representing a Cloudflare DNS record."""
    def __init__(self, id, zone, type, name, content, ttl, proxied):
        self.id = id
        self.zone = zone # Zone ID that this record belongs to
        self.type = type # e.g., "A", "CNAME", "TXT" etc.
        self.name = name # e.g., "subdomain.example.com"
        self.content = content # e.g., IP address for A record, target domain for CNAME etc.
        self.ttl = ttl
        self.proxied = proxied
        self.tags = [] # List of tags associated with the record, if any
        self.comment = None # Optional comment for the record


class CloudflareProvider(Provider):
    """Provider class for Cloudflare DNS management."""
    
    def __init__(self, token):
        self.token = token
        super().__init__("cloudflare")

    def _is_valid_record(self, record):
        """Validate that the record has all necessary information."""
        if record.provider.lower() != 'cloudflare':
            raise ValueError("Invalid provider for CloudflareProvider. Expected 'cloudflare'.")
        if not record.token:
            raise ValueError("Cloudflare token is required for Cloudflare records.")
        if not record.domain_name:
            raise ValueError("Domain name is required for Cloudflare records.")
        return True
    
    def _get_zones(self):
        """Fetch the list of zones from Cloudflare."""
        res = requests.get(
            f"{BASE_URL}/zones",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if res.status_code != 200:
            raise Exception(f"Failed to fetch zones from Cloudflare: {res.text}")
        return [CloudflareApiZone(id=zone['id'], name=zone['name'], status=zone['status']) for zone in res.json().get('result', [])]
    
    def _get_all_dns_records(self, zone_id):
        """Fetch the list of DNS records for a given zone from Cloudflare."""
        res = requests.get(
            f"{BASE_URL}/zones/{zone_id}/dns_records",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if res.status_code != 200:
            raise Exception(f"Failed to fetch DNS records from Cloudflare: {res.text}")
        return [CloudflareApiRecord(id=record['id'], zone=zone_id, type=record['type'], name=record['name'], content=record['content'], ttl=record['ttl'], proxied=record['proxied']) for record in res.json().get('result', [])]

    def _get_single_dns_record(self, record):
        """Fetch the DNS record from Cloudflare."""
        self._is_valid_record(record)
        zones = self._get_zones()
        for zone in zones:
            if record.domain_name.endswith(zone.name):
                records = self._get_all_dns_records(zone.id)
                for r in records:
                    if r.name == record.domain_name:
                        return r 
        return None
    
    def update_dns_record(self, record, ip_address):
        """Update the DNS record in Cloudflare with the new IP address."""
        cloudflare_record = self._get_single_dns_record(record)
        if not cloudflare_record:
            raise Exception(f"DNS record for {record.domain_name} not found in ${self.name}.")
        if cloudflare_record.type != 'A':
            raise Exception(f"DNS record type {cloudflare_record.type} is not supported for ip address updates. Only 'A' records can be updated with an IP address.")
        res = requests.put(
            f"{BASE_URL}/zones/{cloudflare_record.zone}/dns_records/{cloudflare_record.id}",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "type": cloudflare_record.type,
                "name": cloudflare_record.name,
                "content": ip_address,
                "ttl": cloudflare_record.ttl,
                "proxied": cloudflare_record.proxied
            }
        )
        if res.status_code != 200:
            raise Exception(f"Failed to update DNS record in Cloudflare: {res.text}")
        return res.json()
