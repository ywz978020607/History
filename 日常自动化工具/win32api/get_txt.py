import win32gui,win32api,win32con




# 获得父容器
pHwnd = win32gui.FindWindow('WTWindow', '验证码识别')

# 获取子容器,识别结果输入框
edtextHwnd = win32gui.FindWindowEx(pHwnd, None, 'Edit', '')
 
buf_size = win32gui.SendMessage(edtextHwnd, win32con.WM_GETTEXTLENGTH, 0, 0) + 1  # 要加上截尾的字节
str_buffer = win32gui.PyMakeBuffer(buf_size)  # 生成buffer对象
win32api.SendMessage(edtextHwnd, win32con.WM_GETTEXT, buf_size, str_buffer)  # 获取buffer
print(str_buffer[:-1])
str = str(str_buffer[:-1])  # 转为字符串
result = str
print(result)
##########################

# 获取识别结果中输入框文本
length = win32gui.SendMessage(edtextHwnd, win32con.WM_GETTEXTLENGTH)+1
buf = win32gui.PyMakeBuffer(length)
#发送获取文本请求
win32api.SendMessage(edtextHwnd, win32con.WM_GETTEXT, length, buf)
#下面应该是将内存读取文本
address, length = win32gui.PyGetBufferAddressAndLen(buf[:-1])
text = win32gui.PyGetString(address, length)

