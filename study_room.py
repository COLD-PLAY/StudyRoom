import requests, time, json, smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import smtplib
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header

__author__ = "liaozhou"

# 说明: 5楼研修室只有字典中的三个且dev_id无规律，
# 1楼到4楼的都是门牌号增1，其dev_id增4
# 如: GetDevId(105) = GetDevId(101) + (105-101)*4
room_dev_id = [0,  # room_dev_id[floor]表示floor楼层的起始dev_id, room_dev_id[0]置零
100548027, 100547591, 
100547745, 100547951, 
{
	512: 100548015,
	517: 100548007,
	519: 100548019,
}]

def GetDevId(room):
	floor = room // 100
	return room_dev_id[floor][room] if floor == 5 else room_dev_id[floor] + (room-(floor*100+1))*4

start_time, end_time, room = "2019-05-19+21:10", "2019-05-19+22:00", 209

url_login = "https://idas.uestc.edu.cn/authserver/login?service=http://reservelib.uestc.edu.cn/loginall.aspx?page="
url = "http://reservelib.uestc.edu.cn/ClientWeb/pro/ajax/reserve.aspx?\
&dev_id=%s&start=%s&end=%s&act=set_resv" % (GetDevId(room), start_time, end_time)

sid, pw, mail = "2015060103012", "101387", "liaozhou98@qq.com"

def notify(err_code):
	msg = MIMEText('请手动预约，错误代码:%s' % err_code, 'plain', 'utf-8')
	msg['From'] = Header('米西狮子','utf-8')
	msg['To'] = Header('用户','utf-8')
	subject = '预约研修室出现错误'
	msg['Subject'] = Header(subject,'utf-8') 

	sender = 'liaozhou98@qq.com'

	user = 'liaozhou98@qq.com'
	password = 'blrnygevjbhwghhd'

	smtpserver = 'smtp.qq.com'
	receiver = [mail]

	smtp = smtplib.SMTP()
	smtp.connect(smtpserver, 25)
	smtp.login(user, password)
	smtp.sendmail(sender,receiver,msg.as_string())
	smtp.quit()

def func():
	SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
	driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
	wait = WebDriverWait(driver, 10)

	driver.get(url_login)
	username = wait.until(
		EC.presence_of_element_located((By.CSS_SELECTOR, '#username'))
	)
	password = wait.until(
		EC.presence_of_element_located((By.CSS_SELECTOR, '#password'))
	)
	username.send_keys(sid)
	password.send_keys(pw)
	password.send_keys(Keys.RETURN)

	driver.get(url)
	r = json.loads(driver.find_element_by_tag_name("pre").text)["msg"]

	if r != "操作成功！":
		notify(r)

	driver.close()

if __name__ == '__main__':
	s = time.time()
	func()
	e = time.time()
	print(e-s)