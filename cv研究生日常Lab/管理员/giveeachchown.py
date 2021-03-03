import os,glob

root = "/home"
all_list = sorted(glob.glob(os.path.join(root,"*")))
for ii in range(len(all_list)):
    temp = all_list[ii]
    print("sudo chown "+temp+":"+temp+" "+os.path.join(root,temp)+"/")
    # os.system("sudo chown "+temp+":"+temp+" "+os.path.join(root,temp)+"/")

