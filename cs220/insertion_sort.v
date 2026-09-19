`timescale 1ns / 1ps

module insertion_sort(
    input clk,
    input reset,
    output reg done
);
    // Memory interface
    reg [31:0] mem_addr;
    reg [31:0] mem_write_data;
    reg mem_write_en;
    wire [31:0] mem_read_data;
    
    // Register file
    reg [4:0] reg_addr;
    reg [31:0] reg_write_data;
    reg reg_write_en;
    wire [31:0] reg_read_data;
    
    // Control signals
    reg [3:0] state;
    reg [7:0] i, j;
    reg [31:0] key, array_j;
    
    // Memory instance
    data_memory dmem(
        .clk(clk),
        .mem_read(1'b1),
        .mem_write(mem_write_en),
        .address(mem_addr),
        .write_data(mem_write_data),
        .read_data(mem_read_data)
    );
    
    // Register file instance
    mips_registers reg_file(
        .clk(clk),
        .reset(reset),
        .read_reg1(reg_addr),
        .read_reg2(5'b0),
        .write_reg(reg_addr),
        .write_data(reg_write_data),
        .reg_write(reg_write_en),
        .read_data1(reg_read_data),
        .read_data2()
    );
    
    // States
    parameter IDLE = 0, LOAD_KEY = 1, COMPARE = 2, SHIFT = 3, STORE_KEY = 4, DONE = 5;
    
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            state <= IDLE;
            done <= 0;
            mem_write_en <= 0;
            reg_write_en <= 0;
            i <= 1;  // Start with second element
            j <= 0;
        end else begin
            case (state)
                IDLE: begin
                    if (i < 8) begin
                        state <= LOAD_KEY;
                    end else begin
                        state <= DONE;
                    end
                end
                
                LOAD_KEY: begin
                    mem_addr <= i << 2;
                    #1;
                    key <= mem_read_data;
                    j <= i - 1;
                    state <= COMPARE;
                end
                
                COMPARE: begin
                    if (j >= 0) begin
                        mem_addr <= j << 2;
                        #1;
                        array_j <= mem_read_data;
                        
                        if (array_j > key) begin
                            state <= SHIFT;
                        end else begin
                            state <= STORE_KEY;
                        end
                    end else begin
                        state <= STORE_KEY;
                    end
                end
                
                SHIFT: begin
                    mem_addr <= (j + 1) << 2;
                    mem_write_data <= array_j;
                    mem_write_en <= 1;
                    
                    j <= j - 1;
                    state <= COMPARE;
                end
                
                STORE_KEY: begin
                    mem_addr <= (j + 1) << 2;
                    mem_write_data <= key;
                    mem_write_en <= 1;
                    
                    i <= i + 1;
                    state <= IDLE;
                end
                
                DONE: begin
                    done <= 1;
                end
            endcase
        end
    end
endmodule
