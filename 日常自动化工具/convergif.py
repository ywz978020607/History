# gif 制作 - 支持透明通道
from PIL import Image
import glob, os
outfilename = "my.gif" # 转化的GIF图片名称

path = "动图透明分列" #"动图(1)"
filenames = sorted(glob.glob(os.path.join(path, "*.png")))
print(filenames)

crop_up_left = (47, 160)
crop_down_right = (1293, 1003)
duration = 800 #ms


#####deal#########
frames = []
for image_name in filenames:
    pic_p = Image.open(image_name)
    # print(pic_p.size) #[height, width]
    pic_p.crop((crop_up_left[1],crop_up_left[0],crop_down_right[1],crop_down_right[0]))
    frames.append(pic_p)
#保存图像，disposal可以为2(无重影)或者3(重影残留)，但是不能为1或0，切记，其他自定义未尝试
frames[0].save(outfilename, save_all=True, append_images=frames[1:],duration=duration,transparency=0,loop=0,disposal=2)
