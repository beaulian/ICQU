# coding=utf-8

import smtplib
from hashlib import md5
from pyDes import *
from email.mime.text import MIMEText

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def send_mail(content, mail_receiver):
    mail_host = "smtp.qq.com"
    mail_sender = "870402916@qq.com"
    mail_password = s.decrypt("\x94\xc6\xa8\x88\x85\x92\xe5\xdb\x85FO\x96f\xbdlE")
    msg = MIMEText(content,_subtype="plain",_charset="utf-8")
    msg["Subject"] = "新成绩"
    msg["From"] = mail_sender
    msg["To"] = mail_receiver
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_sender,mail_password)
        server.sendmail(mail_sender,mail_receiver,msg.as_string())
        server.close()
    except:
        sys.exit(1)