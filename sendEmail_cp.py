import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import poundtoRMB
import time

my_sender = 'xxxxxx@163.com'  # 发件人邮箱账号
my_pass = 'xxxxxxxxxxx'  # 发件人邮箱密码
my_receiver = 'xxxxxxxxxx@qq.com'  # 收件人邮箱账号，我这边发送给自己
cc_receiver = ['xxxxxxxx@outlook.com']


def mail():
	ret = True
	try:
		msg = MIMEText('目前汇率为 ' + str(standard), 'plain', 'utf-8')
		msg['From'] = formataddr(["MailBot", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
		print(standard)
		msg['To'] = formataddr(["Name", my_receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
		msg['Cc'] = ";".join(cc_receiver)
		msg['Subject'] = "买英镑辽 " + str(standard)  # 邮件的主题，也可以说是标题

		server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
		server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
		server.sendmail(my_sender, [my_receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
		server.quit()  # 关闭连接
	except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
		ret = False
	return ret


while 1:
	standard = poundtoRMB.getnumber()
	if standard < 8.65:
		ret = mail()

		if ret:
			print("邮件发送成功")
		else:
			print("邮件发送失败")
	mail()
	time.sleep(300)
