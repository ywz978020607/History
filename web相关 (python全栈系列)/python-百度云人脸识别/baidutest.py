#百度云人脸库管理测试
import requests
import json
import base64
#tobase64
def tob64(filename):
    with open(filename, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s
        # print('data:image/jpeg;base64,%s' % s)


# #获取token
# # client_id 为官网获取的AK， client_secret 为官网获取的SK
# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=RL9d67Tudouxs6fzb9PhZdIX&client_secret=3B38YF0n40WKLVo9LnXynE9mGhc8zIuB'
# response = requests.get(host)
# if response:
#     print(response.json())
# #'24.a0dd4855acc372c618154c4bb71541ad.2592000.1619051582.282335-23845754'
access_token = '24.a0dd4855acc372c618154c4bb71541ad.2592000.1619051582.282335-23845754'

'''
获取用户列表
'''
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers"

params = "{\"group_id\":\"g1\"}"
# access_token = '24.a0dd4855acc372c618154c4bb71541ad.2592000.1619051582.282335-23845754'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())



# '''
# 人脸注册
# '''
# file = "../test2.jpg"
# image = tob64(file)
# imageType = "BASE64"
#
# request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
#
# params = "{\"image\":\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"group_id\":\"g1\",\"user_id\":\"c2\"}"
# params = json.loads(params)
# params["image"] = image
# params["image_type"] = imageType
# params = json.dumps(params)
#
#
# access_token = '24.a0dd4855acc372c618154c4bb71541ad.2592000.1619051582.282335-23845754'
# request_url = request_url + "?access_token=" + access_token
# headers = {'content-type': 'application/json'}
# response = requests.post(request_url, data=params, headers=headers)
# if response:
#     print (response.json())


# """
# 人脸删除 先获取人脸列表拿到face_token再删除
# """
# request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist"
#
# params = "{\"group_id\":\"g1\"}"
# params = json.loads(params)
# params["user_id"] = "c2"
# params = json.dumps(params)
#
# request_url = request_url + "?access_token=" + access_token
# headers = {'content-type': 'application/json'}
# response = requests.post(request_url, data=params, headers=headers)
# if response:
#     print (response.json())
#
# request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete"
#
# params = json.loads(params)
# params["face_token"]  = response.json()['result']['face_list'][0]['face_token']
# params = json.dumps(params)
#
# request_url = request_url + "?access_token=" + access_token
# headers = {'content-type': 'application/json'}
# response = requests.post(request_url, data=params, headers=headers)
# if response:
#     print (response.json())



#============================================
"""
人脸检测
"""
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"


params = "{\"image\":\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"face_field\":\"faceshape,facetype\"}"
file = "../test1.jpg"
image = tob64(file)
imageType = "BASE64"

params = json.loads(params)
params["image"] = image
params["image_type"] = imageType
params = json.dumps(params)

# access_token = '[调用鉴权接口获取的token]'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())
    loc = response.json()['result']['face_list'][0]['location']  # 'left','top','width','height'
    x = int(loc['left'])
    y = int(loc['top'])
    w = int(loc['width'])
    h = int(loc['height'])
    # img = cv2.imread(file)
    # img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # cv2.imwrite("new.jpg", img)


""" 调用人脸搜索 """
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
params = "{\"image\":\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"face_field\":\"faceshape,facetype\"}"
file = "../test1.jpg"
image = tob64(file)
imageType = "BASE64"

params = json.loads(params)
params["image"] = image
params["image_type"] = imageType
params["group_id_list"] = "g1"
params = json.dumps(params)

# access_token = '[调用鉴权接口获取的token]'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())
    print(response.json()['result']['user_list'][0]['user_id'])

