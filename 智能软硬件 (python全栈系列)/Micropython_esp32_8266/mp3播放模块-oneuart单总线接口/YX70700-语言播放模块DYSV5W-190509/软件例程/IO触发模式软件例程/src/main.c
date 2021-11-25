/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：I/O模式试验
 * 描述    ：  
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：
//--------------------------------------------------------------
  硬件连接
      ____________________________
     |                           / 
     |         IO0-> PC3         |
     |         IO1-> PC4         |
     |         IO2-> PC5         |
     |         IO3-> PC6         |
     |         IO4-> PC7         |
     |         IO5-> PD1         |
     |         IO6-> PD2         |
     |         IO7-> PD3         |
     |___________________________|

*****************************************************************/
/* Includes ------------------------------------------------- --*/
#include "stm8s.h"
#include "main.h"
#include "clk.h"
#include "led.h"
#include "delay.h"
#include "IO_mode.h"
#include "TIM2.h"

//设置播放曲目号及播放模式
unsigned char music_num=0x07; //曲目号
unsigned char play_mode=1;    //播放模式——组合（1）、独立(0)
unsigned char play_key=1;     //触发模式——按键模式(1)、触发模式(0)


void main(void)
{
  
  sim();
  CLK_Config();//CLK HSI 16MHz
  LED_Init();
  rim();
  CFG->GCR|= CFG_GCR_SWD;//Disable swim function
  IO_init();
  TIM2_Init();
//  TIM2Delay_n100us(50000); //s
  LED_OFF();
  
  while (1)
  {
      IO_signal(music_num,play_mode,play_key); //IO模式测试
      while( GPIOB->IDR & 0x08 == 1);//等待释放busy位
      if(play_key == 1)  //按键模式，播放一次后停止
        break;     
  }
}