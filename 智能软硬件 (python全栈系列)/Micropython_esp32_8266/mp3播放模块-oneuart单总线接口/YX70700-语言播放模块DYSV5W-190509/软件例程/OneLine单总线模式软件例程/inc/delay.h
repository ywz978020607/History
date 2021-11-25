/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：delay.H
 * 描述    ：  
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：
*****************************************************************/
#ifndef __DELAY_H
#define __DELAY_H 


//-------------delay延时函数-------------
void Delay(unsigned int nCount);
void TIM2DelayDecrement(void);
void TIM2Delay_n100us(unsigned int n100us);
#endif