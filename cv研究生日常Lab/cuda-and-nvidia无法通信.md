# CUDA AND NVIDIA

## 1. 安装或升级

### 1.1. 须知

`nvidia-smi` 查看显卡信息，`nvcc -V` 查看 CUDA 版本。

需要安装 NVIDIA 驱动的情况：

- `nvidia-smi` 不正常显示。
- `nvidia-smi` 显示的 NVIDIA 驱动版本号过低；不同 CUDA 要求的最低 NVIDIA 版本号不同，参见[这里](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)。

需要安装 CUDA 的情况：

- `nvcc -V` 不正常显示版本号。
- 算法需要指定 CUDA 版本（与现有版本不符）。

注意：

- 如都需安装，先装 NVIDIA 驱动，再装 CUDA。
- 安装 NVIDIA 驱动需要管理员权限。
- CUDA 尽量不要装在 `/usr` 下；装在自己 home 目录下即可，无需管理员权限。
- 一般不需要装 CUDNN（CONDA 装 PYTORCH 包时会自带）。

### 1.2. NVIDIA 驱动

无需手动下载驱动程序，无需图形界面。

#### 禁用 NOUVEAU 驱动

该驱动与 NVIDIA 驱动冲突，需保证被禁用。

先查看 NOUVEAU 是否加载：

```bash
lsmod | grep nouveau

# 没有 lsmod 则安装
sudo apt install module-init-tools
```

如果没输出，说明没加载，OK；如果有输出，则说明 NOUVEAU 正在加载，需要按以下操作禁用。

编辑 `/etc/modprobe.d/blacklist.conf` 文件，在最后一行添加：

```txt
blacklist nouveau
options nouveau modeset=0
```

更新，重启：

```bash
sudo update-initramfs -u
sudo reboot
```

确认无输出即可：

```bash
lsmod | grep nouveau
```

#### 安装 NVIDIA 驱动

安装 GCC，删除旧 NVIDIA 驱动：

```bash
sudo apt install build-essential
sudo apt remove nvidia-*
sudo apt autoremove
```

更新软件仓库列表：

```bash
sudo apt update
```

查看推荐的驱动：

```bash
ubuntu-drivers devices
```

其中会有一个版本后显示 `recommended`；例如 `nvidia-driver-465`。那么执行以下操作：

```bash
sudo apt install nvidia-settings nvidia-driver-465 nvidia-prime
sudo ubuntu-drivers autoinstall
```

重启：

```bash
sudo reboot
```

此时 `nvidia-smi` 应该就正常显示了，安装完成。

图可参见[博客](https://blog.csdn.net/BigData_Mining/article/details/99670642)。该教程中需要双显卡切换，我们不需要。

### 1.3. CUDA

参考[知乎](https://zhuanlan.zhihu.com/p/198161777)。

注意：

1. 建议装在自己的 home 目录下，无需管理员权限。
2. 可以在 home 目录下安装多个版本的 CUDA。只需修改自己 home 目录下 `~/.bashrc` 中的环境变量，即可随意切换当前的 CUDA 版本。
