# e2me

不知道什么时候跑完程序? 发一封邮件吧

```bash
pip install e2me
```

视频介绍: [【e2me】不知道什么时候跑完程序?发一封邮件吧](https://www.bilibili.com/video/BV1TstPenECo)

## 快速开始

需要在运行程序的服务器端编写一个配置文件, 可以通过 e2me init 自动生成 `e2me.toml`, 如下所示 

```toml
[email]
email = "your_email@example.com"
passwd = "your_password"

[content]
subject = "程序运行结束"
body = "[<DATE> | <TIME>] [<KERNEL>] <USER>:<HOSTNAME> "

# [file]
# file_path = ["result.log"]
```

其中 email 改为您的邮箱地址, **注意这里的密码并不是邮箱的登录密码**, **注意这里的密码并不是邮箱的登录密码**, **注意这里的密码并不是邮箱的登录密码**, 而是需要开启邮箱的 SMTP/POP3 服务后**分配给你的密码**

本项目目前支持 163/qq/gmail, 请请参考下述链接开启邮箱的 SMTP/POP3 服务并配置好自己的邮箱和密码

- [如何使用163的SMTP服务发邮件?](https://blog.csdn.net/liuyuinsdu/article/details/113878840)
- [如何开启QQ邮件的SMTP服务](https://blog.csdn.net/qq_42076902/article/details/131900459)
- [谷歌Gmail邮箱开启SMTP/IMAP服务流程](https://www.cnblogs.com/jiyuwu/p/16313476.html)

> 扫描二维码发送短信失败可以手动编辑短信

### 保存配置

修改完 email 和 passwd 信息之后可以使用 e2me 将该信息保存到全局

```bash
e2me -s
```

此选项将使用当前目录的 e2me.toml 覆盖全局配置信息, 此后可以在所有目录下直接使用 e2me run 发送邮件

### 发送邮件

```bash
e2me run
```

配置信息中 subject 为邮件标题, body 为邮件正文内容, 默认提供了 5 个基本宏用于系统信息的记录, 您可以按照喜好修改对应的文字内容

```toml
[content]
subject = "程序运行结束"
body = "[<DATE> | <TIME>] [<KERNEL>] <USER>:<HOSTNAME> "
```

您希望可以动态调整标题和正文内容, 可以使用 `--subject` 修改默认邮件标题, `--body` 修改默认邮件正文内容, 例如

```bash
e2me run --subject "llm project A finished" --body "epoch 1"
```

如果您同时希望将一些结果图片/文件/日志发送, 可以启用 [file] 并填写文件位置, 它们将会被一起发送到邮箱

```toml
[file]
file_path = ["result.log"]
```

您可以编写一个执行脚本, 并在最后一行执行

```bash
#!/bin/bash
python main.py
./myprogram

e2me run
```

对于 python 程序您也可以直接使用该库发送邮件

```python
import e2me

def main():
    # do something

    # finish
    e2me.run()
    # e2me.run("llm project finsihed", "epoch 1")
```

### 接收邮件

```bash
e2me get
```

## 邮箱基本信息

```txt
# 协议  服务器         SSL    非 SSL
# SMTP smtp.163.com   465    25
# IMAP imap.163.com   993    143
# POP3 pop.163.com    995    110
# -------------------------------
# SMTP smtp.qq.com    465/587
# IMAP imap.qq.com    993
# POP3 pop.qq.com     995
# -------------------------------
# SMTP smtp.gmail.com 465(SSL)/587(TLS/STARTTLS)
# IMAP imap.gmail.com 993
# POP3 pop.gmail.com  995
# -------------------------------
# 163/qq: password 为授权码
# gmail: password 为 Google 授权密码
```

## 参考

- [foofish python-re-email](https://foofish.net/python-re-email.html#google_vignette)