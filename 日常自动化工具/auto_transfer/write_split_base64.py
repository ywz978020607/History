import os
import json
import base64

filename = input("文件名:")
# filename = 'test.whl'
need_trans_b64 = True #只切分时可设置False
need_split_out = True # 是否需要切分
split_size = 19922944 # 切分大小 - 19MB
# split_size = 50922944

output_path = "output_convert"
with open(filename, 'rb') as f:
    data = f.read()

# bytes->list
print(len(data))

if need_trans_b64:
    write_str = (base64.b64encode(data)).decode()
else:
    write_str = str(data)

# # 测试
# re_data = base64.b64decode(write_str)
# print(len(re_data))

print("out-str-len", len(write_str))

if not need_split_out:
    with open(filename+'.b64.txt', 'w') as f:
        f.write(write_str)
else:
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
            f.write(write_str[write_start:min(write_start+split_size, len(write_str))])
        idx += 1
        write_start += split_size
