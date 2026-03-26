"""
This script is designed to update DNS records with the host's current IP address. At a high level, the script performs the following steps:

1. Parses DNS records that need to be updated from a configuration file or command-line arguments.
2. Fetches the current IP address from an external service.
3. Updates the DNS records with the current IP address using the appropriate API for the DNS provider
"""

import os
import argparse
from src.utils.logger import setup_logging
from src.common.config import Config, parse_config
from src.common.record import Record
from src.providers.cloudflare import CloudflareProvider
from src.utils.ip import get_ip_address

DEFAULT_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dynamic_dns.log')
DYNAMIC_DNS_CONFIG_FILE = os.environ.get('DYNAMIC_DNS_CONFIG_FILE', None)
DYNAMIC_DNS_LOG_FILE = os.environ.get('DYNAMIC_DNS_LOG_FILE', None)

def main():
    parser = argparse.ArgumentParser(description='Update DNS records with current IP address.')
    parser.add_argument('--log', type=str, help=f'Log update operations to the specified log file (Default: {DEFAULT_LOG_FILE})', default=DYNAMIC_DNS_LOG_FILE or DEFAULT_LOG_FILE)
    parser.add_argument('--config', type=str, help='Path to the configuration YAML file')
    parser.add_argument('--provider', type=str, help='DNS provider name (e.g., cloudflare)')
    parser.add_argument('--token', type=str, help='API token for the DNS provider')
    parser.add_argument('--domain', type=str, help='Domain name to update')
    args = parser.parse_args()

    logger = setup_logging(log_file=args.log)

    if args.config or DYNAMIC_DNS_CONFIG_FILE:
        config_path = args.config or DYNAMIC_DNS_CONFIG_FILE
        logger.info(f"Loading configuration from {config_path}")
        config = parse_config(config_path)
    elif args.provider and args.domain:
        if args.provider.lower() == 'cloudflare' and not args.token:
            logger.error("Cloudflare token is required when using Cloudflare provider.")
            return
        record = Record(provider=args.provider, domain_name=args.domain, token=args.token)
        config = Config(records=[record])
    else:
        logger.error("No valid configuration provided. Please specify either a config file or domain with records to update.")
        parser.print_help()
        return
    
    try:
        ip_address = get_ip_address()
        logger.info(f"Current IP address: {ip_address}")
    except Exception as e:
        logger.error(e)
        return

    for record in config.records:
        try:
            if record.provider.lower() == 'cloudflare':
                provider = CloudflareProvider(token=record.token)
                result = provider.update_dns_record(record, ip_address)
                logger.info(f"Successfully updated {record.domain_name} from {result.old_ip} to {result.new_ip} in {record.provider} DNS provider.")
            else:
                logger.error(f"Failed to update {record.domain_name}: Unsupported provider {record.provider}")
        except Exception as e:
            logger.error(f"Failed to update {record.domain_name} in {record.provider} DNS provider: {str(e)}")


if __name__ == "__main__":
    main()
