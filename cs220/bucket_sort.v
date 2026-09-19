`timescale 1ns / 1ps

module bucket_sort(
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
    reg [7:0] i, j, k;
    reg [31:0] max_val, array_size;
    
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
    parameter IDLE = 0, INIT = 1, COUNT = 2, RECONSTRUCT = 3, DONE = 4;
    
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            state <= IDLE;
            done <= 0;
            mem_write_en <= 0;
            reg_write_en <= 0;
        end else begin
            case (state)
                IDLE: begin
                    array_size <= 8;  // Size of array to sort
                    max_val <= 5;     // Maximum value in array
                    i <= 0;
                    j <= 0;
                    k <= 0;
                    state <= INIT;
                end
                
                INIT: begin
                    if (i <= max_val) begin
                        mem_addr <= 256 + (i << 2);
                        mem_write_data <= 0;
                        mem_write_en <= 1;
                        i <= i + 1;
                    end else begin
                        mem_write_en <= 0;
                        i <= 0;
                        state <= COUNT;
                    end
                end
                
                COUNT: begin
                    if (i < array_size) begin
                        mem_addr <= i << 2;
                        #1;
                        mem_addr <= 256 + (mem_read_data << 2);
                        #1;
                        mem_write_data <= mem_read_data + 1;
                        mem_write_en <= 1;
                        i <= i + 1;
                    end else begin
                        mem_write_en <= 0;
                        i <= 0;
                        j <= 0;
                        state <= RECONSTRUCT;
                    end
                end
                
                RECONSTRUCT: begin
                    if (j <= max_val) begin
                        mem_addr <= 256 + (j << 2);
                        #1;
                        
                        if (mem_read_data > 0) begin
                            mem_addr <= k << 2;
                            mem_write_data <= j;
                            mem_write_en <= 1;
                            
                            mem_addr <= 256 + (j << 2);
                            mem_write_data <= mem_read_data - 1;
                            mem_write_en <= 1;
                            
                            k <= k + 1;
                        end else begin
                            j <= j + 1;
                        end
                    end else begin
                        mem_write_en <= 0;
                        state <= DONE;
                    end
                end
                
                DONE: begin
                    done <= 1;
                end
            endcase
        end
    end
endmodule
