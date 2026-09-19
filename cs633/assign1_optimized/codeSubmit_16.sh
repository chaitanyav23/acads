#!/bin/bash
#SBATCH --job-name=main
#SBATCH -N 1 #### max limit now is 1
#SBATCH --ntasks-per-node=16  #### max limit now is 4
#SBATCH --output=main_%j.out
#SBATCH --error=main_%j.err
#SBATCH --partition=cpu
#SBATCH --time=00:05:00

module load compiler/oneapi-2024/mpi

D1=2
D2=4
T=10
seed=1000

# M values
for M in 262144 1048576
do
    # Repeat each configuration 5 times
    for run in 1 2 3 4 5
    do
        echo "Run $run with M=$M"
        mpirun -np 16 ./main $M $D1 $D2 $T $seed
    done
done
