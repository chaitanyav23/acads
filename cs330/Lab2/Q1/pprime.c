#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<math.h>
#include<sys/time.h>
#include<sys/wait.h>


extern int isPrime(long x); // Returns zero if composite.
                            // Returns one if prime. You may use this if you want. 
int find_primes(long M)
{
	int count =0; 
	int s1, s2;
	long n1 = M/2;

	pid_t cpid1 = fork();


	if(cpid1 == -1 ){
		perror("fork");
               exit(EXIT_FAILURE);
	}
	if(cpid1== 0) {
		int ans = 0;
		for(int i =2 ; i <= n1; i++)	 if(isPrime(i)) ans++;
		exit(ans%256);
	}
	pid_t cpid2 = fork();
	if(cpid2 == -1 ) {
		perror("fork");
		exit(EXIT_FAILURE);
	}
	if(cpid2 == 0){
		int ans =0 ; 
		for(int i =(M/2)+1; i<= M; i++ ){
			if(isPrime(i)){
			ans++;
			}
		}
		exit(ans%256);
	}
	int total = 0;
	waitpid(cpid1, &s1, 0);
	waitpid(cpid2, &s2, 0);
	if(WEXITSTATUS(s1))total += WEXITSTATUS(s1); 
	if(WEXITSTATUS(s2))total += WEXITSTATUS(s2);
	return total%256;

   
}
