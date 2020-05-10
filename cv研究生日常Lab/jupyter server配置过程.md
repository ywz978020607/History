#shell输入
pip install jupyter #安装jupyter notebook
pip install ipython
pip install jupyterlab #再安装lab版

jupyter notebook password #设置密码

#生成lab配置文件
jupyter lab --generate-config
#在生成的文件 vim xx.py中，找到下面三行代码，取消注释，并修改等号右侧为以下：
	c.NotebookApp.allow_root = True
	c.NotebookApp.open_browser = False
	c.NotebookApp.password = '刚才复制的输出粘贴到这里来'

#运行试试
#单次运行
jupyter lab --ip=0.0.0.0 --port=9003 
#后台运行
nohup jupyter lab --ip=0.0.0.0 --no-browser --port=9003 &  

