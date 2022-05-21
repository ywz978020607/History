# gif 制作 - 支持透明通道
from tkinter import Image
import PIL
import glob, os
import numpy as np
from transparent_gif import save_transparent_gif
outfilename = "my.gif" # 转化的GIF图片名称
duration = 800 #ms

path = "动图透明分列" #"动图(1)"
filenames = sorted(glob.glob(os.path.join(path, "*.png")))
print(filenames)

#####cut picture##
def cut_pic(pic_p):
    # print(pic_p.size)
    # crop_up_left = (47, 160)
    # crop_down_right = (1293, 1003)
    # pic_p.crop((crop_up_left[1],crop_up_left[0],crop_down_right[1],crop_down_right[0]))
    return pic_p

def cut_frames(frames):
    # img = np.array(img)
    # img_tr = Image.fromarray(tr_img)
    img_size = [1126, 328] #width, height
    length = len(frames)
    for idx in range(length):
        img = frames[idx]
    # for idx, img in enumerate(frames):
        # if idx == 0:
        #     print(img.size) #(1126, 328)
        if img.size[0] > img_size[0] or img.size[1] > img_size[1]:
            img_arr = np.array(img)
            # print(img_arr.shape) #(346, 1126, 4)
            img_arr = img_arr[img_arr.shape[0] - img_size[1]:img_arr.shape[0]][img_arr.shape[1] - img_size[0]:img_arr.shape[1]]
            img = PIL.Image.fromarray(img_arr)
            frames[idx] = img
    return frames

#####deal#########
if __name__ == "__main__":
    frames = []
    for image_name in filenames:
        pic_p = PIL.Image.open(image_name)
        # pic_p = cut_pic(pic_p)
        frames.append(pic_p)
    frames = cut_frames(frames)
    #保存图像，disposal可以为2(无重影)或者3(重影残留)，但是不能为1或0，切记，其他自定义未尝试
    # frames[0].save(outfilename,save_all=True, append_images=frames[1:],duration=duration,transparency=0,loop=0,disposal=2)
    save_transparent_gif(frames,duration,save_file=outfilename)