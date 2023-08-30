## read
import os
import json

filename = input("文件名:")
# filename = 'test.whl'

output_path = "output_convert"
read_str = ''
exists_files = os.listdir(output_path)
for file in exists_files:
    with open(output_path+"/"+file, 'r', encoding='utf-8') as f:
        read_str += f.read()
print("len-read_str:", len(read_str))
re_data_list = read_str.split(",")
re_data_list= [int(re_data_list[ii],16) for ii in range(len(re_data_list))]
re_data = bytes(re_data_list)
print(len(re_data))

with open(filename, 'wb') as f:
    f.write(re_data)
