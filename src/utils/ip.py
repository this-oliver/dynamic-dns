import re
import requests

IP_ADDRESS_PATTERN = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

def is_ip_address(value):
  return re.match(IP_ADDRESS_PATTERN, value) is not None

def get_ip_address():
  """Get the ip address of the host machine."""
  res = requests.get('https://api.ipify.org')
  if res.status_code == 200:
    ip = res.text.strip()
    if is_ip_address(ip):
      return ip
