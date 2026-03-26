import re
import requests

IP_ADDRESS_PATTERN = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

def is_ip_address(value):
  return re.match(IP_ADDRESS_PATTERN, value) is not None

def get_ip_address():
  """Get the ip address of the host machine."""
  try:
      res = requests.get('https://api.ipify.org')
      res.raise_for_status()
      if res.status_code == 200:
        ip = res.text.strip()
        if is_ip_address(ip):
          return ip
  except requests.exceptions.ConnectionError as e:
      message = f"Connection failed likely due to timeout - {e}."
      raise Exception(message)
  except requests.RequestException as e:
      if hasattr(e, 'response') and e.response is not None:
        status_code = e.response.status_code
        message = f"({status_code}) Failed to fetch IP address - {e.response.reason}"
      raise Exception(e)
  except Exception as e:
      message = f"Failed to fetch IP address - {e}"
      raise Exception(message)
