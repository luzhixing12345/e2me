import re
import smtplib
import poplib

from .pop3 import *
from email.parser import Parser
import chardet
from enum import Enum
from typing import List
import time

class EmailType(Enum):
    QQ = "qq"
    GMAIL = "gmail"
    WANGYI163 = "163"


class EmailServer:

    def __init__(self, email_addr: str, passwd: str) -> None:
        print(f"create {self.__class__.__name__} email server for [{email_addr}]...")
        self.email_addr = email_addr
        self.passwd = passwd

        self.smtp_port = None
        self.smtp_ssl = None
        self.smtp_server = None

        self.pop3_port = None
        self.pop3_ssl = None
        self.pop3_server = None
        
        self.emails: List[Email]  = []
        self.download_path = "e2me-download"
        
        self.max_timeout = 5
        self.max_retries = 5

    def send(self, msg):

        smtp_type = smtplib.SMTP_SSL if self.smtp_ssl else smtplib.SMTP
        retries = 0
        while retries < self.max_retries:
            try:
                with smtp_type(self.smtp_server, self.smtp_port, timeout=self.max_timeout) as server:
                    # server.starttls()
                    server.login(self.email_addr, self.passwd)
                    server.send_message(msg)
                    server.quit()
                    print(f"Email sent successfully")
                    break
            except (smtplib.SMTPException, TimeoutError) as e:
                retries += 1
                print(f"Error sending email: {e}. Retrying {retries}/{self.max_retries}")
                time.sleep(1)  # 等待1秒后重试
            except Exception as e:
                print(f"Error sending email: {e}")

    def receive(self, receive_num: int):
        # 连接到 POP3 服务器
        pop3_type = poplib.POP3_SSL if self.pop3_ssl else poplib.POP3
        try:
            pop3_server = pop3_type(self.pop3_server, self.pop3_port)
            pop3_server.user(self.email_addr)
            pop3_server.pass_(self.passwd)

            # 列出邮件数量
            resp, mails, octets = pop3_server.list()
            num, total_size = pop3_server.stat()
            # print("邮件数量为:" + str(num))

            # 倒序遍历邮件, 获取最近 email_num 封邮件
            print("获取最近 " + str(receive_num) + " 封邮件")
            cnt = 0
            for i in range(len(mails), 0, -1):
                cnt += 1
                if cnt > receive_num:
                    break
                resp, lines, octets = pop3_server.retr(i)
                # msg_content = b"\r\n".join(lines).decode("utf-8")
                msg_content = b"\r\n".join(lines)
                detected_encoding = chardet.detect(msg_content)["encoding"]
                encodings = [detected_encoding, "utf-8", "iso-8859-1", "windows-1252"]
                for encoding in encodings:
                    try:
                        msg_content_decoded = msg_content.decode(encoding, errors="ignore")
                        break  # 成功解码后退出循环
                    except Exception as e:
                        print(f"尝试使用编码 {encoding} 解码失败: {e}")
                else:
                    print(f"所有编码尝试失败,邮件索引: {i}")
                    continue
                msg = Parser().parsestr(msg_content_decoded)
                try:
                    # 解析邮件具体内容,包括正文,标题,和附件
                    email = parser_content(msg, 0)
                    self.emails.append(email)
                except Exception as e:
                    print(f"解析邮件内容时出错: {e}")

            # 退出
            pop3_server.quit()

        except Exception as e:
            print(f"获取邮件时出错: {e}")

    def select_mail(self) -> Email:
        
        if len(self.emails) == 0:
            print("No emails")
            return

        has_attachments = False
        for i, email in enumerate(self.emails):
            print(f"[{i}]: {email}")
            if len(email.attachments) > 0:
                has_attachments = True

        if not has_attachments:
            return
        
        index = input("输入索引下载邮件附件, 输入 q 退出: ")
        if index == "q":
            return
        elif index.isdigit() and int(index) < len(self.emails):
            email = self.emails[int(index)]
            if len(email.attachments) == 0:
                print("该邮件没有附件")
                return

            if not os.path.exists(self.download_path):
                os.mkdir(self.download_path)
            
            for i, data in enumerate(email.attachment_datas):
                filename = email.attachments[i]
                with open(os.path.join(self.download_path, filename), "wb") as f:
                    f.write(data)
                print(f"已保存 {os.path.join(self.download_path, filename)}")
        else:
            print("Invalid index")
            return

class WANGYI163(EmailServer):

    def __init__(self, email_addr: str, passwd: str) -> None:
        super().__init__(email_addr, passwd)
        self.smtp_port = 25
        self.smtp_ssl = False
        self.smtp_server = "smtp.163.com"

        self.pop3_port = 110
        self.pop3_ssl = False
        self.pop3_server = "pop.163.com"


class GMAIL(EmailServer):

    def __init__(self, email_addr: str, passwd: str) -> None:
        super().__init__(email_addr, passwd)
        self.smtp_port = 465
        self.smtp_ssl = True
        self.smtp_server = "smtp.gmail.com"

        self.pop3_port = 995
        self.pop3_ssl = True
        self.pop3_server = "pop.gmail.com"


class QQ(EmailServer):

    def __init__(self, email_addr: str, passwd: str) -> None:
        super().__init__(email_addr, passwd)
        self.smtp_port = 465
        self.smtp_ssl = True
        self.smtp_server = "smtp.qq.com"

        self.pop3_port = 995
        self.pop3_ssl = True
        self.pop3_server = "pop.qq.com"


def get_email_server(email_addr: str, passwd: str) -> EmailServer:
    # 获取邮件服务器类型
    pattern = r"^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+)\.[a-zA-Z0-9-.]+$"
    match = re.match(pattern, email_addr)
    if match:
        email_servers = {EmailType.WANGYI163: WANGYI163, EmailType.GMAIL: GMAIL, EmailType.QQ: QQ}

        try:
            email_type = EmailType(match.group(1))
            return email_servers[email_type](email_addr, passwd)
        except Exception as e:
            print(f"Unsupported email type with email address: {email_addr}")
            print("supported email types: " + ", ".join([t.value for t in email_servers.keys()]))
            exit(1)
    else:
        raise ValueError(f"Invalid email address: {email_addr}")
