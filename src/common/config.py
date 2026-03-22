import yaml
from common.record import Record

class Config:
    """Configuration class to hold all DNS records."""
    def __init__(self, records):
        self.records = records

def parse_config(config_path):
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    records = [Record(**record) for record in config['records']]
    return Config(records)