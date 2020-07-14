#下载北航云盘的文件
import sys
import os
url = sys.argv[1]
name = sys.argv[2]
os.system("wget -c '"+url+"' -O "+name)

# def down(url,name):
#     os.system("wget -c '"+url+"' -O "+name)




#eg: python bhpan.py 'https://p300s.buaa.edu.cn:10002/bhpan_bucket/7f451e0dxxxx'  test.rar

