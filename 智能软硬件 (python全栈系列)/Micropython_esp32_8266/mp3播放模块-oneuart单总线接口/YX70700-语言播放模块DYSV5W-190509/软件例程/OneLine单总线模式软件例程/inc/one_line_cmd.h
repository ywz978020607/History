/******************** (C) COPYRIGHT  ***************************
 * 文件名  ：one_line_cmd.H
 * 描述    ：   
 * 库版本  ： 
 * 作者    ：
 * 博客    ：
 *修改时间 ：

*****************************************************************/
#ifndef __ONE_LINE_CMD_H_
#define __ONE_LINE_CMD_H_
#include "stm8s.h"

//one_line指令
#define CLEAR           0x0A    //清零数字
#define MUSIC_SELECT    0x0B    //选取确认
#define VOLUME          0x0C    //设置音量
#define EQ              0x0D    //设置EQ
#define CYCLICAL_MODE   0x0E    //设置循环模式
#define CHANNEL         0x0F    //设置通道
#define INTER_CUT       0x10    //设置插播曲目
#define PLAY            0x11    //播放
#define PAUSE           Ox12    //暂停
#define STOP            0x13    //停止
#define PREV_MUSIC      0x14    //上一曲
#define NEXT_MUSIC      0x15    //下一曲
#define PREV_CATALOGUE  0x16    //上一目录
#define NEXT_CATALOGUE  0x17    //下一目录
#define SD_CARD         0x18    //选择SD卡
#define USB_FLASH_DISK  0x19    //选择U盘
#define FLASH_DISK      0x1A    //选择FLASH
#define SYS_HIBERNATION 0x1B    //系统休眠
#define CLOSE_DOWN      0x1C    //结束播放

//--------------------------
void Online_trans(unsigned char data);
void Mix_Command(unsigned char number,unsigned char command);
#endif          