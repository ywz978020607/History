`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2019/07/27 15:15:42
// Design Name: 
// Module Name: CountFreq
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


module CountFreq(
    input clk_in_100MHz,      // 输入100MHz时钟
    input sig_in,             // 被测信号的TTL电平   
    input m_gdata_ready,      // 主片可接受信号，若该引脚为低  则使得计数器全部清零不工作
    input enable,             // 使能端   高电平有效   若低电平   则全部清零不作数   再次高电平就重来
    input rst_n,              // 异步复位信号
    
    output reg [31:0] clk_num,    // 输出时钟计数数目
    output reg [31:0] sig_num,    // 输出信号计数数目
    output reg out_valid          // 持续高电平，输出有效，输出有效后  输出值锁存不再计数
    );
    initial begin
        clk_num = 32'd0;
        sig_num = 32'd0;
        out_valid = 0;
    end
    // 计数器的工作使能端由控制端与ready端共同决定
    // 当当前工作模式被选定  并且主片可接受数据时才可工作   否则都是清零等待
    wire enable_count;
    and a1(enable_count, enable, m_gdata_ready);
    // 设计起始与结束都是输入信号 sig_in 的上升沿
    // 持续时长必须大于 1ms 即100 000 个时钟周期
    reg sig_in_posedge; // 用于记录输入信号上升沿的到达
    initial sig_in_posedge = 1'b0; // 初始一定为0

    //wire enable_count_sig_in;
    //and a2(enable_count_sig_in, enable_count); // 为了避免延时  记就完事了
    wire [31:0] sig_num_wire;
    //二进制加法器 IP核 vivado
    counter count_sig_in (
      .CLK(sig_in),  // input wire CLK
      .CE(enable_count),    // input wire CE
      .SCLR(out_valid),  // input wire SCLR
      .Q(sig_num_wire)      // output wire [31 : 0] Q
    );
    
    wire enable_count_clk;
    and a3(enable_count_clk, enable_count, sig_in_posedge);
    wire [31:0] clk_num_wire;
    //二进制加法器 IP核 vivado
    counter count_clk (
      .CLK(clk_in_100MHz),  // input wire CLK
      .CE(enable_count_clk),    // input wire CE
      .SCLR(out_valid),  // input wire SCLR
      .Q(clk_num_wire)      // output wire [31 : 0] Q
    );
    reg assign_flag; // 赋值标签  
    initial assign_flag = 1;
    always @(posedge sig_in)
        begin
            if (enable_count == 0)
                out_valid <= 0; // ready = 0 的时候 就输出无效了
                assign_flag <= 1; // 不能工作的时候 把它赋值为0
                
            if (enable_count == 1 && assign_flag)
                sig_in_posedge <= 1'b1; // 一定要阻塞式  当有上升沿后就标记有过上升沿
            if (sig_num_wire > 0 && clk_num_wire > 32'd100000 && assign_flag)
            // 结束标志  
                begin
                    clk_num <= clk_num_wire; 
                    sig_num <= sig_num_wire;
                    out_valid <= 1;
                    sig_in_posedge <= 1'b0; // 不能工作时  把它重新置为0
                    assign_flag <= 0; // 一次工作只能赋值一次
                end
            if (out_valid)
                assign_flag <= 0;

        end 
     
endmodule
