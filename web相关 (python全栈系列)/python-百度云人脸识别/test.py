import json
import base64

# appid 23784177
# key P1w3CYe4aw50coECX0GKLyCe
# secret Q26QoCTAVVruHA4Ijxejbr7XT3FP7YTo

from aip import AipFace
import cv2

#tobase64
def tob64(filename):
    with open(filename, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s
        # print('data:image/jpeg;base64,%s' % s)



""" 你的 APPID AK SK """
APP_ID = '23784177'
API_KEY = 'P1w3CYe4aw50coECX0GKLyCe'
SECRET_KEY = 'Q26QoCTAVVruHA4Ijxejbr7XT3FP7YTo'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


# image = "取决于image_type参数，传入BASE64字符串或URL字符串或FACE_TOKEN字符串"
file = "wenzheyang.jpg"
image = tob64(file)
imageType = "BASE64"
""" 调用人脸检测 """
ret1 = client.detect(image, imageType)
loc = ret1['result']['face_list'][0]['location'] #'left','top','width','height'
x = int(loc['left'])
y = int(loc['top'])
w = int(loc['width'])
h = int(loc['height'])
img = cv2.imread(file)
img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
cv2.imwrite("new.jpg",img)

# ==========
# 人脸搜索
groupIdList = "g1"

""" 调用人脸搜索 """
ret2 = client.search(image, imageType, groupIdList)
finduser = ret2['result']['user_list'][0]['user_id']
print(finduser)

print("ok")