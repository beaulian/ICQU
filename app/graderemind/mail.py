# coding=utf-8

import smtplib
from email.mime.text import MIMEText

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def send_mail(content, mail_receiver, mail_password):
    mail_host = "smtp.qq.com"
    # mail_port = 465
    mail_sender = "870402916@qq.com"
    msg = MIMEText(content,_subtype="plain",_charset="utf-8")
    msg["Subject"] = "新成绩"
    msg["From"] = mail_sender
    msg["To"] = mail_receiver
    
    server = smtplib.SMTP()
    server.connect(mail_host)
    server.starttls()
    server.login(mail_sender,mail_password)
    server.sendmail(mail_sender,mail_receiver,msg.as_string())
    server.close()