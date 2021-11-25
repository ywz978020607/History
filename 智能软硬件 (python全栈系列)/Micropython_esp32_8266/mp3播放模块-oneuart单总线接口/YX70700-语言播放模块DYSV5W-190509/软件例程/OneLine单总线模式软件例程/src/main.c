/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：ONE_LINE功能测试
 * 描述    ：  
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：
//--------------------------------------------------------------
  硬件连接
      _____________________________
     |                            | 
     |  IO4/ONE_LINE---------PD4  |
     |____________________________|

*****************************************************************/
/* Includes ------------------------------------------------- --*/
#include "stm8s.h"
#include "main.h"
#include "clk.h"
#include "led.h"
#include "delay.h"
#include "uart.h"
#include "tim2.h"
#include "IO.h"
#include "one_line_cmd.h"

//设置参数
unsigned char music_num = 2;    //曲目名
unsigned char vol_num = 20;     //音量值范围0-30，上电默认20
unsigned char EQ_num = 0;       //EQ定义，NORMAL(00),POP(01),ROCK(02),JAZZ(03),CLASSIC(04),上电默认NORMAL(00)
unsigned char cyc_num = 2;      //定义播放模式，全盘循环（00），单曲循环（01），单曲停止（02），全盘随机（03），
                                  //目录循环（04），目录随机（05），目录顺序播放（06），顺序播放（07），上电默认为单曲停止。
unsigned char chnl_num = 0;     //DAC输出通道定义，MP3播放通道（00），AUX播放通道（01），MP3+AUX（02），上电默认MP3播放通道 


void main(void)
{
  
  sim();
  CLK_Config();//CLK HSI 16MHz
  LED_Init();
  UART_Config();
  rim();
  CFG->GCR|= CFG_GCR_SWD;//Disable swim function
  IO_Init();
  TIM2_Init();
  TIM2Delay_n100us(50000); //s
//  TIM2Delay_n100us(50000); //s
  LED_OFF();
  
      
      /***********基本操作指令***********/
      //选择播放磁盘，SD卡、U盘、Flash三选一
      //Online_trans(SD_CARD);            //选择SD卡
      //Online_trans(USB_FLASH_DISK);     //选择U盘
      //Online_trans(FLASH_DISK);         //选择FLASH
      
      /***********混合操作指令***********/
      //Mix_Command(vol_num,VOLUME);               //设置音量
      //Mix_Command(EQ_num,EQ);                    //设置EQ
      Mix_Command(cyc_num,CYCLICAL_MODE);          //设置循环模式
      //Mix_Command(chnl_num,CHANNEL);             //选择播放通道
  
 //     Online_trans(PLAY);               //播放
      //Online_trans(PAUSE);              //暂停
      //Online_trans(STOP);               //停止
      //Online_trans(PREV_MUSIC);         //上一曲
      //Online_trans(NEXT_MUSIC);         //下一曲
      //Online_trans(PREV_CATALOGUE);     //上一目录，播放上一目录中最后一首曲目
      //Online_trans(NEXT_CATALOGUE);     //下一目录，播放下一目录中第一首曲目
      //Online_trans(SYS_HIBERNATION);    //系统休眠
      //Online_trans(CLOSE_DOWN);         //结束播放
      //Online_trans(CLEAR);              //数字清除

     
      //“选曲”和“插播”是根据曲目名字播放  
      //播放指定曲目
      //必须对曲目名中每一位数字单独发送，数字发送完毕后，再发送指令
      //例如曲目名为“00123.mp3”，则选曲输入的数据依次为“0x01”“0x02”“0x03”“0x0B”，完成选曲
      //例如，00255.mp3
      Online_trans(0);
      Online_trans(0);
      Online_trans(2);
      Online_trans(MUSIC_SELECT);

 /*
      //设置插播曲目
      Online_trans(2);
      Online_trans(5);
      Online_trans(5);
      Online_trans(INTER_CUT);
*/
  while(1)
  {
      LED_ON();
      TIM2Delay_n100us(5000); //s
      LED_OFF();
      TIM2Delay_n100us(5000); //s
  }
      
}