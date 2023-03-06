# ----------使用帮助[命令eg:>help]--------
help(){
    echo """
    一行自动/手动管理蓝牙设备连接/断开  
    help()      #使用帮助  

    . bt.sh     #默认设备自动开/关  

    . bt.sh a   #airpods自动开/关  
    . bt.sh x   #xm3自动开/关  

    . bt.sh x q #xm3进行查询  
    . bt.sh x 1 #xm3进行开  
    . bt.sh x 0 #xm3进行关  
    
    """
}


##############################
# btdiscovery->address(more quickly)
xm3="38:18:4C:12:5C:B3"
airpods="7C:9A:1D:B8:61:C8"

# https://bluetoothinstaller.com/bluetooth-command-line-tools
cmdpath="/mnt/d/software/BluetoothCommandLineTools/bin"
##############################

#choose device
if [ x$1 != x ];then
    if [ $1 == "a" ];then
        device="$airpods"
        echo "airpods"
    else
        device="$xm3" #默认
        echo "xm3"
    fi
else
    device="$xm3" #默认
    echo "xm3"
fi


#mode->auto=auto open/close
mode="auto"
if [ x$2 != x ];then
    if [ $2 == "1" ];then
        mode="open"
        echo $mode
    elif [ $2 == "0" ];then
        mode="close"
        echo $mode
    else
        mode="query"
        echo "check status..."
        temp_status=$($cmdpath/btdiscovery.exe -b $device -d "%c%")
        echo "temp status:$temp_status"
    fi
else
    #auto
    echo "auto, check status..."
    temp_status=$($cmdpath/btdiscovery.exe -b $device -d "%c%")
    echo $temp_status # ${#"Yes不可见"}=4, ${#"No不可见"}=3
    if [ ${#temp_status} == 4 ];then
        echo "is open"
        mode="close"
    else
        echo "is close"
        mode="open"
    fi
fi

#exec
if [ $mode == "open" ];then
    echo "mode:$mode"
    temp_cmd1=$($cmdpath/btcom.exe -b ${device} -c -s111e)
    temp_cmd2=`$cmdpath/btcom.exe -b ${device} -c -s110b`
elif [ $mode == "close" ];then
    echo "mode:$mode"
    temp_cmd1=`$cmdpath/btcom.exe -b ${device} -r -s111e`
    temp_cmd2=`$cmdpath/btcom.exe -b ${device} -r -s110b`
fi








# 参考
# temp_status=$($cmdpath/btdiscovery.exe -b $device -d "%c%")
# echo $temp_status #show the result
# or
# temp_status=`$cmdpath/btdiscovery.exe -b $device -d "%c%"`
# echo $temp_status #show the result
# or
# temp_status="$cmdpath/btdiscovery.exe -b $device -d "%c%""
# $temp_status #exec
# echo $temp_status #show the cmd


# /mnt/d/software/BluetoothCommandLineTools/bin/btdiscovery.exe
# /mnt/d/software/BluetoothCommandLineTools/bin/btdiscovery.exe -b 38:18:4C:12:5C:B3 -d "%c%"
# /mnt/d/software/BluetoothCommandLineTools/bin/btcom.exe -b "38:18:4C:12:5C:B3" -c -s111e
# /mnt/d/software/BluetoothCommandLineTools/bin/btcom.exe -b "38:18:4C:12:5C:B3" -c -s110b
# /mnt/d/software/BluetoothCommandLineTools/bin/btcom.exe -b "38:18:4C:12:5C:B3" -r -s111e
# /mnt/d/software/BluetoothCommandLineTools/bin/btcom.exe -b "38:18:4C:12:5C:B3" -r -s110b