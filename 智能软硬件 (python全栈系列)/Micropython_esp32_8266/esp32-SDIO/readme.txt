按照SDIO完整方式连线，具体连线如下表：

SP32 pin	SD name
GPIO14 (MTMS)	CLK
GPIO15 (MTDO)	CMD / DI
GPIO2	DAT0 / DO
GPIO4	DAT1
GPIO12 (MTDI)	DAT2
GPIO13 (MTCK)	DAT3
--------------------------------------------------------
#正常也可以熔断，不影响什么
https://www.freesion.com/article/2761785305/
ESP32的IO12决定了VDD_SDIO,也就是内部的SPI,EXT RAM的IO工作电压,针对WROVER,他是1.8V的,针对WROOM,他是3.3V的,但是他是通过IO12判断,有没有办法释放IO12然后也能决定VDD_SDIO呢.
需efuse工具进行熔丝熔断，固定flash电压3.3V，防止进入错误的1.8V，设置3.3V，启动内部flash（因为挂在SD，有上拉，不熔断的话检测进入1.8）
https://www.taterli.com/3183/
注意：GPIO2需要加上拉电阻选通开关/留出IO接地试试，不然无法烧录

E:\software\anaconda\Scripts
输入 (需重启，如同烧录，把ESP32的GPIO0拉低，重新上电）
./espefuse.exe -b 115200 -p COM3 summary
./espefuse.exe -b 115200 -p COM3 set_flash_voltage 3.3V
---------------------------------------------------------
http://docs.micropython.org/en/latest/library/machine.SDCard.html
引脚说明
除SPI有两组可用外，SDIO只能用slot=1（默认）
