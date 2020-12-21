import yaml # pip install pyyaml
import os,glob,sys


def trans(mode='1'): #'0':全部传输 ;; '1'：只传输.py 文件;;
    # print(mode)
    # 用open方法打开直接读取
    f = open('iplist.yml', 'rb')
    cfg = f.read()
    ipdict = yaml.load(cfg)
    # print(ipdict)
    iplist = list(ipdict.keys())
    # iplist = iplist.remove('local')

    local_root = ipdict['local']['root']
    local_append_path = ipdict['local']['temp']
    local_path = local_root
    if local_append_path!=None:
        local_path = os.path.join(local_root,local_append_path)
    print(iplist)
    print(local_path)

    for ii in range(len(iplist)):
        if iplist[ii]=='local':
            continue
        temp_user = ipdict[iplist[ii]]["user"]
        temp_port = ipdict[iplist[ii]]["port"]
        temp_ip = ipdict[iplist[ii]]["ip"]
        temp_remote_root =ipdict[iplist[ii]]["root"]
        temp_remote_path = temp_remote_root
        if local_append_path!=None:
            temp_remote_path = os.path.join(temp_remote_root,local_append_path)

        #最后的名字相同，因为是文件夹，则取消remote_path的名字，留出/表示，否则会自动补/
        if os.path.basename(temp_remote_path)==os.path.basename(local_path):
            temp_remote_path = os.path.dirname(temp_remote_path)
        temp_remote_path = os.path.join(temp_remote_path,"")
        print(temp_remote_path)

        ####
        #开始同步
        if mode=='0': #直接递归同步
            p = os.popen("scp -P "+temp_port+" -r "+local_path+" "+temp_user+"@"+temp_ip+":"+temp_remote_path)
            print(p.read())

        elif mode=='1': #只同步.py文件
            pass


if __name__=="__main__":
    mode = '0'
    if len(sys.argv) < 2:
        pass
    else:
        mode = str(sys.argv[1])
    trans(mode)



