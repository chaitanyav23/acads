#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<math.h>
#include<sys/time.h>
#include<sys/wait.h>

void long_to_str(long val , char *buff){
	char temp[32];
	int i= 0 , j =0;
       if(val == 0 ){
       	buff[0] = '0';
	buff[1] = '\0';
       return ;
       } 
	if(val<0) {
		buff[j++] = '-';
		val = -val;
		
	}       
      while(val > 0) {
      	temp[i++] ='0'+ (val%10);
	val /= 10;

      }
      while(i>0){
      	buff[j++] = temp[--i];
      }
      buff[j] ='\0';
      return;
}
int main(int argc, char **argv)
{
	int n = atoi(argv[1]);
	long long result = 1LL; 
	if(argc >= 3) result = atoi(argv[2]);
	if(n <= 1) {
		printf("%lld\n", result);
		return 0;
	} else if (n==2) {
		long long new_result = (long)2*result;
		printf("%lld\n", new_result);
		return 0;
	} else {
	long long new_result =(long) n * result;
	char argN[32] , argRES[64];
	long_to_str(n-1 , argN);
	long_to_str(new_result, argRES);
	execl("./fact", "./fact", argN, argRES, (char*)NULL);
	perror("execl");
	return 1;
	}
}
