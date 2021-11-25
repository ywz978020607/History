/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：IO_MODE.H
 * 描述    ：   
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：

*****************************************************************/

#include "stm8s.h"

void IO_init(void)
{
  //配置IO
  
  GPIOD->DDR |= (1<<1) | (1<<2) | (1<<3);    //  PD1-PD3 output mode
  GPIOD->CR1 |= (1<<1) | (1<<2) | (1<<3);
  //GPIOD->CR2 =~(1<<1) | ~(1<<2) | ~(1<<3);
  GPIOD->ODR |= (1<<1) | (1<<2) | (1<<3);
  
  GPIOC->DDR |= (1<<3) | (1<<4) | (1<<5) | (1<<6) | (1<<7);    //PC3-PC7 output
  GPIOC->CR1 |= (1<<3) | (1<<4) | (1<<5) | (1<<6) | (1<<7);
  //GPIOC->CR2 =~(1<<3) | ~(1<<4) | ~(1<<5) | ~(1<<6) | ~(1<<7);
  GPIOC->ODR |= (1<<3) | (1<<4) | (1<<5) | (1<<6) | (1<<7);
  
  
  //BUSY位   BUSY位占用-低电平，释放-高电平
  GPIOB->DDR &= ~(1<<4);     //PB4 input mode
  GPIOB->CR1 &= ~(1<<4);
  GPIOB->CR2 &= ~(1<<4);
  
}


//IO测试程序——输入变量为曲目号、模式（0-独立，1-组合），触发模式（0-电平触发，1-按键触发）

void IO_signal(unsigned char data,unsigned char combin,unsigned char key_touch)
{
  unsigned char n;
  if(combin)  //IO组合模式
  {
    for(n=0;n<8;n++)
    {
      if(n<5) //数据低5位，IO0-IO4
      {
        if((data & (0x01<<n))>>n) 
          GPIOC->ODR &= ~(1<<n+3);  //PC3-PC7低电平触发
        else       
          GPIOC->ODR |= (1<<n+3);
      }
      else  //数据高3位,IO5-IO7
      {
        if((data & (0x01<<n))>>n) 
          GPIOD->ODR &= ~(1<<n-4);  //PD1-PD3低电平触发
        else       
          GPIOD->ODR |= (1<<n-4);
      }
    }
    
  }
  else   //IO独立模式
  {
    switch(data)
    {
      case 0x01:
        GPIOC->ODR &= ~(1<<3);//PC3 低电平触发
        GPIOC->ODR |= (1<<4) | (1<<5) | (1<<6) | (1<<7);
        GPIOD->ODR |= (1<<1) | (1<<2) | (1<<3);
        break;   
      case 0x02:
        GPIOC->ODR &= ~(1<<4);//PC4
        GPIOC->ODR |= (1<<3) | (1<<5) | (1<<6) | (1<<7);
        GPIOD->ODR |= (1<<1) | (1<<2) | (1<<3);
        break;   
      case 0x03:
        GPIOC->ODR &= ~(1<<5);//PC5
        GPIOC->ODR |= (1<<3) | (1<<4) | (1<<6) | (1<<7);
        GPIOD->ODR |= (1<<1) | (1<<2) | (1<<3);
        break;   
      case 0x04:
        GPIOC->ODR &= ~(1<<6);//PC6
        GPIOC->ODR |= (1<<3) | (1<<4) | (1<<5) | (1<<7);
        GPIOD->ODR |= (1<<1) | (1<<2) | (1<<3);
        break;   
      case 0x05:
        GPIOC->ODR &= ~(1<<7);//PC7
        GPIOC->ODR |= (1<<3) | (1<<4) | (1<<5) | (1<<6);
        GPIOD->ODR |= (1<<1) | (1<<2) | (1<<3);
        break;   
      case 0x06:
        GPIOD->ODR &= ~(1<<1);//PD1
        GPIOC->ODR |= (1<<3) | (1<<4) | (1<<5) | (1<<6) | (1<<7);
        GPIOD->ODR |= (1<<2) | (1<<3);
        break;   
      case 0x07:
        GPIOD->ODR &= ~(1<<2);//PD2
        GPIOC->ODR |= (1<<3) | (1<<4) | (1<<5) | (1<<6) | (1<<7);
        GPIOD->ODR |= (1<<1) | (1<<3);
        break;   
      case 0x08:
        GPIOD->ODR &= ~(1<<3);//PD3
        GPIOC->ODR |= (1<<3) | (1<<4) | (1<<5) | (1<<6) | (1<<7);
        GPIOD->ODR |= (1<<1) | (1<<2);
        break;   
      default:
        GPIOC->ODR = (1<<3) | (1<<4) | (1<<5) | (1<<6) | (1<<7);  //8首之外的数据，IO0-IO7均为高电平
        GPIOD->ODR = (1<<1) | (1<<2) | (1<<3);
        break;
    } 
  }
  if(key_touch)     //按键模式
  {
    TIM2Delay_n100us(1000); //至少100ms延时   
    GPIOC->ODR = (1<<3) | (1<<4) | (1<<5) | (1<<6) | (1<<7);  //释放按键
    GPIOD->ODR = (1<<1) | (1<<2) | (1<<3);
  }
}
