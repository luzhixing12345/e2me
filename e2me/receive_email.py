
from typing import Dict

import email.message
import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from email.parser import Parser
import os
import poplib
import shutil
from datetime import datetime
import arrow  # 轻量级的日期处理库


def parser_content(msg: email.message.EmailMessage, indent: int) -> None:
    """
    解析邮件内容，包括邮件头部、正文和附件，并保存附件。

    Args:
        msg: 邮件消息对象。
        indent: 缩进层级，用于打印输出。
    """
    if indent == 0:
        # 解析邮件头部信息
        parser_email_header(msg)

    # 下载附件
    for part in msg.walk():
        file_name = part.get_filename()  # 获取附件名称
        if file_name is None:
            continue

        # 对附件名称进行解码
        filename = decode_str(file_name)
        # 下载附件
        data = part.get_payload(decode=True)  # 需要使用 decode=True
        if data:
            # 创建目录（如果不存在）
            if not os.path.exists("downloads"):
                os.mkdir("downloads")

            # 保存附件
            file_path = os.path.join("downloads", filename)
            with open(file_path, "wb") as f:
                f.write(data)
            print(f"附件：{filename} 保存成功！")

    if msg.is_multipart():
        # 如果邮件对象是一个MIMEMultipart, get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        for part in parts:
            parser_content(part, indent + 1)  # 递归打印每一个子对象
    else:
        # 解析正文
        content_type = msg.get_content_type()
        if content_type == "text/plain" or content_type == "text/html":
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset and content:
                content_decoded = content.decode(charset)
                print(f"{'  ' * indent}正文内容为: {content_decoded}")


def parser_email_header(msg: email.message.EmailMessage) -> None:
    """
    解析并打印邮件的标题、发件人和收件人信息。

    Args:
        msg: 邮件消息对象。
    """
    # 解析邮件标题
    subject = msg["Subject"]
    value, charset = decode_header(subject)[0]
    if isinstance(value, bytes) and charset:
        value = value.decode(charset)
    print(f"邮件标题： {value}")

    # 解析发送人信息
    hdr, addr = parseaddr(msg["From"])
    name, charset = decode_header(hdr)[0]
    if isinstance(name, bytes) and charset:
        name = name.decode(charset)
    print(f"发送人邮箱名称: {name}，发送人邮箱地址: {addr}")

    # 解析接收人信息
    hdr, addr = parseaddr(msg["To"])
    name, charset = decode_header(hdr)[0]
    if isinstance(name, bytes) and charset:
        name = name.decode(charset)
    print(f"接收人邮箱名称: {name}，接收人邮箱地址: {addr}")


def decode_str(s: str) -> str:
    """
    解码字符串。

    Args:
        s: 待解码的字符串。

    Returns:
        解码后的字符串。
    """
    value, charset = decode_header(s)[0]
    if isinstance(value, bytes) and charset:
        value = value.decode(charset)
    return value


def guess_charset(msg: email.message.EmailMessage) -> str:
    """
    猜测邮件的字符编码。

    Args:
        msg: 邮件消息对象。

    Returns:
        邮件的字符编码。
    """
    # 从msg对象获取编码
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get("Content-Type", "").lower()
        for item in content_type.split(";"):
            item = item.strip()
            if item.startswith("charset"):
                charset = item.split("=")[1]
                break
    return charset


def parse_mail_time(mail_datetime: str) -> datetime:
    """
    解析邮件的时间字符串为 datetime 对象。

    Args:
        mail_datetime: 邮件时间字符串。

    Returns:
        解析后的 datetime 对象。
    """
    GMT_FORMAT = "%a, %d %b %Y %H:%M:%S"
    GMT_FORMAT2 = "%d %b %Y %H:%M:%S"
    index = mail_datetime.find(" +0")
    if index > 0:
        mail_datetime = mail_datetime[:index]  # 去掉+0800
    formats = [GMT_FORMAT, GMT_FORMAT2]
    for ft in formats:
        try:
            mail_datetime_obj = datetime.strptime(mail_datetime, ft)
            return mail_datetime_obj
        except ValueError:
            pass
    raise ValueError("邮件时间格式解析错误")


def receive_email(config: Dict):
    
    pop3_server = config["email"]["pop3_server"]
    email_user = config["email"]["email"]
    email_password = config["email"]["passwd"]
    
    # 连接到 POP3 服务器
    try:
        email_server = poplib.POP3(pop3_server)
        email_server.user(email_user)
        email_server.pass_(email_password)

        # 列出邮件数量
        resp, mails, octets = email_server.list()
        num, total_size = email_server.stat()
        print("邮件数量为：" + str(num))

        # 倒序遍历邮件
        for i in range(len(mails), 0, -1):
            # 获取邮件
            resp, lines, octets = email_server.retr(i)
            msg_content = b"\r\n".join(lines).decode("utf-8")
            msg = Parser().parsestr(msg_content)

            # 解析邮件时间
            mail_datetime = parse_mail_time(msg.get("date"))
            max_mail_time_str = arrow.get(mail_datetime).format("YYYY-MM-DD HH:mm")
            print("邮件接收时间为：" + max_mail_time_str)

            # 解析邮件具体内容，包括正文，标题，和附件
            parser_content(msg, 0)

        # 退出
        email_server.quit()

    except Exception as e:
        print(f"获取邮件时出错: {e}")
