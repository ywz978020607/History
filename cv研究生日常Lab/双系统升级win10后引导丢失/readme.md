# 双系统升级win10后grub丢失解决

使用usb装好的ubuntu系统进入，选择try without install试用ubuntu模式

sudo -i

fdisk -l 查看ubuntu在哪个分区，看系统为Linux或看大小或者试挂，以/dev/sda5为例

mkdir /media/tmp

mount /dev/sda5 /media/tmp

#查看是否正确：cd /media/tmp/ & ls 查看目录下是否有dev 等很多linux所属文件夹

#安装引导进行修复

grub-install --root-directory=/media/tmp  /dev/sda

#重启，更改bios顺序即可，如果没用win10引导，则进入ubuntu后升级grub

sudo update-grub2