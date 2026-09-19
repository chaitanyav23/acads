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
        // Initialize test array [5, 3, 2, 5, 1, 4, 0, 3]
        mem[0] = 5;
        mem[1] = 3;
        mem[2] = 2;
        mem[3] = 5;
        mem[4] = 1;
        mem[5] = 4;
        mem[6] = 0;
        mem[7] = 3;
        
        // Initialize buckets area to 0
        for (integer i = 256; i < 512; i = i + 1)
            mem[i] = 0;
    end
    
    always @(posedge clk) begin
        if (mem_write)
            mem[address] <= write_data;
        if (mem_read)
            read_data <= mem[address];
    end
endmodule
