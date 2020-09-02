vim ~/.bashrc

在最后添加：

export PATH=~/anaconda3/bin:$PATH

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