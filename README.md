# e2me

[![PyPI download month](https://img.shields.io/pypi/dm/e2me.svg)](https://pypi.python.org/pypi/e2me/)
[![PyPI version fury.io](https://badge.fury.io/py/e2me.svg)](https://pypi.python.org/pypi/e2me/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/e2me.svg)](https://pypi.python.org/pypi/e2me/)

不知道什么时候跑完程序? 发一封邮件吧

```bash
pip install e2me
```

视频介绍: [【e2me】不知道什么时候跑完程序?发一封邮件吧](https://www.bilibili.com/video/BV1TstPenECo)

## 快速开始

初次使用需要配置文件, 通过 e2me init 自动生成 `e2me.toml`, 如下所示 

```toml
[email]
email = "your-email@example.com"
passwd = "xxx"

cc = [""]
```

email 改为您的邮箱地址即可，密码为邮箱的 SMTP 密码

> 如果需要可以填写 cc 抄送对象

### 获取 SMTP 密码

**注意这里的密码并不是邮箱的登录密码**, **注意这里的密码并不是邮箱的登录密码**, **注意这里的密码并不是邮箱的登录密码**, 而是需要开启邮箱的 SMTP/POP3 服务后**分配给你的密码**

本项目目前支持 163/qq/gmail, 请请参考下述链接开启邮箱的 SMTP/POP3 服务并配置好自己的邮箱和密码

- [如何使用163的SMTP服务发邮件?](https://blog.csdn.net/liuyuinsdu/article/details/113878840)
- [如何开启QQ邮件的SMTP服务](https://blog.csdn.net/qq_42076902/article/details/131900459)
- [谷歌Gmail邮箱开启SMTP/IMAP服务流程](https://www.cnblogs.com/jiyuwu/p/16313476.html)

> 扫描二维码发送短信失败可以手动编辑短信

### 保存配置

修改完 email 和 passwd 信息之后可以将该信息保存到全局

```bash
e2me -s
```

此选项将使用当前目录的 e2me.toml 覆盖全局配置信息, 此后可以在所有目录下直接使用 `e2me run` 发送邮件

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

### Python API

如果您想在程序中发送邮件也非常方便

```python
import e2me
e2me.send_email()
e2me.send_email(subject = "hello", body = "world")
```

### 环境变量

在一些特殊情况下可能不想要生成 e2me.toml 配置，您也可以设置环境变量 `E2ME_EMAIL` 和 `E2ME_PASSWD` 来验证身份

```bash
export E2ME_EMAIL=abc@163.com
export E2ME_PASSWD=xxx
```

以及配置 E2ME_CC 来添加抄送者

```bash
export E2ME_CC="abc@163.com,xxx@qq.com"
```

### 接收邮件

```bash
$ e2me get
create WANGYI163 email server for [luzhixing12345@163.com]...
获取最近 5 封邮件
[0]: [2026-03-26 21:53] 程序运行结束 [luzhixing12345@163.com]
[1]: [2026-03-26 21:26] 程序运行结束 [luzhixing12345@163.com]
[2]: [2026-03-26 08:00] Paper Notifier: HPCA [2026] 0 Papers [e2me_free@163.com]
[3]: [2026-03-25 19:33] Important Update to GitHub Copilot Interaction Data Usage Policy [no-reply@github.com]
[4]: [2026-03-24 13:17] Overleaf thoughts [welcome@overleaf.com]
```

### Q&A

- 为什么是自己给自己发送邮件？
  
  理论上来说只需要注册一个公共邮箱账号负责发送，并硬编码该邮箱的smtp密钥，然后给自己的邮箱发送邮件即可。但是这种方式很容易被各大邮箱和谐，ip登录不统一等等问题，作为一个公共库这种做法会有很大问题

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