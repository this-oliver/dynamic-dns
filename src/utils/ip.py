import re
import requests

def is_ip_address(value):
  pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
  return re.match(pattern, value) is not None

def get_ip_address():
  """Get the ip address of the host machine."""
  res = requests.get('https://api.ipify.org')
  if res.status_code == 200:
    ip = res.text.strip()
    if is_ip_address(ip):
      return ip
