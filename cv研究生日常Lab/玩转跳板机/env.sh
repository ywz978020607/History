# ssh ywz@467830y6j3.zicp.vip -p 32027
# --------跳板机配置-------
jump1="ywz@467830y6j3.zicp.vip:32027"
jump2="ywz@467830y6j3.zicp.vip:57009"
jump3="ywz@370581k45d.wicp.vip:57526"

# 跳板机-ssh-输入额外参数则表示不选择跳板机而使用内网
# 默认1号跳板机 可输入参数 #eg:$>. env.sh nojump/1/2/3 #注意输入". "
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
# ----外网&跳板机直连----
alias s220="ssh yangwenzhe@183.129.176.220"
alias j207="ssh ${jump1/:/ -p }"
alias j3090="ssh ${jump2/:/ -p }"
alias j509="ssh ${jump3/:/ -p }"



# --------内网----------
ip518="10.135.6.78"
ip509="10.134.162.159"
ipdyf="10.130.159.113"
ipywz="10.136.150.144"

# ssh ywz@10.135.6.78 -J ywz@467830y6j3.zicp.vip:32027
alias s518="ssh ywz@$ip518 $jump"
alias s509="ssh ywz@$ip509 $jump"
alias sdyf="ssh dyf@$ipdyf $jump"
alias sywz="ssh ywz@$ipywz $jump"


# 端口映射 scp跳板机-将本机端口 通过跳板机映射到某个机器ip上的某个端口
# ssh -L 0.0.0.0:9000:10.130.159.113:22 ywz@467830y6j3.zicp.vip -p 32027
# alias mapping='_a(){ ssh -L 0.0.0.0:$2:$1:22 ywz@467830y6j3.zicp.vip -p 32027; }; _a'
# 参考eg:$>mapping 10.130.159.113 9050 或者eg:$>mapping $ip518 9050
# 又或eg: $>mapping $ip518 22 9050 #将$ip518:22 映射到本机9050端口
# 参数说明: mapping [内网机器-ip] [内网机器-端口-默认22] [自定义映射到本机的端口]
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

