from selenium import webdriver
import time
driver = webdriver.Chrome()

while 1:
    driver.get('https://www.bilibili.com/video/BV1ri4y137MP/')
    time.sleep(3)
    driver.find_element_by_id("bilibiliPlayer").click()
    time.sleep(27) #视频播放时间
