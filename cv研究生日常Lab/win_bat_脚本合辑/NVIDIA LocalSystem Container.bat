@echo off
echo 关闭服务
net stop "NvContainerLocalSystem"
timeout 2
echo 开启服务
net start "NvContainerLocalSystem"