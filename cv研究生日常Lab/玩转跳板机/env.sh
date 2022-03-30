
# ----------使用帮助[命令eg:>help]--------
help(){
    echo """
    #建议看env.sh代码及注释
    #1.初始化配置(必须)
    . env.sh        #使用默认1号跳板机
    . env.sh 3      #使用3号跳板机
    . env.sh nojump #不使用跳板机，如已经在内网中/需要多级跳板可使用此项

    #2.直接连接跳板机本身(可选)
    j2      #ssh连接2号跳板机
    s220    #ssh连接到本身可公网直连的服务器

    #3.连接内网机器(可选)
    s518    #第一步中选择的跳板机/无跳板机进行内网机器ssh连接
    ### 多级跳板ssh[注意规则]-无视默认选择
    ssh ywz@$ip518 -J $jump1,$jump2,$jump3 #跳板顺序为: jump1->jump2->jump3->ip518

    #4.映射内网机器端口(可选)
    # mapping函数主要用来端口映射，方便scp/sftp/打开浏览器查看面板等高级操作 搭配本机ip固定127.0.0.1进一步使用
    mapping $ip518 22 9050 #将内网机器的22端口(默认ssh端口) 映射到本机的9050端口，使用默认跳板机
    ### 多级跳板后映射机器端口[注意规则]-无视默认选择，但至少输入一个跳板机
    mapping $ip518 22 9050 $jump1 $jump2 $jump3 #端口映射多级跳转规则, jump1->jump2->jump3->ip518

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
jumpnum=6
jump0="127.0.0.1:22" #自身ssh作为跳板机
jump1="ywz@467830y6j3.zicp.vip:32027" #30901
jump2="ywz@467830y6j3.zicp.vip:57009" #30902
jump3="admin@10.135.115.200:22" #nouse
jump4="dyf@cn-zz-bgp-7.natfrp.cloud:14775" #ipdyf
jump5="ywz@cn-hn-dx-1.natfrp.cloud:56603" #ipywz
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
ip509="10.135.206.119"
ip207="10.134.162.162"
ip401="10.134.162.193"
ip2080="10.134.162.90"
ip930="10.134.126.158"
ip30901="10.130.156.192"
ip30902="10.130.158.90"
ipdyf="10.130.157.75"
iplty="10.135.115.200"
ipvm="192.168.136.128"

# ------------------常用: 内网跳连SSH[命令eg:>s518]-----------------------
alias s518="ssh ywz@$ip518 $jump"
alias s509="ssh ywz@$ip509 $jump"
alias s207="ssh ywz@$ip207 $jump"
alias s401="ssh ywz@$ip401 $jump"
alias s2080="ssh ywz@$ip2080 $jump"
alias s930="ssh ywz@$ip930 $jump"
alias s30901="ssh ywz@$ip30901 $jump"
alias s30902="ssh ywz@$ip30902 $jump"
alias sdyf="ssh dyf@$ipdyf $jump"
alias slty="ssh ywz@$iplty $jump"
alias svm="ssh ywz@$ipvm"

# ----------常用: 跳板机端口映射[命令eg:>mapping $ip518 22 9050]----------
# scp跳板机-将本机端口 通过跳板机映射到某个机器ip上的某个端口
# 参数说明: mapping [内网机器-ip] [内网机器-端口] [自定义映射到本机的端口] [$jump1 $jump2 ...]
mapping(){
    if [ $# == 3 ]
    then
        if [ $jump=="" ]
        then
            mapcmd=""
            echo "need one jumper at least in mapping!"
        else
            config="0.0.0.0:$3:$1:$2" #config="0.0.0.0:$2:$1:22"
            mapcmd="ssh -L $config ${jump/:/ -p }" #ywz@467830y6j3.zicp.vip -p 32027;
            mapcmd=${mapcmd/-J/}
        fi
    elif [ $# != 3 ]
    then
        config="0.0.0.0:$3:$1:$2"
        if [ $# != 4 ];then
            concatjump=`eval echo '$'"4"`
            for(( i=5;i<=$#-1;i++ ));
            do  
                tempcmd=`eval echo '$'"$i"`
                concatjump="$concatjump,$tempcmd"
            done
        fi
        finalone=`eval echo '$'"$#"`
        mapcmd="ssh -L $config ${finalone/:/ -p } -J $concatjump"
    fi
    echo $mapcmd
    $mapcmd
}





# ---------git----------
# git同步命令
alias sync="git add -A && git commit -m 'up' && git push origin master"


# ---------天气预报-------
alias wea="curl http://wttr.in"

# 参考
# alias j1="ssh ${jump1/:/ -p }" => ssh ywz@467830xxx3.zicp.vip -p 32xxx
# 多级跳转
# ssh ywz@10.135.6.78 -J ywz@467830y6j3.zicp.vip:32027 ,dyf@10.130.157.75:22
# ssh -L 0.0.0.0:9000:10.130.159.113:22 ywz@467830y6j3.zicp.vip -p 32027
# 多级跳转
# ssh -L 0.0.0.0:9000:10.130.159.113:22 ywz@10.135.6.78 -p 22 -J dyf@cn-zz-bgp-7.natfrp.cloud:14775,dyf@cn-zz-bgp-7.natfrp.cloud:14775
