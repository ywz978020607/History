import os
import json
import base64

filename = input("文件名:")

need_merge = True

read_str = ''

if need_merge:
    output_path = "output_convert"
    exists_files = os.listdir(output_path)
    for file in exists_files:
        if file.endswith(".py") or file.endswith(".txt"):
            with open(output_path+"/"+file, 'r', encoding='utf-8') as f:
                read_str += f.read()
else:
    with open(filename, 'r', encoding='utf-8') as f:
        read_str = f.read()

print("len-read_str:", len(read_str))
re_data = base64.b64decode(read_str.encode())
print(len(re_data))

with open(filename.split(".b64.txt")[0], "wb") as f:
    f.write(re_data)

​
