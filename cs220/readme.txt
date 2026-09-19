IITK-Mini-MIPS Processor Implementation
=======================================

Project Overview
----------------
Complete Verilog implementation of IITK-Mini-MIPS processor with:
- Bucket Sort and Insertion Sort algorithms
- Floating-point operations
- Integer multiplication
- Single-cycle execution architecture
- MIPS-32 ISA with 32 general-purpose registers

Repository Structure
--------------------
IITK-Mini-MIPS/
├── src/                  # Verilog source files
│   ├── alu.v            # Arithmetic Logic Unit
│   ├── control_unit.v   # Control Unit
│   ├── cpu.v           # Top-level CPU
│   ├── data_memory.v   # Data Memory
│   ├── fpu.v          # Floating Point Unit
│   ├── instruction_memory.v # Instruction Memory
│   ├── mips_registers.v    # Register File
│   ├── program_counter.v   # Program Counter
│   ├── bucket_sort.v      # Bucket Sort
│   └── insertion_sort.v   # Insertion Sort
├── test/                # Test benches
│   ├── alu_tb.v        # ALU Test
│   ├── cpu_tb.v       # CPU Test
│   ├── fpu_tb.v      # FPU Test
│   ├── bucket_sort_tb.v    # Bucket Sort Test
│   ├── insertion_sort_tb.v # Insertion Sort Test
│   ├── fp_sub_tb.v        # FP Subtraction
│   └── int_mul_tb.v      # Integer Multiplication

Key Features
------------
1. Core Processor:
- Single-cycle 32-bit RISC
- Harvard architecture
- 32 general registers

2. Sorting Algorithms:
- Bucket Sort (bucket_sort.v)
  - O(n) best case
  - Uses counting approach
- Insertion Sort (insertion_sort.v)
  - In-place sorting
  - O(n^2) worst case

3. Arithmetic Operations:
- Integer: ADD, SUB, MUL
- Floating Point: ADD, SUB
- Signed/unsigned variants

Getting Started
--------------
Prerequisites:
- Icarus Verilog (iverilog)
- GTKWave (optional)

Compile & Run:
# Bucket Sort
iverilog -o bucket_test test/bucket_sort_tb.v src/bucket_sort.v src/data_memory.v src/mips_registers.v
vvp bucket_test

# Insertion Sort
iverilog -o insert_test test/insertion_sort_tb.v src/insertion_sort.v src/data_memory.v src/mips_registers.v
vvp insert_test

# FP Subtraction
iverilog -o fp_sub_test test/fp_sub_tb.v src/cpu.v src/*.v
vvp fp_sub_test

# Integer Multiply
iverilog -o mul_test test/int_mul_tb.v src/cpu.v src/*.v
vvp mul_test

Implementation Details
----------------------
Memory Organization:
- Instruction: 1KB, word-aligned
- Data: 1KB, initialized with test patterns
- Bucket Sort uses addresses:
  - Input: 0-31
  - Buckets: 256-511

Test Data:
- Sorting: [5,3,2,5,1,4,0,3]
- FP: 1.0 - 0.5 = 0.5
- Int: 5 * 10 = 50

Expected Outputs
---------------
Sorting Algorithms:
mem[0] = 0
mem[1] = 1
mem[2] = 2
mem[3] = 3
mem[4] = 3
mem[5] = 4
mem[6] = 5
mem[7] = 5

Arithmetic:
FP Subtraction: 3f000000 (0.5)
Integer Multiply: 50

Additional Notes
---------------
- All modules include reset functionality
- Test benches verify timing and correctness
- Memory is word-addressable (4 bytes/address)
- Processor executes 1 instruction/cycle