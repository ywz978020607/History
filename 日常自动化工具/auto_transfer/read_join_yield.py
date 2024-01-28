## read
​import os
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
###
# re_data_list = read_str.split(",")
# re_data_list = [int(re_data_list[ii], 16) for ii in range(len(re_data_list))]
###
re_data_list = [0] * (read_str.count(",")+1)
# re_data_list = []

def custom_split(input_str, delimiter):
    start = 0
    while start < len(input_str):
        end = input_str.find(delimiter, start)
        if end == -1:
            yield input_str[start:]
            break
        yield input_str[start:end]
        start = end + len(delimiter)
# 使用方法： for part in custom_split("your_large_string", "your_delimiter"): # 处理每个分割后的子字符串
idx = 0
for part in custom_split(read_str, ","):
    # re_data_list.append(int(part, 16))
    re_data_list[idx] = (int(part, 16))
    idx += 1


###
re_data = bytes(re_data_list)
print(len(re_data))

with open(filename, 'wb') as f:
    f.write(re_data)
