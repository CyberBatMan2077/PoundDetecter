from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def getnumber():
	try:
		html = urlopen("http://www.baidu.com/s?ie=UTF-8&wd=%E8%8B%B1%E9%95%91%E6%B1%87%E7%8E%87",timeout=60)
		bsObj = BeautifulSoup(html, "html.parser")
		# tables = bsObj.findAll("script", {"data-compress": {"off"}})
		data = bsObj.find("div", {"class": {"op_exrate_result"}})
		number = re.findall(r"[1-9]+\.+[0-9]+", data.get_text())

	except Exception as e:
		number = None

	if number is not None:
		print(data.get_text())
		standard = float(number[0])
	else:
		standard = None

	return standard
