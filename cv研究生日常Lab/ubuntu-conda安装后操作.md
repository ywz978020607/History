sh Anaconda.sh 进行安装

=========

vim ~/.bashrc

在最后添加：

export PATH=~/anaconda3/bin:$PATH

source activate

#或是 export PATH=/usr/local/bin:$PATH  #无conda时

重启环境变量：

source ~/.bashrc

```bash
# 激活环境
source activate
```





# 环境导出与导入 迁移机器

激活进入到所要导出的环境中

activate python36  python36为要导出的环境名称

导出环境 到yml文件， 文件名为 python36_20190106.yml

```python
conda env export --file python36_20190106.yml
```

将yml文件复制到B机器中，执行以下命令导入

```
conda env create -f  d:\python36_20190106.yml
```



# 删除环境

```csharp
conda remove -n mm --all
```



## 重命名环境

```bash
conda create -n tf --clone rcnn
```

```csharp
conda remove -n rcnn --all
```





# 整个anaconda文件夹迁移

*适用重置系统等情境下，如原/home/user->/home2/user*

1. 添加anaconda3文件夹软链接到/home/user/ 

   `ln -s /xxx/user/anaconda3/ /home/user/  #注意xxx处要用完整绝对路径`

2. 使用原~/.bashrc即可激活



效果:

```
ywz@509:~$ ln -s /temp_disk2/home/ywz/anaconda3/ /home/ywz/
ywz@509:~$ source ~/.bashrc
(base) ywz@509:~$ ls
anaconda3  Anaconda3-2019.07-Linux-x86_64.sh  data  database  examples.desktop  HESIC  huawei_F  multi_mode  remote
(base) ywz@509:~$ conda activate mm
(mm) ywz@509:~$ python
Python 3.6.10 |Anaconda, Inc.| (default, May  8 2020, 02:54:21)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> import torchvision
>>> print(torch.cuda.is_available())
True
```

