import os
import smtplib

import toml

from .email_server import get_email_server
from .send_email import send_email as _send_email
from typing import List, Optional


def send_email(subject: str = "", body: str = "", cc: List[str] = None, config_path: str = "e2me.toml"):
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
    _send_email(config)


def check(config_path: str = "e2me.toml") -> Optional[str]:
    default_config_path = os.path.join(os.path.dirname(__file__), "e2me.toml")
    if not os.path.exists(config_path):
        config_path = default_config_path

    try:
        config = toml.load(config_path)
        email_addr = os.getenv("E2ME_EMAIL") or config["email"]["email"]
        passwd = os.getenv("E2ME_PASSWD") or config["email"]["passwd"]

        if not email_addr or email_addr == "your-email@example.com" or not passwd:
            return None

        email_server = get_email_server(email_addr, passwd)
        smtp_type = smtplib.SMTP_SSL if email_server.smtp_ssl else smtplib.SMTP

        with smtp_type(email_server.smtp_server, email_server.smtp_port, timeout=email_server.max_timeout) as server:
            server.login(email_addr, passwd)

        return email_addr
    except BaseException:
        return None
