# Dynamic DNS

Update your DNS records with your server's latest IP Address!

Features:

- automatically identify IP address
- update dns records

Supported DNS Providers:

- Cloudflare (`cloudflare`)

## Getting Started

Prerequisites:

- Python 3.12 or higher

## Usage

Dynamic DNS can be used with a configuration file or with command line arguments.

## Command Line Arguments

```bash
usage: main.py [-h] [--config CONFIG] [--provider PROVIDER] [--token TOKEN] [--domain DOMAIN]

Update DNS records with current IP address.

options:
  -h, --help           show this help message and exit
  --config CONFIG      Path to the configuration YAML file
  --provider PROVIDER  DNS provider name (e.g., cloudflare)
  --token TOKEN        API token for the DNS provider
  --domain DOMAIN      Domain name to update
```

Example:

```bash
# update ip address for example.com using cloudflare provider with api token
python main.py --provider cloudflare --token <API_TOKEN> --domain example.com
```

## Configuration File

The configuration file should be in YAML format and contain the necessary information for the DNS provider and the domain to update.

The structure of the configuration file is as follows:

```yaml
records:
  - provider: cloudflare
    token: <API_TOKEN>
    domain: example.com
```

The example above will update the IP address for `example.com` using the Cloudflare provider with the specified API token.

### Credits

This repository is inspired by the archived [troglobit/inadyn](https://github.com/troglobit/inadyn) which supported me in the past with dynamic DNS updates.
