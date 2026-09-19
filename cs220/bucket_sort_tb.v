`timescale 1ns / 1ps

module bucket_sort_tb;
    reg clk;
    reg reset;
    wire done;
    
    bucket_sort uut(
        .clk(clk),
        .reset(reset),
        .done(done)
    );
    
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    initial begin
        reset = 1;
        #20 reset = 0;
        
        wait(done);
        
        $display("Bucket Sort Results:");
        $display("mem[0] = %d", uut.dmem.mem[0]);
        $display("mem[1] = %d", uut.dmem.mem[1]);
        $display("mem[2] = %d", uut.dmem.mem[2]);
        $display("mem[3] = %d", uut.dmem.mem[3]);
        $display("mem[4] = %d", uut.dmem.mem[4]);
        $display("mem[5] = %d", uut.dmem.mem[5]);
        $display("mem[6] = %d", uut.dmem.mem[6]);
        $display("mem[7] = %d", uut.dmem.mem[7]);
        
        $finish;
    end
endmodule
