from typing import Dict


from .email_server import get_email_server, EmailServer



def receive_email(config: Dict):

    email_user = config["email"]["email"]
    email_password = config["email"]["passwd"]
    email_server = get_email_server(email_user, email_password)
    email_server.receive(config["email"].get("pop3_email_num", 5))
    email_server.select_mail()