`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2019/08/01 15:46:47
// Design Name: 
// Module Name: recv_uart
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module recv_uart(
input clk_50,   //50MHz
input rst_n,     //低电平复位
input rx,         //连接板子接收rx的IO引脚
///////////////
output [7:0] rx_data,   //接收到的数据，会一直保存直到下次刷新
output valid   //上升沿有效，持续时间一个50MHz的时钟，表示更新数据。 //参考调用方式:top.v,利用reg的阻塞式赋值，两行代码在always clk内检测上升沿
    );
    
    wire temp_valid;
    assign valid = ~temp_valid;
    urx urx1(
    .clk(clk_50),
    .rst_n(rst_n),
    .rx(rx),
    .rx_data(rx_data),
    .rx_int(temp_valid)
    );
endmodule
