# 与django模板结合

将vue相关的html代码块禁用django模板：

在上述html代码前添加"\{\% verbatim \%\}"，尾部添加"\{\% endverbatim \%\}" (去掉\和")，这样vue就可以生效了，