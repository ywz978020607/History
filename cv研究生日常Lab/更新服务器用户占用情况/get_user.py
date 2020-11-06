import os
import time
import psutil

file_name = '/var/www/html/status.txt'

def task1():
    

    out_cpu = psutil.cpu_percent(1)
    out_mem = psutil.virtual_memory().percent
    
    p = os.popen('nvidia-smi')

    out = p.read()
    all_lines = out.split('\n')
    all_data = {}
    gpu_data = []

    flag1 = False
    for ii in range(len(all_lines)):
        if 'Default' in all_lines[ii]:
            gpu_data.append([all_lines[ii-1].split('|')[1].strip().split(' ')[0],all_lines[ii].split('|')[2].strip()])

        if ii>2 and 'Process name' in  all_lines[ii-1]:
            flag1 = True
            continue

        if flag1:
            if '------' in all_lines[ii]:
                break
            elif 'C' in all_lines[ii]:
                temp_data = all_lines[ii].split(' ')
                temp_user = []
                for kk in range(len(temp_data)):
                    if temp_data[kk]!='|' and temp_data[kk]!='':
                        temp_user.append(temp_data[kk])
                #获取用户名
                p = os.popen('ps -f -p '+str(temp_user[-4]))
                out = p.read().split('\n')[1].split(' ')[0]

                if temp_user[0] in all_data.keys():
                    if out in all_data[temp_user[0]].keys():
                        all_data[temp_user[0]][out] += (int)(temp_user[-1].split('M')[0])
                    else:
                        all_data[temp_user[0]][out] = (int)(temp_user[-1].split('M')[0])
                else:
                    all_data[temp_user[0]] = {}
                    all_data[temp_user[0]][out] = (int)(temp_user[-1].split('M')[0])

                # all_data.append([temp_user[0],out,temp_user[-1]])

    # print(all_data)
    # print(gpu_data)

    #write
    f= open(file_name,'w')
    f.write(str(time.asctime( time.localtime(time.time()) ))+"\n")
    f.write("============================\n")
    f.write("Server Name:\t509\n")
    f.write("============================\n")
    f.write("CPU:"+str(out_cpu)+"%\tMEM:"+str(out_mem)+"%\n")
    f.write("============================\n")
    
    for ii in range(len(gpu_data)):
        for jj in range(len(gpu_data[ii])):
            if jj!=0:
                f.write('\t')
            f.write(gpu_data[ii][jj])
        f.write('\n')
    f.write("============================\n")
    f.write("============================\n")
    keys1 = list(all_data.keys())
    for ii in range(len(keys1)):
        f.write(keys1[ii]+":\n")
        keys2 = list(all_data[keys1[ii]])
        for jj in range(len(keys2)):
            f.write('\t'+keys2[jj]+"--"+str(all_data[keys1[ii]][keys2[jj]])+"MiB\n")
        f.write("----------------------------\n")
    f.close()


############
while 1:
    task1()
    time.sleep(60)