/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：clk.H
 * 描述    ：   
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：

*****************************************************************/
#include "clk.h"

//--------------------------
void CLK_Config(void)
{
    CLK->CKDIVR=0x00 ;                    //16M
    CLK->SWCR |=0x02;                     // enable convert
    CLK->SWR=0xe1;                        //lect HSI
    
    CLK->SWCR &= 0xFD;
    CLK->PCKENR1|=(1<<5);                    //enable TIM2
    
    while((CLK->ICKR&0x02)!=0x02);        //wait for converting success
    /*
    CLK_ECKR |=0X1;  //开启外部时钟 
    
    while(!(CLK_ECKR&0X2)); //等待外部时钟rdy 
    
    CLK_CKDIVR &= 0XF8;     //CPU无分频 
    
    CLK_SWR = 0XB4;  //选择外部时钟 
    
    while(!(CLK_SWCR&0X8)); //这里要等 
    
    
    CLK_SWCR |=0X2;  //使能外部时钟 
    */
}