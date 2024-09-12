from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

from typing import Dict
import time
import getpass
import socket
import platform
from .email_server import get_email_server, EmailServer


def parse_content(text: str):
    """
    "[<DATE>:<TIME>] <USER>:<HOSTNAME>"
    """
    built_in_dict = {
        "<DATE>": time.strftime("%Y-%m-%d", time.localtime()),
        "<USER>": getpass.getuser(),
        "<HOSTNAME>": socket.gethostname(),
        "<TIME>": time.strftime("%H:%M:%S", time.localtime()),
        "<KERNEL>": platform.release(),
    }
    for key, value in built_in_dict.items():
        text = text.replace(key, value)
    return text


# 邮件发送函数
def send_email(config: Dict):
    # 发送者和接收者邮箱信息
    email_addr = config["email"]["email"]
    passwd = config["email"]["passwd"]
    email_server: EmailServer = get_email_server(email_addr, passwd)

    # 创建邮件对象
    msg = MIMEMultipart()
    msg["From"] = email_addr
    msg["To"] = email_addr
    msg["Subject"] = parse_content(config["content"]["subject"])

    # 添加邮件正文
    body = parse_content(config["content"]["body"])
    msg.attach(MIMEText(body, "plain"))

    # 添加附件(如果有)
    if config.get("file"):
        files = config["file"]["file_path"]
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
                    msg.attach(part)
            else:
                print(f"File not found: {file_path}")
    email_server.send(msg)
    return True
