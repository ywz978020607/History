https://www.jianshu.com/p/4d48d8547c5e

系统为ubuntu 18.04.3

1. 卸载nouveau（必须）

   ```undefined
   sudo vim /etc/modprobe.d/blacklist-nouveau.conf
   
   blacklist nouveau
   blacklist lbm-nouveau
   options nouveau modeset=0
   alias nouveau off
   alias lbm-nouveau off
   
   echo options nouveau modeset=0 | sudo tee -a /etc/modprobe.d/nouveau-kms.conf
   sudo update-initramfs -u
   sudo reboot
   ```

   输入lsmod | grep nouveau  如果无输出则表示禁用成功，可能需要重启一次

2. ```
   sudo  service lightdm stop 
   ```

   ​    #与sudo init 3 作用同， 关闭图形界面，才能安装！

   sudo apt-get purge nvidia* #卸载驱动

3. 安装nvidia-smi  必须版本对应!   对照表如下

   (装显卡驱动时，CUDA决定了最低版本，而cat /proc/driver/nvidia/version 决定了支持的最高版本，区间内即可)

   https://blog.csdn.net/heiheiya/article/details/103868478 

   https://www.cnblogs.com/abella/p/10217959.html (找不到cc)

   cat /proc/driver/nvidia/version

   sudo chmod a+x NVIDIA-Linux-x86_64-435.21.run

   sudo sh ./NVIDIA-Linux-x86_64-435.21.run -no-x-check -no-nouveau-check -no-opengl-files

   

   *The distribution-provided pre-install script failed! Are you sure you want to continue? 选择 yes 继续。
   Would you like to register the kernel module souces with DKMS? This will allow DKMS to automatically build a new module, if you install a different kernel later?  选择 No 继续。
   问题没记住，选项是：install without signing
   问题大概是：Nvidia's 32-bit compatibility libraries? 选择 No 继续。
   Would you like to run the nvidia-xconfigutility to automatically update your x configuration so that the NVIDIA x driver will be used when you restart x? Any pre-existing x confile will be backed up.  选择 Yes  继续*

   https://www.cnblogs.com/abella/p/10217959.html

   输入nvidia-smi，就能看到显卡

   (如果装错：sudo apt-get purge nvidia* #卸载)

   

4. 安装cuda

cat /usr/local/cuda/version.txt

- 安装cuda 更正版：

​		https://blog.csdn.net/qq_32408773/article/details/84112166

​	sudo sh cuda_10.0.130_410.48_linux.run  不独立安装驱动  （单独安装驱动比较好）

​	vim ~/.bashrc	

``` 
export CUDA_HOME=/usr/local/cuda 
export PATH=$PATH:$CUDA_HOME/bin 
export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

​	source ~/.bashrc

​	测试:

1. cd /usr/local/cuda/samples/1_Utilities/deviceQuery 
2. sudo make
3. ./deviceQuery

​	

5. 安装cudnn：

sudo tar -xzvf cudnn-10.0-linux-x64-v7.6.5.32.tgz

sudo cp cuda/include/cudnn.h /usr/local/cuda/include

sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64

sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*

cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2 #如果输出#definexxx即正确

整理版：

https://www.cnblogs.com/dereen/p/dl_env.html



6. 安装后输入nvidia-smi 报错版本不一致

   https://blog.csdn.net/qq_40200387/article/details/90341107

7. 内核版本 5.0.0-23-generic （自动升级如果找不到后需要降级）

   如果自动升级，可能会显卡报错，解决方法是查看uname -r 以及到grub配置文件中，将0改为"1>2" #对应1是高级选项，2是第三行的二级目录选项，update grub后重启即可。

   

# 创建新用户

sudo su

*useradd csdn*

*passwd csdn*

*usermod -s /bin/bash csdn*

*usermod -d /home/csdn csdn*

*cat /etc/passwd*

## 允许该用户以管理员身份执行指令

```
su root
```

如果这里提示“su: Authentication failure”，是因为没有给root设置登录密码，解决方法： 
1.先切换回用户peng: su peng 
2.在给root设置登录密码：sudo passwd root

visudo

- 该命令实际上打开的是/etc/sudoers文件，修改该文件，在“root ALL=(ALL:ALL) ALL”这一行下面加入一行：

> csdn ALL=(ALL:ALL) ALL



