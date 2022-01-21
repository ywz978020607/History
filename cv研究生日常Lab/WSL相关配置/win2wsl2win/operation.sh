git pull && git add -A && git commit -m "up-ywz" && git push origin shoebox

# WSL-Win 远程ssh后相互转换

#1)wsl->win
/mnt/c/Windows/System32/cmd.exe /K "cd /d D:\Desktop\folder"

#2)wsl->win : 在当前路径打开win-cmd (当前路径为WSL下/mnt/挂载的win文件夹) --例如调mpfs调试硬件开发 #或调用win下的git执行
root="D:\Desktop\folder"
temp=$(pwd -L)
temp=${temp#*folder}
temp=${temp//\//\\} #\是转义字符  /是替换一个 //是替换所有
/mnt/c/Windows/System32/cmd.exe /K "cd /d $root$temp"

/mnt/e/software/Git/git-cmd.exe

#3)win->wsl
wsl
