import yaml # pip install pyyaml
import os,glob,sys


def trans(mode): #'0':全部传输 ;; '1'：只传输.py 文件;;
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
        print(iplist[ii])

        temp_user = ipdict[iplist[ii]]["user"]
        temp_passwd = ipdict[iplist[ii]]["passwd"]
        temp_port = ipdict[iplist[ii]]["port"]
        temp_ip = ipdict[iplist[ii]]["ip"]
        temp_remote_root =ipdict[iplist[ii]]["root"]
        temp_remote_path = temp_remote_root
        if local_append_path!=None:
            temp_remote_path = os.path.join(temp_remote_root,local_append_path)

        ####
        #开始同步
        if mode=='0': #直接递归同步 文件夹传输

            #最后的名字相同，因为是文件夹，则取消remote_path的名字，留出/表示，否则会自动补/
            if os.path.basename(temp_remote_path)==os.path.basename(local_path):
                temp_remote_path = os.path.dirname(temp_remote_path)
            temp_remote_path = os.path.join(temp_remote_path,"")
            print(temp_remote_path)

            print("sshpass -p "+ temp_passwd +" scp -P "+temp_port +" -r "+local_path+" "+temp_user+"@"+temp_ip+":"+temp_remote_path)
            os.system("sshpass -p "+ temp_passwd +" scp -P "+temp_port +" -r "+local_path+" "+temp_user+"@"+temp_ip+":"+temp_remote_path)


        elif mode=='1': #只同步.py文件
            #先列出所有文件
            temp_all_file_list = []
            for root, dirs, files in os.walk(local_path):
                for file in files:
                    if ".py" in file: #后缀.py
                        temp_all_file_list.append(os.path.join(root, file))
            # print(temp_all_file_list)
            for jj in range(len(temp_all_file_list)):
                local_file_path = temp_all_file_list[jj]
                temp_remote_file_path = local_file_path.replace(local_path,temp_remote_path)
                # print(local_file_path)
                print(temp_remote_file_path)
                # print(
                #     "scp -P " + temp_port + " " + local_file_path + " " + temp_user + "@" + temp_ip + ":" + temp_remote_file_path)
                os.system(
                    "sshpass -p "+ temp_passwd +" scp -P " + temp_port + " " + local_file_path + " " + temp_user + "@" + temp_ip + ":" + temp_remote_file_path)
                # print(p.read()) #搭配os.popen()

if __name__=="__main__":
    mode = '0'
    if len(sys.argv) < 2:
        pass
    else:
        mode = str(sys.argv[1])
    trans(mode)



