#by RyanXing.


1. 确认CUDA是否和要装的tensorflow版本兼容。

cat /usr/local/cuda/version.txt # 查看CUDA版本
cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2 # 查看cuDNN版本

据我所知：CUDA10.0和tf1.13是兼容的。
注意：CUDA10.0和cuDNN7.6已经安装好了，是装在/usr/local目录下的，是大家共享的，所以不要修改和升级哦。

2. 安装Anaconda。

一定要在Anaconda里创建环境，然后在环境里装各种包，跑程序。否则越到后面装的库越多，会出现很多冲突和不兼容。
Anaconda提供了很好的机制，能隔离多个子环境。如果你不小心装错了或者搞乱了环境，直接删掉这个环境，重新建一个。一切都很安全。

安装方法：

+ 在https://repo.anaconda.com/archive/上能看到全部可以下载的Anaconda版本。我们选择Anaconda3-2019.07-Linux-x86_64.sh。
+ 直接下载也可以。我后来发现迅雷下载很快：把下载链接复制到迅雷里下载，校园网速度可以到7MB/s。
+ 下载好以后，传到服务器上，比如/home/czp/下载，可以放你的安装包（以后安装包都可以堆在这里，以后还能用）。
  推荐用MobaXterm，可以拖拽上传。也可以用scp指令上传。
+ 在/home/czp/下载 目录下，执行：sh Anaconda....（Tab补齐），一切默认即可。最后问你要不要init，选择y。
+ 关闭terminal，重新开。你会看到命令行前面多一个base。（MobaXterm就是关掉窗口，重开窗口）
+ 分别执行以下三条指令，加入国内源，以后在Anaconda下载包更快：
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/

3. 创建环境

比如我们可以创建环境，名为HUAWEI，那么指令如下：
conda create -n HUAWEI python=3.7

4. 激活该环境

conda activate HUAWEI
以后要跑程序前，都这么做。激活HUAWEI环境，在环境里安装各种需要的包或库，还有跑程序。

5. 安装tensorflow-gpu=1.13
最基本的方法是：conda install 包的名字，比如conda install tensorflow-gpu=1.13

## 千万不要conda install tensorflow-gpu，会给你装最新版tf2.0！

如果搜不到，就执行：conda install --channel https://conda.anaconda.org/anaconda tensorflow-gpu=1.13

国内源（兼容windows）：

（ apt-get install python-pip python-dev)

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tensorflow-gpu==1.13.1   







6. 其他

比如你要安装 skimage 这个库，但貌似 conda install skimage 提示搜不到。这个时候这么操作：

export PATH=~/anaconda3/bin:$PATH （第一次用执行，以后都不需要执行）
anaconda search -t conda skimage # 在更大的库里，搜索skimage包

这时候会提示你发现了一些选项。你会看到每个选项右边有兼容要求，比如有的只能在py2上跑。选择兼容的那个DavidMertz/accelerate-skimage，执行：

anaconda show  DavidMertz/accelerate-skimage # 展示更多关于DavidMertz/accelerate-skimage的信息

最后一行就告诉你了下载地址。照做：conda install --channel https://conda.anaconda.org/DavidMertz accelerate-skimage
这样就下载成功了。



###########################

tensorflow-gpu  1.13版本

实验室给配了个rtx2070s的电脑，在win10中装tensorflow1.13   

GPU版 一句话搞定： (自动安装版本对应的cuda和cudnn

conda install tensorflow-gpu==1.13.1

CPU版 一句话搞定：

conda install tensorflow==1.13.1



#else:(not recommended)

（pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tensorflow-gpu==1.13.1

(ubuntu 版

sudo apt-get install python-pip python-dev

sudo python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tensorflow-gpu==1.13.1

)

注：必须指定tf版本，否则会装2.0版本

###########################

# pytorch-gpu

实验室给配了个rtx2070s的电脑，在win10中装pytorch

只去鲁大师装了显卡的驱动，然后直接装pytorch gpu版：

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/

conda config --set show_channel_urls yes

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

conda install pytorch torchvision cudatoolkit=10.1

or

conda install pytorch==1.6.0 torchvision cudatoolkit=10.1 

安装完毕



**检查PyTorch版本**

- torch.**version** # PyTorch version
- torch.version.cuda # Corresponding CUDA version
- torch.backends.cudnn.version() # Corresponding cuDNN version
- torch.cuda.get_device_name(0) # GPU type

**更新PyTorch**

- conda update pytorch torchvision -c pytorch



conda remove -n mm --all  删除环境



# 测试pytorch-cuda

```
import torch
print(torch.cuda.is_available())
```

