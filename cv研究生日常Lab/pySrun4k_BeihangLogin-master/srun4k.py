import password
import requests
from requests.packages import urllib3

# 关闭SSL验证警告
urllib3.disable_warnings()

class pySrun4kError(Exception):
	def __init__(self,reason):
		Exception.__init__(self)
		self.reason = reason

def do_login(url,username,pwd,mbytes=0,minutes=0):
	pwd = password.encrypt(pwd)
	payload = {
		'action':'login',
		'username':username,
		'password':pwd,
		'drop':0,
		'pop':0,
		'type':2,
		'n':117,
		'mbytes':0,
		'minutes':0,
		'ac_id':1
	}
	header = {
		'user-agent':'pySrun4k'
	}
	r = requests.post(url + "/cgi-bin/srun_portal",data=payload,headers=header,verify=False)
	if ('login_error' in r.text):
		ret = {
			'success':False,
			'code':int(r.text[13:17]),
			'reason':r.text[19:]
		}
		return ret;
	elif ('login_ok' in r.text):
		ret = {
			'success':True,
			'data':r.text.split(',')[1:]
		}
		return ret;
	else:
		raise pySrun4kError(r.text)


def check_online(url):
	header = {
		'user-agent':'pySrun4k'
	}
	r = requests.get(url + "/cgi-bin/rad_user_info", headers=header, verify=False)
	if ('not_online' in r.text):
		ret = {
			'online':False
		}
		return ret
	else:
		raw = r.text.split(',')
		ret = {
			'online':True,
			'username':raw[0],
			'login_time':raw[1],
			'now_time':raw[2],
			'used_bytes':raw[6],
			'used_second':raw[7],
			'ip':raw[8],
			'balance':raw[11],
			'auth_server_version':raw[21]
		}
		return ret


def do_logout(url,username):
	header = {
		'user-agent':'pySrun4k'
	}
	payload = {
		'action':'logout',
		'ac_id':1,
		'username':username, #这参数好像没啥用,不过好像不传又不行.
		'type':2
	}
	r = requests.post(url + "/cgi-bin/cgi-bin/srun_portal",
	                  data=payload, headers=header, verify=False)
	if ('logout_ok' in r.text):
		ret = {
			'success':True,
		}
		return ret;
	elif ('login_error' in r.text):
		ret = {
			'success':False,
			'reason':r.text.split('#')[1]
		}
		return ret
	else:
		raise pySrun4kError(r.text)


def force_logout(url,username, pwd):
	payload = {
		'action':'logout',
		'username':username,
		'password':pwd,
		'drop':0,
		'type':1,
		'n':117,
		'ac_id':1
	}
	header = {
		'user-agent':'pySrun4k'
	}
	r = requests.post(url + "/cgi-bin/cgi-bin/srun_portal",
	                  data=payload, headers=header, verify=False)
	if ('logout_ok' in r.text):
		ret = {
			'success':True
		}
		return ret
	elif ('login_error' in r.text):
		ret = {
			'success':False,
			'reason':r.text.split('#')[1]
		}
		return ret
	else:
		raise pySrun4kError(r.text)
