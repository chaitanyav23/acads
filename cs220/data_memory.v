`timescale 1ns / 1ps

module data_memory(
    input clk,
    input mem_read,
    input mem_write,
    input [31:0] address,
    input [31:0] write_data,
    output reg [31:0] read_data
);
    reg [31:0] mem [0:1023];
    
    initial begin
        mem[0] = 5; mem[1] = 3; mem[2] = 2;
        mem[100] = 32'h3f800000;
        mem[200] = 5;
    end
    
    always @(posedge clk) begin
        if (mem_write)
            mem[address[11:2]] <= write_data;
        if (mem_read)
            read_data <= mem[address[11:2]];
    end
endmodule
