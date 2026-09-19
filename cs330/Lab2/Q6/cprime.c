#include<stdio.h> 
#include<stdlib.h>
#include<unistd.h>
#include<math.h>
#include<sys/time.h>
#include<sys/wait.h>
#include<string.h>
#include<sys/syscall.h>
extern int isPrime(long x); 
long find_primes(int n, long M){
	if(n <= 0 || M < 2) {printf("0");return;}
	int pipes[n][2];
	pid_t pids[n];	int c = M / n;	int e = M % n;
	for(int i = 0; i < n; i++) {
		if(syscall(SYS_pipe, pipes[i]) < 0 ) {	perror("pipe");	exit(1);}
		pids[i] = fork();
		if(pids[i] < 0) {
			perror("fork");
			exit(1);
		}
		if(pids[i] == 0) {
			close(pipes[i][0]);
			
			int start = i*c + 1;
			int end = (i+1)*c;
			if( i == n-1 ) end += e;
			

			int cnt = 0;
			for(long x = start; x <= end && x <= M; x++) 
				if(isPrime(x))	cnt++;
			if(write(pipes[i][1], &cnt, sizeof(cnt)) < 0) {
				perror("write");
				exit(1);
			}
			close(pipes[i][1]);
			_exit(0);
		} else close(pipes[i][1]);
	}   
	long ans = 0;
	for(int i = 0; i < n; i++) {
		int cnt;
		if(read(pipes[i][0], &cnt, sizeof(cnt)) > 0)
			ans += cnt;
		close(pipes[i][0]);
	}
	for(int i = 0; i < n; i++)
		wait(NULL);
	return ans;
}
