# Tmux 鼠标配置



下面是配置文件内容，在家目录下创建.tmux.conf，并粘贴下面内容保存后，进入tmux， ctrl+b，然后输入命令：source-file ~/.tmux.conf 即可。



步骤：

vim ~/.tmux.conf

```
set-option -g mouse on

# set default path of create new windows or panne
bind '%' split-window -h -c '#{pane_current_path}'  # Split panes horizontal
bind '"' split-window -v -c '#{pane_current_path}'  # Split panes vertically
bind c new-window -c '#{pane_current_path}' # Create new window
```

ctrl+b  :

```
source-file ~/.tmux.conf
```



小技巧：

按住shift再滚轮

按住shift选中复制