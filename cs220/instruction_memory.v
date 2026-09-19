`timescale 1ns / 1ps

module instruction_memory(
    input [31:0] address,
    output [31:0] instruction
);
    reg [31:0] mem [0:1023];
    
    initial begin
        mem[0] = 32'h20010005;
        mem[1] = 32'h20020003;
        mem[100] = 32'h3c011f80;
        mem[200] = 32'h20010005;
    end
    
    assign instruction = mem[address[11:2]];
endmodule
