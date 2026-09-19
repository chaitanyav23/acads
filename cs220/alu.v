`timescale 1ns / 1ps

module alu(
    input [31:0] a,
    input [31:0] b,
    input [5:0] alu_control,
    output reg [31:0] result,
    output zero
);
    parameter ADD = 6'b100000, SUB = 6'b100010;
    parameter AND = 6'b100100, OR = 6'b100101;
    parameter XOR = 6'b100110, NOR = 6'b100111;
    parameter SLT = 6'b101010, SLTU = 6'b101011;
    parameter SLL = 6'b000000, SRL = 6'b000010, SRA = 6'b000011;
    
    assign zero = (result == 0);
    
    always @(*) begin
        case (alu_control)
            ADD: result = a + b;
            SUB: result = a - b;
            AND: result = a & b;
            OR:  result = a | b;
            XOR: result = a ^ b;
            NOR: result = ~(a | b);
            SLT: result = ($signed(a) < $signed(b)) ? 1 : 0;
            SLTU: result = (a < b) ? 1 : 0;
            SLL: result = b << a[4:0];
            SRL: result = b >> a[4:0];
            SRA: result = $signed(b) >>> a[4:0];
            default: result = 0;
        endcase
    end
endmodule
