# gif 制作 不支持透明通道

import imageio
import glob, os
outfilename = "my.gif" # 转化的GIF图片名称

path = "动图(1)"
filenames = sorted(glob.glob(os.path.join(path, "*.png")))
print(filenames)

crop_up_left = (47, 160)
crop_down_right = (1293, 1003)

frames = []
for image_name in filenames:
    im = imageio.imread(image_name)
    # print(im.shape) #[height, width, channel]
    im = im[crop_up_left[0]:crop_down_right[0], crop_up_left[1]:crop_down_right[1]]
    frames.append(im)
imageio.mimsave(outfilename, frames, 'GIF', duration=0.8) 


