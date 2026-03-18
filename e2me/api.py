import os

import toml

from .send_email import send_email as _send_email
from typing import List


def send_email(subject: str = "", body: str = "", cc: List[str] = None, to: str = None, config_path: str = "e2me.toml"):
    '''
    Send an email with the specified subject, body, and recipients.
    
    Args:
        subject_str: The subject of the email.
        body_str: The body of the email.
        cc: A list of email addresses to be added as CC recipients. ["<EMAIL1>", "<EMAIL2>"]
    '''
    default_config_path = os.path.join(os.path.dirname(__file__), "e2me.toml")
    if not os.path.exists(config_path):
        config_path = default_config_path

    config = toml.load(config_path)
    if subject != "":
        config["content"]["subject"] = subject
    if body != "":
        config["content"]["body"] = body
    if cc:
        config["content"]["cc"] = cc
    if to:
        config["email"]["to"] = to
    _send_email(config)


run = send_email
