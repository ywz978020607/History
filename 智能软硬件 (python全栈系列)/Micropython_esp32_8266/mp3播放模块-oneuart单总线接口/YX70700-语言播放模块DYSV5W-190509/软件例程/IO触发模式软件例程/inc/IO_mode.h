/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：IO_MODE.H
 * 描述    ：   
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：

*****************************************************************/
#ifndef __IO_MODE_H_
#define __IO_MODE_H_
#include "stm8s.h"


//--------------------------
void IO_init(void);
void IO_signal(unsigned char data,unsigned char combin,unsigned char key_touch);
#endif