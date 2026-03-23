"""
This script is designed to update DNS records with the host's current IP address. At a high level, the script performs the following steps:

1. Parses DNS records that need to be updated from a configuration file or command-line arguments.
2. Fetches the current IP address from an external service.
3. Updates the DNS records with the current IP address using the appropriate API for the DNS provider
"""

import argparse
import logging
from src.common.config import Config, parse_config
from src.common.record import Record
from src.providers.cloudflare import CloudflareProvider
from src.utils.ip import get_ip_address

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
    elif args.provider and args.domain:
        if args.provider.lower() == 'cloudflare' and not args.token:
            logging.error("Cloudflare token is required when using Cloudflare provider.")
            return
        record = Record(provider=args.provider, domain_name=args.domain, token=args.token)
        config = Config(records=[record])
    else:
        logging.error("No valid configuration provided. Please specify either a config file or domain with records to update.")
        parser.print_help()
        return
    
    ip_address = get_ip_address()

    for record in config.records:
        if record.provider.lower() == 'cloudflare':
            try:
                provider = CloudflareProvider(token=record.token)
                result = provider.update_dns_record(record, ip_address)
                logging.info(f"Successfully updated {record.domain_name} from {result.old_ip} to {result.new_ip} in {record.provider} DNS provider.")
            except Exception as e:
                logging.error(f"Failed to update {record.domain_name} in {record.provider} DNS provider: {str(e)}")
        else:
            logging.error(f"Failed to update {record.domain_name}: Unsupported provider {record.provider}")

    logging.info("DNS record update process completed.")

if __name__ == "__main__":
    main()
