#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>
#include <float.h>
#include <limits.h>
#include <time.h>

// #pragma prutor-mpi-args: -np 32 -ppn 4
// #pragma prutor-mpi-sysargs: 100000 2 4 5 1000

#define TAG_FWD_D1 100
#define TAG_FWD_D2 101
#define TAG_BWD_D1 200
#define TAG_BWD_D2 201
#define TAG_FINAL 300

int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv);
    MPI_Status status;
    int my_rank, P, bucket1, bucket2;
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &P);
    

    if (argc < 6) {
        if (my_rank == 0) fprintf(stderr, "Usage: %s M D1 D2 T seed\n", argv[0]);
        MPI_Finalize();
        return EXIT_FAILURE;
    }

    int M = atoi(argv[1]);
    int D1 = atoi(argv[2]);
    int D2 = atoi(argv[3]);
    int T = atoi(argv[4]);
    int seed = atoi(argv[5]);

    bucket1 = (my_rank/D1);
    bucket2 = (my_rank/D2);

    if (M <= 0 || D1 <= 0 || D2 <= 0 || T < 0) {
        if (my_rank == 0) fprintf(stderr, "Error: M, D1, D2 must be positive and T >= 0\n");
        MPI_Finalize();
        return EXIT_FAILURE;
    }
    if (!(D1 < D2)) {
        if (my_rank == 0) fprintf(stderr, "Error: require D1 < D2\n");
        MPI_Finalize();
        return EXIT_FAILURE;
    }

    // allocate
    double *data_received   = (double*)malloc(M * sizeof(double));
    double *send_to_D1      = (double*)malloc(M * sizeof(double));
    double *send_to_D2      = (double*)malloc(M * sizeof(double));
    double *recv_from_D1    = (double*)malloc(M * sizeof(double));
    double *recv_from_D2    = (double*)malloc(M * sizeof(double));
    double *return_back_D1  = (double*)malloc(M * sizeof(double));
    double *return_back_D2  = (double*)malloc(M * sizeof(double));

    // init
    srand(seed);
    for (int i = 0; i < M; ++i) {
        data_received[i] = (double)rand() * (my_rank + 1) / 10000.0;
        send_to_D1[i] = data_received[i];
        send_to_D2[i] = data_received[i];
        return_back_D1[i] = 0.0;
        return_back_D2[i] = 0.0;
    }

    double start_time = MPI_Wtime();

    for (int iter = 0; iter < T; ++iter) {

        // =================================================================
        // PHASE 1: D1 INTERACTION (Forward -> Compute -> Backward)
        // =================================================================
        
        // --- 1.1 Forward Pass (Send data to Right / Recv data from Left) ---
        if (bucket1 % 2 == 0) {
            // Even Bucket: Send Right First, Then Recv Left
            if (my_rank + D1 < P) {
                MPI_Send(send_to_D1, M, MPI_DOUBLE, my_rank + D1, TAG_FWD_D1, MPI_COMM_WORLD);
            }
            if (my_rank - D1 >= 0) {
                MPI_Recv(recv_from_D1, M, MPI_DOUBLE, my_rank - D1, TAG_FWD_D1, MPI_COMM_WORLD, &status);
            }
        } else {
            // Odd Bucket: Recv Left First, Then Send Right
            if (my_rank - D1 >= 0) {
                MPI_Recv(recv_from_D1, M, MPI_DOUBLE, my_rank - D1, TAG_FWD_D1, MPI_COMM_WORLD, &status);
            }
            if (my_rank + D1 < P) {
                MPI_Send(send_to_D1, M, MPI_DOUBLE, my_rank + D1, TAG_FWD_D1, MPI_COMM_WORLD);
            }
        }

        // --- 1.2 Computation at Receiver (D1 Logic) ---
        if (my_rank - D1 >= 0) {
            for (int i = 0; i < M; ++i) recv_from_D1[i] = recv_from_D1[i] * recv_from_D1[i];
        }

        // --- 1.3 Backward Pass (Send result to Left / Recv result from Right) ---
        if (bucket1 % 2 == 0) {
            // Even Bucket: Recv Right First (matches Odd's Send), Then Send Left
            if (my_rank + D1 < P) {
                MPI_Recv(return_back_D1, M, MPI_DOUBLE, my_rank + D1, TAG_BWD_D1, MPI_COMM_WORLD, &status);
            }
            if (my_rank - D1 >= 0) {
                MPI_Send(recv_from_D1, M, MPI_DOUBLE, my_rank - D1, TAG_BWD_D1, MPI_COMM_WORLD);
            }
        } else {
            // Odd Bucket: Send Left First, Then Recv Right
            if (my_rank - D1 >= 0) {
                MPI_Send(recv_from_D1, M, MPI_DOUBLE, my_rank - D1, TAG_BWD_D1, MPI_COMM_WORLD);
            }
            if (my_rank + D1 < P) {
                MPI_Recv(return_back_D1, M, MPI_DOUBLE, my_rank + D1, TAG_BWD_D1, MPI_COMM_WORLD, &status);
            }
        }

        // =================================================================
        // PHASE 2: D2 INTERACTION (Forward -> Compute -> Backward)
        // =================================================================

        // --- 2.1 Forward Pass (Send data to Right / Recv data from Left) ---
        if (bucket2 % 2 == 0) {
            // Even Bucket: Send Right, Then Recv Left
            if (my_rank + D2 < P) {
                MPI_Send(send_to_D2, M, MPI_DOUBLE, my_rank + D2, TAG_FWD_D2, MPI_COMM_WORLD);
            }
            if (my_rank - D2 >= 0) {
                MPI_Recv(recv_from_D2, M, MPI_DOUBLE, my_rank - D2, TAG_FWD_D2, MPI_COMM_WORLD, &status);
            }
        } else {
            // Odd Bucket: Recv Left, Then Send Right
            if (my_rank - D2 >= 0) {
                MPI_Recv(recv_from_D2, M, MPI_DOUBLE, my_rank - D2, TAG_FWD_D2, MPI_COMM_WORLD, &status);
            }
            if (my_rank + D2 < P) {
                MPI_Send(send_to_D2, M, MPI_DOUBLE, my_rank + D2, TAG_FWD_D2, MPI_COMM_WORLD);
            }
        }

        // --- 2.2 Computation at Receiver (D2 Logic) ---
        if (my_rank - D2 >= 0) {
            for (int i = 0; i < M; ++i) {
                if (recv_from_D2[i] > 0.0) recv_from_D2[i] = log(recv_from_D2[i]);
                else recv_from_D2[i] = 0.0;
            }
        }

        // --- 2.3 Backward Pass (Send result to Left / Recv result from Right) ---
        if (bucket2 % 2 == 0) {
            // Even Bucket: Recv Right, Then Send Left
            if (my_rank + D2 < P) {
                MPI_Recv(return_back_D2, M, MPI_DOUBLE, my_rank + D2, TAG_BWD_D2, MPI_COMM_WORLD, &status);
            }
            if (my_rank - D2 >= 0) {
                MPI_Send(recv_from_D2, M, MPI_DOUBLE, my_rank - D2, TAG_BWD_D2, MPI_COMM_WORLD);
            }
        } else {
            // Odd Bucket: Send Left, Then Recv Right
            if (my_rank - D2 >= 0) {
                MPI_Send(recv_from_D2, M, MPI_DOUBLE, my_rank - D2, TAG_BWD_D2, MPI_COMM_WORLD);
            }
            if (my_rank + D2 < P) {
                MPI_Recv(return_back_D2, M, MPI_DOUBLE, my_rank + D2, TAG_BWD_D2, MPI_COMM_WORLD, &status);
            }
        }

        // =================================================================
        // PHASE 4: Update at sender
        // =================================================================
        if(my_rank + D1 < P){
            // Prepare buffers for NEXT iteration
            for(int i = 0; i < M; i++){
                // Logic: buffer_updated_for_D1 = (ulong)data % 100000
                send_to_D1[i] = (double)((unsigned long long)return_back_D1[i] % 100000ULL);
                
                // Logic: buffer_updated_for_D2 = data * 100000
                if(my_rank + D2 < P) send_to_D2[i] = return_back_D2[i] * 100000.0;
            }
        }
        
    } // end iterations
    
    double val_to_reduce[2] = {-INFINITY, -INFINITY};

    // 2. Load actual computed data if I am a valid sender
    if (my_rank + D1 < P) {
        for (int i = 0; i < M; ++i) {
            if (return_back_D1[i] > val_to_reduce[0]) val_to_reduce[0] = return_back_D1[i];
        }
    }
    if (my_rank + D2 < P) {
        for (int i = 0; i < M; ++i) {
            if (return_back_D2[i] > val_to_reduce[1]) val_to_reduce[1] = return_back_D2[i];
        }
    }

    // 3. Binary Tree Reduction Loop
    // Loop steps: 1, 2, 4, 8... until step >= P
    for (int step = 1; step < P; step *= 2) {
        
        // Receiver Logic: I stay active if I am divisible by (2 * step)
        if (my_rank % (2 * step) == 0) {
            int source = my_rank + step;
            
            // Check if the source exists (handle non-power-of-2 processes)
            if (source < P) {
                double incoming[2];
                MPI_Recv(incoming, 2, MPI_DOUBLE, source, TAG_FINAL, MPI_COMM_WORLD, &status);
                
                // Perform the MAX operation locally
                if (incoming[0] > val_to_reduce[0]) val_to_reduce[0] = incoming[0];
                if (incoming[1] > val_to_reduce[1]) val_to_reduce[1] = incoming[1];
            }
        } 
        // Sender Logic: I send if I am divisible by 'step' (but failed the check above)
        else if (my_rank % step == 0) {
            int dest = my_rank - step;
            
            // Send my current accumulated max to the destination
            MPI_Send(val_to_reduce, 2, MPI_DOUBLE, dest, TAG_FINAL, MPI_COMM_WORLD);
            
            // Once I send, I have passed my data up the tree. I am done.
            break; 
        }
    }

    double end_time = MPI_Wtime(); 
    double local_elapsed_time = end_time - start_time;
    double max_elapsed_time;

    // We use standard MPI_Reduce for time to get the slowest process time
    MPI_Reduce(&local_elapsed_time, &max_elapsed_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    if (my_rank == 0) {
        // At this point, val_to_reduce holds the Global Max because Rank 0 is the root of the tree
        printf("%f %f %f\n", val_to_reduce[0], val_to_reduce[1], max_elapsed_time);
    }

    // clean up
    free(data_received);
    free(send_to_D1); free(send_to_D2);
    free(recv_from_D1); free(recv_from_D2);
    free(return_back_D1); free(return_back_D2);

    MPI_Finalize();
    return 0;
}
