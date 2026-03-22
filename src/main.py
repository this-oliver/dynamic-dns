"""
This script is designed to update DNS records with the host's current IP address. At a high level, the script performs the following steps:

1. Parses DNS records that need to be updated from a configuration file or command-line arguments.
2. Fetches the current IP address from an external service.
3. Updates the DNS records with the current IP address using the appropriate API for the DNS provider
"""

import argparse
import logging
from common.config import Config, parse_config
from providers.cloudflare import CloudflareRecord, CloudflareProvider
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
        if args.provider.lower() == 'cloudflare':
            record = CloudflareRecord(
                domain_name=args.domain,
                token=args.token,
            )
            config = Config(records=[record])
        else:
            logging.error(f"Unsupported provider: {args.provider}")
            return
    else:
        logging.error("No valid configuration provided. Please specify either a config file or domain with records to update.")
        parser.print_help()
        return
    
    successful_updates = []
    unsuccessful_updates = []

    for record in config.records:
        logging.info(f"Processing record for domain: {record.domain_name} with provider: {record.provider}")
    #    if record.provider.lower() == 'cloudflare':
    #        provider = CloudflareProvider(token=record.token)
    #        cloudflare_record = provider.get_dns_record(record)
    #        if not cloudflare_record:
    #            unsuccessful_updates.append((record, "Record not found"))
    #        try:
    #            ip_address = get_ip_address()
    #            provider.update_dns_record(cloudflare_record, ip_address)
    #            successful_updates.append(record)
    #        except Exception as e:
    #            unsuccessful_updates.append((record, str(e)))
    #    else:
    #        logging.error(f"Unsupported provider: {record.provider}")
    #        unsuccessful_updates.append((record, "Unsupported provider"))

    #logging.info(f"Successfully updated {len(successful_updates)} records.")
    #if unsuccessful_updates:
    #    logging.warning(f"Failed to update {len(unsuccessful_updates)} records:")
    #    for record, error in unsuccessful_updates:
    #        logging.warning(f" - {record.domain_name} ({record.provider}): {error}")


if __name__ == "__main__":
    main()