#下载北航云盘的文件
import sys
import os
argv_len = len(sys.argv)
if argv_len==3:
    url = sys.argv[1]
    name = sys.argv[2]
else:
    url = input("downloads_url:")
    name = input("filename_to_save:")
os.system("wget -c '"+url+"' --header 'Cookie:allow-download=1' -O "+name)

#eg: python bhpan.py 'https://p300s.buaa.edu.cn:10002/bhpan_bucket/7f451e0dxxxx'  test.rar
#    or
#    python bhpan.py



