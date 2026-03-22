"""
This script is designed to update DNS records with the host's current IP address. At a high level, the script performs the following steps:

1. Parses DNS records that need to be updated from a configuration file or command-line arguments.
2. Fetches the current IP address from an external service.
3. Updates the DNS records with the current IP address using the appropriate API for the DNS provider
"""

import argparse
import logging
from common.config import Config, parse_config
from common.record import Record
from utils.ip import get_ip_address

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description='Update DNS records with current IP address.')
    parser.add_argument('--config', type=str, help='Path to the configuration YAML file')
    parser.add_argument('--provider', type=str, help='DNS provider name (e.g., cloudflare)')
    parser.add_argument('--token', type=str, help='API token for the DNS provider')
    parser.add_argument('--domain', type=str, help='Domain name to update')
    args = parser.parse_args()

    if args.config:
        logging.info(f"Loading configuration from {args.config}")
        config = parse_config(args.config)
    elif args.provider and args.token and args.domain:
        record = Record(
            domain_name=args.domain,
            token=args.token,
            provider=args.provider
        )
        config = Config(records=[record])
    else:
        logging.error("No valid configuration provided. Please specify either a config file or domain with records to update.")
        parser.print_help()
        return

    for record in config.records:
        logging.info(f"Processing record for domain: {record.domain_name} with provider: {record.provider}")


if __name__ == "__main__":
    main()