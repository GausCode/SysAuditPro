import logging
import configparser
import os

# Konfigurieren des Logging
def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Laden der Konfiguration aus einer Datei
def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        logging.error(f"Konfigurationsdatei {config_file} nicht gefunden.")
        return None
    config.read(config_file)
    return config

# Hilfsfunktion für sichere Pfadüberprüfung
def safe_path_check(path):
    """Überprüft, ob der angegebene Pfad existiert und schreibgeschützt ist."""
    if not os.path.exists(path):
        logging.error(f"Pfad {path} existiert nicht.")
        raise FileNotFoundError(f"Der angegebene Pfad {path} wurde nicht gefunden.")
    if not os.access(path, os.W_OK):
        logging.error(f"Pfad {path} ist nicht beschreibbar.")
        raise PermissionError(f"Keine Schreibberechtigung für den Pfad {path}.")
    return True
