# ssh ywz@467830y6j3.zicp.vip -p 32027
# --------外网----------
alias j207="ssh ywz@467830y6j3.zicp.vip -p 32027"
alias j3090="ssh ywz@467830y6j3.zicp.vip -p 57009"
alias j509="ssh ywz@370581k45d.wicp.vip -p 57526"
alias s220="ssh yangwenzhe@183.129.176.220"

# 跳板机-ssh-输入额外参数则表示不选择跳板机而使用内网
if [ x$1 != x ];then 
    #有参数$1  eg:$>. env.sh nojump #注意输入". "
    jump=""
else
    jump=" -J ywz@467830y6j3.zicp.vip:32027"
fi


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


# scp跳板机-将本机端口$2通过跳板机映射到某个机器ip:$1上的某个端口-port:22
#ssh -L 0.0.0.0:9000:10.130.159.113:22 ywz@467830y6j3.zicp.vip -p 32027
alias local='_a(){ ssh -L 0.0.0.0:$2:$1:22 ywz@467830y6j3.zicp.vip -p 32027; }; _a'
# 参考eg:$>local 10.130.159.113 9000
# 或者eg:$>local $ip518 9050

# ---------git----------
# git同步命令
alias sync="git add -A && git commit -m 'up' && git push origin master"

