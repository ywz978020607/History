/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：uart.H
 * 描述    ：   
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：

*****************************************************************/
#ifndef __UART_H_
#define __UART_H_
#include "stm8s.h"


//--------------------------

void UART_Config(void);
void UART1_SendByte(unsigned char data);

#endif