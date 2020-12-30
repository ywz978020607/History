#!/bin/bash

# ----- ----- ----- 配置 ----- ----- ------
#
# USER_LIST 为数组类型，可填写用户的openid
# 如果 USER_LIST 为空，则会遍历用户列表进行群发
#
# ----- ----- ----- ----- ----- ----- -----

WECHAT_APPID='xxxxx'
WECHAT_APPSECRET='xxxxx'
WECHAT_TEMPLATE_ID='xxxxx'
USER_LIST=()
#USER_LIST=("xxxxx" "xxxxx")



# ----- 运行时 -----
WECHAT_ACCESS_TOKEN=''
THIS_PWD=$(pwd)
JQ=${THIS_PWD}/jq
ACCESS_TOKEN_CONF=${THIS_PWD}/access_token.conf
ICIBA_EVERYDAY=()
USER_LIST_MAX=''



# 请求access_token
request_access_token(){
    url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${WECHAT_APPID}&secret=${WECHAT_APPSECRET}"
    WECHAT_ACCESS_TOKEN=$(echo $(curl ${url}) | ${JQ} .access_token)
    echo -e ${WECHAT_ACCESS_TOKEN:1:-1} > ${ACCESS_TOKEN_CONF}
    WECHAT_ACCESS_TOKEN=${WECHAT_ACCESS_TOKEN:1:-1}
}

# 获取access_token
get_access_token(){
    if [ ! -f ${ACCESS_TOKEN_CONF} ]; then
        request_access_token
    else
        modify_date=`stat -c %Y ${ACCESS_TOKEN_CONF}`
        now_date=`date +%s`
        if [ $[ $now_date - $modify_date ] -gt 3600 ]; then
            request_access_token
        else
            WECHAT_ACCESS_TOKEN=$(cat ${ACCESS_TOKEN_CONF})
        fi
    fi
}

# 获取用户列表
get_user_list(){
    url="https://api.weixin.qq.com/cgi-bin/user/get?access_token=${WECHAT_ACCESS_TOKEN}&next_openid="
    DATA=$(curl ${url})
    errcode=$(echo ${DATA} | ${JQ} .errcode)
    if [ "$errcode" != "" ]; then
        if [ $errcode == "40001" ]; then
            request_access_token
            url="https://api.weixin.qq.com/cgi-bin/user/get?access_token=${WECHAT_ACCESS_TOKEN}&next_openid="
            DATA=$(curl ${url})
        fi
    fi
    OPENIDS=$(echo ${DATA} | ${JQ} .data.openid)
    i=0
    OPENID=$(echo ${OPENIDS} | ${JQ} .[$i])
    if [ -n "${OPENID}" ]; then
        OPENID=${OPENID:1:-1}
        while [ "${OPENID}" != "" ]; do
            USER_LIST[$i]=$OPENID
            i=`expr $i + 1`
            OPENID=$(echo ${OPENIDS} | ${JQ} .[$i])
            if [ "${OPENID}" == null ]; then
                USER_LIST_MAX=$i
                break
            else
                OPENID=${OPENID:1:-1}
            fi
        done
    fi
}

# 发送模板消息
send_msg(){
    url="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=${WECHAT_ACCESS_TOKEN}"
    msg="{\"url\":${ICIBA_EVERYDAY[3]},\"data\":{\"content\":{\"color\":\"#0000CD\",\"value\":${ICIBA_EVERYDAY[0]}},\"note\":{\"value\":${ICIBA_EVERYDAY[1]}},\"translation\":{\"value\":${ICIBA_EVERYDAY[2]}}},\"touser\":\"$1\",\"template_id\":\"${WECHAT_TEMPLATE_ID}\"}"
    result=$(curl -H "Content-Type:application/json" -X POST --data "${msg}" ${url})
    errcode=$(echo $result | ${JQ} .errcode)
    if [ "${errcode}" == "0" ]; then
        echo -e " [\033[32mINFO\033[0m] send to $1 is success\r\n"
    else
        echo " [\033[31mERROR[0m] send to $1 is error\r\n"
        if [ "$errcode" == "40001" ]; then
            request_access_token
            send_msg $1
        fi
    fi
}

# 获取爱词霸每日一句
get_iciba_everyday(){
    url="http://open.iciba.com/dsapi/"
    ICIBA=$(curl ${url})
    ICIBA_EVERYDAY[0]=$(echo ${ICIBA} | ${JQ} .content)
    ICIBA_EVERYDAY[1]=$(echo ${ICIBA} | ${JQ} .note)
    ICIBA_EVERYDAY[2]=$(echo ${ICIBA} | ${JQ} .translation)
    ICIBA_EVERYDAY[3]=$(echo ${ICIBA} | ${JQ} .fenxiang_img)
}

# 为设置的用户列表发送消息
send_everyday_words(){
    if [ "${USER_LIST[0]}" == "" ]; then
        get_user_list
    else
        USER_LIST_MAX=${#USER_LIST[@]}
    fi
    for ((i=0;i<${USER_LIST_MAX};i++)); do
        send_msg ${USER_LIST[$i]}
    done
}

# 执行
run(){
    get_access_token
    get_iciba_everyday
    send_everyday_words
}



#执行
run


