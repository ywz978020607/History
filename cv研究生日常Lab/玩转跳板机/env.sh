
# ----------使用帮助[命令eg:>help]--------
help(){
    echo """
    #建议看env.sh代码及注释
    #1.初始化配置(必须)
    . env.sh        #使用默认1号跳板机
    . env.sh 3      #使用3号跳板机
    . env.sh nojump #不使用跳板机，如已经在内网中可使用此项

    #2.直接连接跳板机本身(可选)
    j2      #ssh连接2号跳板机
    s220    #ssh连接到本身可公网直连的服务器

    #3.连接内网机器(可选)
    s518    #第一步中选择的跳板机/无跳板机进行内网机器ssh连接

    #4.映射内网机器端口(可选)
    # mapping函数主要用来端口映射，方便scp/sftp/打开浏览器查看面板等高级操作 搭配本机ip固定127.0.0.1进一步使用
    mapping $ip518 22 9050 #将内网机器的22端口(默认 可缺省) 映射到本机的9050端口


    #5.查看配置的内网机器ip(可选)
    echo $ip518

    #6.查看使用说明(可选)
    help
    """
}

###################################################
###################################################
###################################################

# -------公网服务器直连[命令eg:>s220]-----
alias s220="ssh yangwenzhe@183.129.176.220"

# -------------跳板机配置--------------
jumpnum=4
jump1="ywz@467830y6j3.zicp.vip:32027" #207
jump2="ywz@467830y6j3.zicp.vip:57009" #3090
jump3="ywz@370581k45d.wicp.vip:57526" #509
jump4="dyf@cn-zz-bgp-7.natfrp.cloud:14775" #ipdyf
# --------跳板机直连[命令eg:>j1]-------
for((i=1;i<=$jumpnum;i++));  
do
temp=`eval echo "j$i"`
tempcmd=`eval echo '$'"jump$i"`
alias $temp="ssh ${tempcmd/:/ -p }" 
done

# ============初始化加载本文件(**必看第一步**)=============
# [命令eg:$>. env.sh (nojump/1/2/3)] #注意开头输入". "
# 跳板机jump选择 默认1号跳板机
if [ x$1 != x ];then
    if [ $1 == "nojump" ];then
        jump=""
        echo "nojump";
    else
        temp=`eval echo '$'"jump$1"` #字符串-eval->变量
        jump=" -J $temp"
        echo $jump
    fi
else
    jump=" -J $jump1" #默认
fi
# ======================================================


# -----------内网IP[变量eg:>$ip518 表示ip地址便于端口映射等]----------------
ip518="10.135.6.78"
ip509="10.134.162.159"
ip3090="10.134.162.65"
ipdyf="10.130.157.75"
ipywz="10.136.150.144"

# ------------------常用: 内网跳连SSH[命令eg:>s518]-----------------------
alias s518="ssh ywz@$ip518 $jump"
alias s509="ssh ywz@$ip509 $jump"
alias sdyf="ssh dyf@$ipdyf $jump"
alias sywz="ssh ywz@$ipywz $jump"



# ----------常用: 跳板机端口映射[命令eg:>mapping $ip518 22 9050]----------
# scp跳板机-将本机端口 通过跳板机映射到某个机器ip上的某个端口
# 参数说明: mapping [内网机器-ip] [内网机器-端口-默认22可缺省] [自定义映射到本机的端口]
mapping(){
    if [ $# == 2 ]
    then
        config="0.0.0.0:$2:$1:22"
    elif [ $# == 3 ]
    then
        config="0.0.0.0:$3:$1:$2"
    fi
    mapcmd="ssh -L $config ${jump/:/ -p }" #ywz@467830y6j3.zicp.vip -p 32027;
    mapcmd=${mapcmd/-J/}
    echo $mapcmd
    $mapcmd
}


# ---------git----------
# git同步命令
alias sync="git add -A && git commit -m 'up' && git push origin master"



# 参考
# alias j1="ssh ${jump1/:/ -p }" => ssh ywz@467830xxx3.zicp.vip -p 32xxx
# ssh ywz@10.135.6.78 -J ywz@467830y6j3.zicp.vip:32027
# ssh -L 0.0.0.0:9000:10.130.159.113:22 ywz@467830y6j3.zicp.vip -p 32027
