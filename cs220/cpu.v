`timescale 1ns / 1ps

module cpu(
    input clk,
    input reset
);
    wire [31:0] pc_next, pc_current;
    program_counter pc(
        .clk(clk),
        .reset(reset),
        .pc_in(pc_next),
        .pc_out(pc_current)
    );

    wire [31:0] instruction;
    instruction_memory imem(
        .address(pc_current),
        .instruction(instruction)
    );

    wire reg_dst, branch, mem_read, mem_to_reg, mem_write, alu_src, reg_write;
    wire jump, jal, jr, lui;
    wire [5:0] alu_op;
    control_unit ctrl(
        .opcode(instruction[31:26]),
        .funct(instruction[5:0]),
        .reg_dst(reg_dst),
        .branch(branch),
        .mem_read(mem_read),
        .mem_to_reg(mem_to_reg),
        .alu_op(alu_op),
        .mem_write(mem_write),
        .alu_src(alu_src),
        .reg_write(reg_write),
        .jump(jump),
        .jal(jal),
        .jr(jr),
        .lui(lui)
    );

    wire [31:0] read_data1, read_data2, write_data;
    wire [4:0] write_reg = reg_dst ? instruction[15:11] : 
                         jal ? 5'b11111 : 
                         instruction[20:16];

    mips_registers reg_file(
        .clk(clk),
        .reset(reset),
        .read_reg1(instruction[25:21]),
        .read_reg2(instruction[20:16]),
        .write_reg(write_reg),
        .write_data(write_data),
        .reg_write(reg_write),
        .read_data1(read_data1),
        .read_data2(read_data2)
    );

    wire [31:0] alu_result;
    wire zero;
    wire [31:0] alu_in2 = alu_src ? {{16{instruction[15]}}, instruction[15:0]} : read_data2;

    alu main_alu(
        .a(read_data1),
        .b(alu_in2),
        .alu_control(alu_op),
        .result(alu_result),
        .zero(zero)
    );

    wire [31:0] mem_read_data;
    data_memory dmem(
        .clk(clk),
        .mem_read(mem_read),
        .mem_write(mem_write),
        .address(alu_result),
        .write_data(read_data2),
        .read_data(mem_read_data)
    );

    assign write_data = mem_to_reg ? mem_read_data : 
                      jal ? pc_current + 4 : 
                      lui ? {instruction[15:0], 16'b0} : 
                      alu_result;

    wire [31:0] pc_plus_4 = pc_current + 4;
    wire [31:0] branch_target = pc_plus_4 + ({{14{instruction[15]}}, instruction[15:0], 2'b0});
    wire [31:0] jump_target = {pc_plus_4[31:28], instruction[25:0], 2'b0};
    wire branch_taken = branch & zero;

    assign pc_next = jr ? read_data1 : 
                    jump ? jump_target : 
                    branch_taken ? branch_target : 
                    pc_plus_4;

endmodule
