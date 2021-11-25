/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：one_line_cmd.c
 * 描述    ：   
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：

*****************************************************************/
#include "one_line_cmd.h"
#include "delay.h"

#define Oneline_H GPIOD->ODR |= (1<<4);
#define Oneline_L GPIOD->ODR &= ~(1<<4);


//传送数据
void Online_trans(unsigned char data)
{
  unsigned char shiftcnt=0;
  Oneline_H
  TIM2Delay_n100us(1); //3ms
  Oneline_L
  TIM2Delay_n100us(30); //3ms
  for(shiftcnt=0;shiftcnt<8;shiftcnt++)
  {
    if(data&0x01)
    {
      Oneline_H
      TIM2Delay_n100us(12); //1200us 
      Oneline_L
      TIM2Delay_n100us(4); //400us
    }
    else
    {
      Oneline_H
      TIM2Delay_n100us(4); //400us 
      Oneline_L
      TIM2Delay_n100us(12); //1200us
    }
    data>>=1;
  }
  Oneline_H;
}


//混合命令函数——设置和命令
void Mix_Command(unsigned char number,unsigned char command)
{
/*
  unsigned char i;
  unsigned char a[5]={0};
  unsigned char n;
  //获取数据中每位上的数字
  for(i=0;i<5;i++)    
  {
    a[i] = number/(10^(4-i))%10;
    Online_trans(a[i]);
  }
  
  //找到非零起始数字
  i=0;
  while(i<5)    
  {
    if(a[i] != 0)break;
    i++;
  } 
  
  //依次传输数字
  for(n=i;n<5;n++)
  {
    Online_trans(a[n]);
  }
*/
  Online_trans(number);
  //传输指令
  Online_trans(command);   
}


















