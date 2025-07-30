import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "config.yaml"

def load_config(item: str="", config_path: Path=CONFIG_PATH) -> dict:
    """Load the configuration from a YAML file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    if item:
        return config[item]
    return config