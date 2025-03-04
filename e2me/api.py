
import toml
import os
from .send_email import send_email


def run(subject_str: str = "", body_str: str = "", config_path: str = "e2me.toml"):
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}\n")
        return
    
    config = toml.load(config_path)
    if subject_str != "":
        config["content"]["subject"] = subject_str
    if body_str != "":
        config["content"]["body"] = body_str
    send_email(config)