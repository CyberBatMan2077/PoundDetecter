import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import poundtoRMB
import time
from random import randint

my_sender = 'xxxxxxxx@163.com'  # 发件人邮箱账号
my_pass = 'xxxxxxxxxxx'  # 发件人邮箱密码
my_receiver = 'xxxxxxxx@qq.com'  # 收件人邮箱账号，我这边发送给自己
# 抄送邮箱
cc_receiver = [
	'xxxxxxxx@163.com',
	'xxxxxxx@qq.com',
	'xxxxxxxx@163.com',
	'xxxxxxxxx@gmail.com'
]
# 实际所有收件人
recipients = cc_receiver
recipients.append(my_receiver)
print(recipients)


def mail(msgtext, theme):
	ret = True
	try:
		msg = MIMEText(msgtext, 'plain', 'utf-8')
		msg['From'] = formataddr(["xxxx", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
		msg['To'] = formataddr(["xxxxx", my_receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
		msg['Cc'] = ";".join(cc_receiver)
		msg['Subject'] = theme  # 邮件的主题，也可以说是标题

		server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
		server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
		server.sendmail(my_sender, recipients, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
		server.quit()  # 关闭连接
	except ValueError:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
		ret = False
		print("ERROR")
	return ret


def write_log(status, rate):
	with open("running.log", 'a+') as f:
		time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		if status:
			f.write("\nSuccess: " + str(rate) + "\t")
			f.write("\n" + time_stamp)
		else:
			f.write("\nFailed: " + str(rate) + "\t")
			f.write("\n" + time_stamp)


def random_delay():
	delay_time = randint(60, 120) * 5
	time.sleep(delay_time)


def start_service():
	sent_flag = 0
	counter = 0
	last_rate = poundtoRMB.getnumber()
	basic_detect_rate = 8.63
	first_msg = '汇率小助手开始工作，通知汇率为:' + str(basic_detect_rate)
	first_theme = '开始工作辽，目前汇率为:' + str(last_rate)
	#	mail(first_msg, first_theme)

	while 1:
		standard = poundtoRMB.getnumber()
		if standard is not None:
			write_log(1, standard)
			print("Getting the latest data")
		if standard is None:
			print("Fail in getting the latest data")
			standard = last_rate
			write_log(0, standard)
		print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
		print("data for monitoring is now " + str(standard))

		if basic_detect_rate - standard >= 0.035:
			sent_flag = 0
		print(basic_detect_rate - standard)
		if standard < basic_detect_rate:
			msgtext = '目前汇率为' + str(standard)
			theme = '买英镑辽' + str(standard)
			if sent_flag == 0:
				ret = mail(msgtext, theme)
				sent_flag = 1
			else:
				ret = 0

			if ret:
				print("邮件发送成功")
			elif sent_flag == 1	and ret == 0:
				print("邮件发送失败,之前已发送过邮件，处于冷却中")
			else:
				print("邮件发送失败")

		random_delay()
		if sent_flag == 1:
			counter += 1
		if counter == 100:
			counter = 0
			if sent_flag != 0:
				sent_flag = 0
		print("flag: " + str(sent_flag))
		print("counter: " + str(counter))

start_service()
