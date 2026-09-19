#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

typedef long long ll;

int R;        
int NY2, NZ2; 

static inline int idxMapping(int i, int j, int k){
    return i * NY2 * NZ2 + j * NZ2 + k;
}

// halo exchange prototype, using zero-copy indexed datatypes.
void haloExchange(double *arr, int nx, int ny, int nz, int west,  int east, int south, 
                    int north, int back,  int front, MPI_Datatype typeX, MPI_Datatype typeY, MPI_Datatype typeZ){

    MPI_Request reqs[4];
    int nreqs;

    // X-axis neighbors  (communication of the Y-Z planes) east-west
    nreqs = 0;
    if (west >= 0) {
        MPI_Isend(&arr[idxMapping(R, R, R)], 1, typeX, west, 0, MPI_COMM_WORLD, &reqs[nreqs++]);
        MPI_Irecv(&arr[idxMapping(0, R, R)], 1, typeX, west, 1, MPI_COMM_WORLD, &reqs[nreqs++]);
    }
    if (east >= 0) {
        MPI_Isend(&arr[idxMapping(nx, R, R)], 1, typeX, east, 1, MPI_COMM_WORLD, &reqs[nreqs++]);
        MPI_Irecv(&arr[idxMapping(nx + R, R, R)], 1, typeX, east, 0, MPI_COMM_WORLD, &reqs[nreqs++]);
    }
    MPI_Waitall(nreqs, reqs, MPI_STATUSES_IGNORE);

    // y-axis neighbors  (communication of the X-Z planes) north-south
    // also shifting the base pointers starting from X=0
    nreqs = 0;
    if (south >= 0) {
        MPI_Isend(&arr[idxMapping(0, R, R)], 1, typeY, south, 2, MPI_COMM_WORLD, &reqs[nreqs++]);
        MPI_Irecv(&arr[idxMapping(0, 0, R)], 1, typeY, south, 3, MPI_COMM_WORLD, &reqs[nreqs++]);
    }
    if (north >= 0) {
        MPI_Isend(&arr[idxMapping(0, ny, R)], 1, typeY, north, 3, MPI_COMM_WORLD, &reqs[nreqs++]);
        MPI_Irecv(&arr[idxMapping(0, ny + R, R)], 1, typeY, north, 2, MPI_COMM_WORLD, &reqs[nreqs++]);
    }
    MPI_Waitall(nreqs, reqs, MPI_STATUSES_IGNORE);

    // Z-axis neighbors  (communication of the X-Y planes) back-front
    // also shifting the base pointers starting from X=0, Y=0 to include all ghost layers in the Z-face exchange.
    nreqs = 0;
    if (back >= 0) {
        MPI_Isend(&arr[idxMapping(0, 0, R)], 1, typeZ, back, 4, MPI_COMM_WORLD, &reqs[nreqs++]);
        MPI_Irecv(&arr[idxMapping(0, 0, 0)], 1, typeZ, back, 5, MPI_COMM_WORLD, &reqs[nreqs++]);
    }
    if (front >= 0) {
        MPI_Isend(&arr[idxMapping(0, 0, nz)], 1, typeZ, front, 5, MPI_COMM_WORLD, &reqs[nreqs++]);
        MPI_Irecv(&arr[idxMapping(0, 0, nz + R)], 1, typeZ, front, 4, MPI_COMM_WORLD, &reqs[nreqs++]);
    }
    MPI_Waitall(nreqs, reqs, MPI_STATUSES_IGNORE);
}

int main(int argc, char **argv){
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // reading the inputs parameters
    int d = atoi(argv[1]);
    int ppn = atoi(argv[2]); 
    int px = atoi(argv[3]);
    int py = atoi(argv[4]);
    int pz = atoi(argv[5]);
    int nx = atoi(argv[6]);
    int ny = atoi(argv[7]);
    int nz = atoi(argv[8]);
    int T = atoi(argv[9]);
    int seed = atoi(argv[10]);
    int F = atoi(argv[11]);
    double isoValue = atof(argv[12]);

    // computing the depth of halo layer
    R = (d-1)/6;  
    NY2 = ny+2*R;       
    NZ2 = nz+2*R;

    // computing the 3D coordinates of the process in the process grid
    int cx = rank/(py*pz);
    int cy = (rank/pz)%py;
    int cz = rank%pz;

    // comunication neighbors
    int west  = (cx > 0)? rank- py * pz:-1;
    int east  = (cx < px - 1)? rank+py*pz :-1;
    int south = (cy > 0) ? rank - pz: -1;
    int north = (cy < py - 1)? rank + pz: -1;
    int back  = (cz > 0) ? rank-1: -1;
    int front = (cz < pz - 1)? rank + 1: -1;

    int memSize = (nx + 2 * R) * (ny + 2 * R) * (nz + 2 * R);
    int arrSize = nx * ny * nz;

    //forming manual indexed datatypes for halo exchange, creating 3D block shapes explicitly
    MPI_Datatype typeX, typeY, typeZ;
    
    // allocating max required memory for block lengths and displacements
    int max_blocks = (nx + 2 * R) * (ny + 2 * R);
    int *blens = malloc(max_blocks * sizeof(int));
    int *disps = malloc(max_blocks * sizeof(int));
    int count, idx;

    // X Faces, blocks of size (R, ny, nz)
    count = R * ny;
    idx = 0;
    for (int i = 0; i < R; i++) {
        for (int j = 0; j < ny; j++) {
            blens[idx] = nz;
            disps[idx] = i * NY2 * NZ2 + j * NZ2; // Memory offset logic
            idx++;
        }
    }
    MPI_Type_indexed(count, blens, disps, MPI_DOUBLE, &typeX);
    MPI_Type_commit(&typeX);

    //Y Faces, blocks of size (nx+2R, R, nz)
    count = (nx + 2 * R) * R;
    idx = 0;
    for (int i = 0; i < nx + 2 * R; i++) {
        for (int j = 0; j < R; j++) {
            blens[idx] = nz;
            disps[idx] = i * NY2 * NZ2 + j * NZ2;
            idx++;
        }
    }
    MPI_Type_indexed(count, blens, disps, MPI_DOUBLE, &typeY);
    MPI_Type_commit(&typeY);

    // Z faces, blocks of size (nx+2R, ny+2R, R)
    count = (nx + 2 * R) * (ny + 2 * R);
    idx = 0;
    for (int i = 0; i < nx + 2 * R; i++) {
        for (int j = 0; j < ny + 2 * R; j++) {
            blens[idx] = R;
            disps[idx] = i * NY2 * NZ2 + j * NZ2;
            idx++;
        }
    }
    MPI_Type_indexed(count, blens, disps, MPI_DOUBLE, &typeZ);
    MPI_Type_commit(&typeZ);

    // freeing temp arrays for memory optimization
    free(blens);
    free(disps);

    double **data = malloc(F * sizeof(double *));
    double **next = malloc(F * sizeof(double *));
    for (int i = 0; i < F; i++) {
        data[i] = calloc(memSize, sizeof(double));
        next[i] = calloc(memSize, sizeof(double));
    }

    ll *localCount  = malloc(F * sizeof(ll));
    ll *globalCounts = malloc(F * sizeof(ll));
    ll *stepCounts = (rank == 0) ? malloc(T*F*sizeof(ll)) : NULL;

    srand(seed);
    for (int i = 0;i<F;i++) {
        for (int j=0; j<arrSize; j++) {
            int lx = j/(ny*nz);
            int ly = (j/nz)%ny;
            int lz = j%nz;
            data[i][idxMapping(lx+R,ly+R,lz+R)] = (double)rand()*(rank+1)/(110426.0+i+j);
        }
    }

    double start_time = MPI_Wtime();

    // primer halo exchange
    for (int f=0;f<F; f++) {
        haloExchange(data[f], nx, ny, nz, west, east, south, north, back, front, typeX, typeY, typeZ);
    }

    for (int t=0;t<T; t++) {
        for (int f = 0; f < F; f++) {
            localCount[f] = 0;

            // step1 - d-point stencil (radius Loop)
            for (int i = R; i < nx+R; i++) {
                for (int j = R;j<ny+R; j++) {
                    for (int k = R;k<nz+R; k++) {
                        double sum = data[f][idxMapping(i, j, k)];
                        int m = 1;

                        for (int rad = 1; rad <= R; rad++) {
                            if (i - rad >= R || cx > 0){
                                sum += data[f][idxMapping(i - rad, j, k)];
                                m++; 
                            }
                            
                            if (i+rad<nx+R||cx<px-1){
                                sum += data[f][idxMapping(i + rad, j, k)];
                                m++;
                            }
                            
                            if (j - rad >= R || cy > 0){
                                sum += data[f][idxMapping(i, j-rad, k)];
                                m++; 
                            }
                            
                            if (j+rad<ny+R || cy<py-1){
                                sum += data[f][idxMapping(i, j+rad, k)];
                                m++; 
                            }
                            
                            if (k - rad >= R || cz>0){
                                sum += data[f][idxMapping(i, j, k-rad)];
                                m++; 
                            }
                            
                            if (k+rad<nz+R || cz<pz-1){
                                sum += data[f][idxMapping(i, j, k+rad)];
                                m++; 
                            }
                        }
                        next[f][idxMapping(i, j, k)] = sum/m;
                    }
                }
            }

           // step2 - halo exchange on next[]   
            haloExchange(next[f], nx, ny, nz, west, east, south, north, back, front, typeX, typeY, typeZ);

            // step3 - isoValue counting
            for (int i = R;i<nx+R; i++) {
                for (int j = R;j<ny+R;j++) {
                    for (int k = R;k<nz + R; k++) {
                        double val = next[f][idxMapping(i, j, k)];

                        if (i<nx+R-1||cx<px-1) {
                            double ve = next[f][idxMapping(i + 1, j, k)];
                            if ((val <= isoValue && ve >isoValue) || (val >= isoValue && ve <isoValue)) localCount[f]++;
                        }
                        if (j<ny+R-1||cy<py-1) {
                            double vn = next[f][idxMapping(i, j+1, k)];
                            if ((val <= isoValue && vn>isoValue) || (val >= isoValue && vn <isoValue)) localCount[f]++;
                        }
                        if (k < nz+R-1 || cz<pz-1) {
                            double vfr = next[f][idxMapping(i,j,k+1)];
                            if ((val <= isoValue && vfr >isoValue) || (val >= isoValue && vfr<isoValue)) localCount[f]++;
                        }
                    }
                }
            }
        } 

        MPI_Reduce(localCount, globalCounts, F, MPI_LONG_LONG, MPI_SUM, 0, MPI_COMM_WORLD);

        if (rank == 0){
            for (int i=0; i<F; i++){
                stepCounts[t*F+i] = globalCounts[i];
            }
        }

        for (int f = 0; f < F; f++) {
            double *tmp = data[f];
            data[f]= next[f];
            next[f] = tmp;
        }
    } 

    double elapsedTime = MPI_Wtime() - start_time;

    if (rank == 0) {
        for (int t = 0; t < T; t++) {
            for (int f = 0; f < F; f++)
                printf("%lld ", stepCounts[t * F + f]);
            printf("\n");
        }
        printf("%f\n", elapsedTime);
    }

    // freeing MPI datatypes
    MPI_Type_free(&typeX);
    MPI_Type_free(&typeY);
    MPI_Type_free(&typeZ);

    // freeing allocated memory
    for (int i = 0; i < F; i++) { free(data[i]); free(next[i]); }
    free(data); free(next); 
    free(localCount); free(globalCounts);
    if (rank == 0) free(stepCounts);

    MPI_Finalize();
    return 0;
}