# 命令行中的复制

```
ctrl+shift+v
```

- tmux版

  按住shift，自动选中复制，取消时：鼠标拖拽其他位置

  

# ipynb转py脚本：

jupyter nbconvert --to script *.ipynb



# 加载图像

- pytorch版

```
img = Image.open('xxx.png').convert('RGB')
x = transforms.ToTensor()(img).unsqueeze(0)
```

- [https://blog.csdn.net/qq_36955294/article/details/82888443](https://blog.csdn.net/qq_36955294/article/details/82888443)

- https://blog.csdn.net/aLWX_hust/article/details/86591783?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param

  ```
  import torch
  import cv2
  from PIL import Image
  from torchvision import transforms
  image = cv2.imread('myimage.jpg')  # numpy数组格式（H，W，C=3），通道顺序（B,G,R)
  image2 = Image.open('myimage.jpg')  # PIL的JpegImageFile格式(size=(W，H))
  print(image.shape)  # (H，W，3）
  print(image2.size)  # (W，H）
  tran = transforms.ToTensor()  # 将numpy数组或PIL.Image读的图片转换成(C,H, W)的Tensor格式且/255归一化到[0,1.0]之间
  img_tensor = tran(image)
  img2_tensor = tran(image2)
  print(img_tensor.size())  # (C,H, W), 通道顺序（B,G,R)
  print(img2_tensor.size())  # (C，H, W), 通道顺序（R,G,B)
  ```

- 

# 保存图像

- pytorch版

```
reimage = x_hat.cpu().clone()
reimage = reimage.squeeze(0)
reimage = transforms.ToPILImage()(reimage) #PIL格式
reimage.save(out_path)
```



# psnr

```
def compute_psnr(a, b):
    mse = torch.mean((a - b)**2).item()
    return -10 * math.log10(mse)
```