import re
import requests
from typing import Callable, Optional

IP_ADDRESS_PATTERN = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

def parse_ipify(response: requests.Response) -> str:
    """Parses the plain text response from ipify."""
    return response.text.strip()

def parse_ip_api(response: requests.Response) -> str:
    """Parses the JSON response from ip-api.com."""
    data = response.json()
    return data.get("query", "")
    
def parse_ip_who_is(response: requests.Response) -> str:
    """Parses the JSON response from ipwho.is."""
    data = response.json()
    return data.get("ip", "")

class Oracle:
    def __init__(self, url: str, parse_func: Callable[[requests.Response], str], query: Optional[str] = None):
        self.url = url
        self.parse_func = parse_func

    def fetch(self) -> str:
        """Fetches data from the oracle and parses it."""
        try:
            res = requests.get(self.url, timeout=5)
            res.raise_for_status()
            return self.parse_func(res)
        except requests.exceptions.RequestException as e:
            # Re-raise to be handled by the loop in get_ip_address
            raise e

ORACLES = [
    Oracle("https://api.ipify.org", parse_ipify),
    Oracle("http://ip-api.com", parse_ip_api),
    Oracle("http://ipwho.is", parse_ip_who_is)
]

def is_ip_address(value: str) -> bool:
    return re.match(IP_ADDRESS_PATTERN, value) is not None

def get_ip_address() -> str:
    """Get the ip address of the host machine using several oracles."""
    ips = {}
    
    for oracle in ORACLES:
        ip = oracle.fetch()
        if is_ip_address(ip):
            if ips[ip] is None:
              ips[ip] = 1
            else:
              ips[ip] = ips[ip] + 1

    most_probable_ip_key = None
    for current_key in ips.keys():
      if most_probable_ip_key is None:
        most_probable_ip_key = current_key
      elif ips[current_key] > ips[most_probable_ip_key]:
        most_probable_ip_key = current_key

    return ips[most_probable_ip_key]
