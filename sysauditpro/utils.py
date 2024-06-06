import logging
import configparser
import os

# Configue logs
def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load of configurations file
def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        logging.error(f"Configurations file {config_file} not found.")
        return None
    config.read(config_file)
    return config

# Function for path check
def safe_path_check(path):
    """Check if path exists."""
    if not os.path.exists(path):
        logging.error(f"Path {path} doesn`t exist..")
        raise FileNotFoundError(f"This path {path} could not be found.")
    if not os.access(path, os.W_OK):
        logging.error(f"Path {path} is not write permission.")
        raise PermissionError(f"No write permission for the path {path}.")
    return True
