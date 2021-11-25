`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2019/07/30 22:11:15
// Design Name: 
// Module Name: top
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


module top(
input CLK_IN,
input RESET,
input FPGA_KEY,
output OUT1,
output [7:0] LED
    );
    wire clk_50;
  clk_wiz_0 pll(
    .clk_in1(CLK_IN),
    .clk_out1(clk_50)
  );  
    
    reg [95:0] data;
    
    wire rx_int;
    
    wire [7:0] recv_data;
    assign LED = recv_data;
    
    recv_uart(
        .clk_50(clk_50),
        .rst_n(RESET),
        .rx(FPGA_KEY),
        ////////////////////
        .rx_data(recv_data), 
        .valid(rx_int) //上升沿触发接收
    );

    reg tx_int;
    wire busy;
    reg last_rx;
    
    always @(posedge CLK_IN or negedge RESET) begin
        if(!RESET) begin
            tx_int=1'b0;
            data=95'd15;
            last_rx = 1'b0; //上升沿触发        
        end
        else begin
            if(rx_int & (!last_rx)) begin
                tx_int=1'b1;//触发
            end
            last_rx=rx_int;
            
            if(tx_int & busy) begin //成功正在发送
                tx_int = 1'b0;
            end
        end
    
    end
    
    ctrl_uart(
    .clk_50(clk_50),
    .rst_n(RESET),
    .data(data),
    .en(tx_int),  //上升沿触发发送
    /////////////////////////
    .tx(OUT1),
    .busy(busy)
    );


    
endmodule
