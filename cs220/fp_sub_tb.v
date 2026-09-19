`timescale 1ns / 1ps

module fp_sub_tb;
    reg clk, reset;
    cpu uut(.clk(clk), .reset(reset));
    
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    initial begin
        reset = 1;
        #20 reset = 0;
        #200;
        $display("FP Sub Result: %h", uut.dmem.mem[102]);
        $finish;
    end
endmodule
