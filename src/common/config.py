import os
import yaml
from src.common.record import Record

class Config:
    """Class representing the configuration loaded from the YAML file."""
    def __init__(self, records: list[Record]):
        self.records = records

def parse_config(config_path):
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    records = [Record(**record) for record in config.get('records', [])]
    return Config(records)