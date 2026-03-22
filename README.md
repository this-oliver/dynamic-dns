# dynamic-dns

Keep your DNS records up to date with your host's current IP address using `dynamic-dns`. This tool automatically identifies your IP address and updates your DNS records accordingly, ensuring that your domain always points to the correct location.

Features:

- automatically identify IP address
- update dns records

Supported DNS Providers:

- Cloudflare (`cloudflare`)

## Getting Started

Prerequisites:

- Python 3.12 or higher

## Usage

Dynamic DNS can be used with a configuration file or directly via command line arguments.

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

Currently, `dynamic-dns` supports the following DNS providers:

- Cloudflare (`cloudflare`)

> [!TIP]
> If you cannot find your DNS provider in the list, feel free to contribute by implementing a [new provider](src/providers/) and submitting a pull request.

### Configuration File

```yaml
records:
  - provider: cloudflare
    token: <API_TOKEN>
    domain: example.com
```

A configuration file allows you to specify multiple records to update, each with its own provider, token, and domain. This is useful if you want to update multiple DNS records at once or if you have different providers for different domains.

To use a configuration file, create a YAML file (e.g., `config.yaml`) with the structure shown above. Each record in the `records` list should include the `provider` and `domain` fields, as well as the `token` field for authentication with the DNS provider.

Once you have your configuration file ready, run the following command to update your DNS records:

```bash
python -m src.main --config path/to/config.yaml
```

### Command Line Arguments

Running the script with command line arguments allows you to update a single DNS record without needing a configuration file. This is useful for quick updates.

```bash
python -m src.main --provider cloudflare --token <API_TOKEN> --domain example.com
```

The command line above will update the DNS record for `example.com` using the Cloudflare provider with the specified API token.

### Docker

> [!WARNING]
> Always pin the image to a specific version or digest rather than using `latest` to ensure stability and avoid unexpected issues due to changes in the image.

You can also run `dynamic-dns` as a container if you do not want to set up a Python environment. To do this, pull the latest image from GitHub Container Registry or build it yourself.

Pull the latest image:

```bash
# via GitHub Container Registry
docker pull ghcr.io/this-oliver/dynamic-dns:latest

# build yourself
git clone https://github.com/this-oliver/dynamic-dns.git
cd dynamic-dns
docker build -t dynamic-dns:local .
```

Run the container:

```bash
docker run -d -v /path/to/config.yaml:/app/config.yaml dynamic-dns:latest --config /app/config.yaml
```

## Practical Use Cases

### Home Servers + Cron Jobs

Unless you have a static IP address, your home network's IP address can change periodically. By using `dynamic-dns`, you can ensure that your domain always points to your home server, allowing you to access it remotely without worrying about IP changes.

With cron jobs, you can automate the process of updating your DNS records at regular intervals. For example, you can set up a cron job to run the `dynamic-dns` script every hour to check for IP changes and update your DNS records accordingly.

1. Create a configuration file (e.g., `~/.dynamic-dns/config.yaml`) with your DNS provider, token, and domain information.

```yaml
records:
  - provider: cloudflare
    token: <API_TOKEN>
    domain: hotdogs.com
```

2. Set up a cron job to run the `dynamic-dns` script at your desired interval (e.g., every hour).

```bash
0 * * * * docker run -d -v ~/.dynamic-dns/config.yaml:/app/config.yaml ghcr.io/this-oliver/dynamic-dns:latest --config /app/config.yaml
```

## Credits

This repository is inspired by the archived [troglobit/inadyn](https://github.com/troglobit/inadyn) which supported me in the past with dynamic DNS updates.
