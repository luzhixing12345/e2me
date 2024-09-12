import os
from datetime import datetime
import email.message
import re
import email
from email.header import decode_header
from email.utils import parseaddr
import arrow

class Email:

    def __init__(self) -> None:
        
        self.sub_emails = []
        
        self.date = None
        self.sender_name = None
        self.sender_email = None

        self.receiver_name = None
        self.receiver_email = None

        self.subject = None
        self.body = None
        self.attachments = []
        self.attachment_datas = []

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        info_str = f"[{self.date}] {self.subject} [{self.sender_email}]"
        if self.attachments:
            info_str += '\n'
            info_str += '     附件: '
            info_str += ', '.join(self.attachments)
        return info_str

def parser_content(msg: email.message.EmailMessage, indent: int) -> Email:
    """
    解析邮件内容,包括邮件头部、正文和附件,并保存附件.

    Args:
        msg: 邮件消息对象.
        indent: 缩进层级,用于打印输出.
    """
    email = Email()
    if indent == 0:
        # 解析邮件头部信息
        parser_email_header(msg, email)
        parse_mail_time(msg, email)

    # 下载附件
    for part in msg.walk():
        file_name = part.get_filename()  # 获取附件名称
        if file_name is None:
            continue

        # 对附件名称进行解码
        filename = decode_str(file_name)
        # 下载附件
        data = part.get_payload(decode=True)  # 需要使用 decode=True
        email.attachments.append(filename)
        email.attachment_datas.append(data)

    if msg.is_multipart():
        # 如果邮件对象是一个MIMEMultipart, get_payload()返回list,包含所有的子对象:
        parts = msg.get_payload()
        for part in parts:
            sub_email = parser_content(part, indent + 1)  # 递归打印每一个子对象
            email.sub_emails.append(sub_email)
    else:
        # 解析正文
        content_type = msg.get_content_type()
        if content_type == "text/plain" or content_type == "text/html":
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset and content:
                content_decoded = content.decode(charset)
                # print(f"{'  ' * indent}正文内容为: {content_decoded}")
                email.body = content_decoded
    return email


def parser_email_header(msg: email.message.EmailMessage, email: Email) -> None:
    """
    解析并打印邮件的标题、发件人和收件人信息.

    Args:
        msg: 邮件消息对象.
    """
    # 解析邮件标题
    subject = msg["Subject"]
    value, charset = decode_header(subject)[0]
    if isinstance(value, bytes) and charset:
        value = value.decode(charset)
    # print(f"邮件标题: {value}")
    email.subject = value

    # 解析发送人信息
    hdr, addr = parseaddr(msg["From"])
    name, charset = decode_header(hdr)[0]
    if isinstance(name, bytes) and charset:
        name = name.decode(charset)
    # print(f"发送人邮箱名称: {name},发送人邮箱地址: {addr}")
    email.sender_name = name
    email.sender_email = addr

    # 解析接收人信息
    hdr, addr = parseaddr(msg["To"])
    name, charset = decode_header(hdr)[0]
    if isinstance(name, bytes) and charset:
        name = name.decode(charset)
    # print(f"接收人邮箱名称: {name},接收人邮箱地址: {addr}")
    email.receiver_name = name
    email.receiver_email = addr


def decode_str(s: str) -> str:
    """
    解码字符串.

    Args:
        s: 待解码的字符串.

    Returns:
        解码后的字符串.
    """
    value, charset = decode_header(s)[0]
    if isinstance(value, bytes) and charset:
        value = value.decode(charset)
    return value


def guess_charset(msg: email.message.EmailMessage) -> str:
    """
    猜测邮件的字符编码.

    Args:
        msg: 邮件消息对象.

    Returns:
        邮件的字符编码.
    """
    # 从msg对象获取编码
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到,再从Content-Type字段获取:
        content_type = msg.get("Content-Type", "").lower()
        for item in content_type.split(";"):
            item = item.strip()
            if item.startswith("charset"):
                charset = item.split("=")[1]
                break
    return charset


def parse_mail_time(msg: email.message.EmailMessage, email: Email) -> datetime:
    """
    解析邮件的时间字符串为 datetime 对象.

    Args:
        mail_datetime: 邮件时间字符串.

    Returns:
        解析后的 datetime 对象.
    """

    GMT_FORMAT = "%a, %d %b %Y %H:%M:%S"
    GMT_FORMAT2 = "%d %b %Y %H:%M:%S"

    if "date" in msg:
        mail_datetime = msg["date"]
    elif "Date" in msg:
        mail_datetime = msg["Date"]
    else:
        # QQ 邮箱没有 date 字段,使用 Received 字段匹配处理
        date_pattern = re.compile(
            r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s+(\d{1,2}\s+\w{3}\s+\d{4}\s+\d{2}:\d{2}:\d{2})\s+.*\b"
        )
        received_headers = msg.get_all('Received', [])
        for header in received_headers:
            match = date_pattern.search(header)
            if match:
                date_str = match.group(1)
                mail_datetime = date_str
                break
        # raise ValueError("邮件时间格式解析错误")

    index = mail_datetime.find(" +0")
    if index > 0:
        mail_datetime = mail_datetime[:index]  # 去掉+0800
    formats = [GMT_FORMAT, GMT_FORMAT2]
    email.date = mail_datetime
    for ft in formats:
        try:
            mail_datetime_obj = datetime.strptime(mail_datetime, ft)
            max_mail_time_str = arrow.get(mail_datetime_obj).format("YYYY-MM-DD HH:mm")
            # print("邮件接收时间为:" + max_mail_time_str)
            email.date = max_mail_time_str
            return
        except ValueError:
            pass
    # raise ValueError(f"邮件时间格式解析错误 {mail_datetime}")
