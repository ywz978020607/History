import os
import json

filename = input("文件名:")
# filename = 'test.whl'

output_path = "output_convert"
with open(filename, 'rb') as f:
    data = f.read()

# bytes->list
print(len(data))
data_list = []
for ii in range(len(data)):
    data_list.append(str(hex(int(data[ii]))[2:]))
assert len(data) == len(data_list)
write_str = ",".join(data_list)
print("len(write_str):",len(write_str))
if os.path.exists(output_path):
    exists_files = os.listdir(output_path)
    for file in exists_files:
        os.remove(output_path+"/"+file)
else:
    os.mkdir(output_path)
idx = 0
write_start = 0
while write_start < len(write_str):
    with open(output_path+"/{}.txt".format(str(idx).zfill(6)), 'w', encoding='utf-8') as f:
        f.write(write_str[write_start:min(write_start+19922944, len(write_str))])
    idx += 1
    write_start += 19922944
