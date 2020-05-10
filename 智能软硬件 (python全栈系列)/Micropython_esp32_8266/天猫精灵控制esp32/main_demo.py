import mywifi,bigconn 

#连接wifi并自检保持连接
m = mywifi.WIFI(SSID='ywzywz',PASS='12345678',check=1)

#连接贝壳物联并自检保持连接,自动执行recv的函数并打印内容,(见bigconn.py)
big = bigconn.mybig(ID = "12617",API_KEY = "eca35b8e9",check=1)

