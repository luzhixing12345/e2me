
import toml
import os
from .send_email import send_email

def run(config_path: str = "e2me.toml"):
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}\n")
        return
    
    config = toml.load(config_path)
    send_email(config)