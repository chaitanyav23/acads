#include<stdio.h>
#include<fcntl.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>

int main(int argc, char **argv)
{
	if( argc!=2) {
		printf("Unable to execute\n");
		return 0;
	} 
	const char* path = argv[1] ;
	int fd = open(path, O_RDONLY);
	if(fd < 0){
                printf("Unable to execute\n");
                return 0;
        }
	int A = 0 , B=0 , C =0 , D=0 , E=0,F =0; 
	char buff[8192] ;	ssize_t n ;	char line[8192]; 	int pos = 0;
	while((n = read(fd, buff , sizeof(buff)))> 0 ){
		for(ssize_t i = 0 ; i < n ; i++){
			line[pos++] = buff[i];
			if(buff[i] == '\n' || pos == (int)sizeof(line)-1 ){
				line[pos] = '\0';
				pos = 0;
				if(strstr(line, " openat(") == line+ strcspn(line, " ")){ A++;}
				if(strstr(line, " close(") == line+ strcspn(line, " ")){ B++;}
				if(strstr(line, " read(") == line+ strcspn(line, " ")){ C++;}
				if(strstr(line, " write(") == line+ strcspn(line, " ")){ D++;}
				if(strstr(line, " stat(") == line+ strcspn(line, " ")){ E++;}
				if(strstr(line, " execve(") == line+ strcspn(line, " ")){ F++;}
			}
			
		}
	}
	if(n < 0 ){ close(fd); printf("Unable to execute\n");   return 0;	}
	if(close(fd) < 0){ printf("Unable to execute\n");      return 0;	}
	printf("openat: %d\n",A );        printf("close: %d\n",B );        printf("read: %d\n",C );
        printf("write: %d\n",D );        printf("stat: %d\n",E );        printf("execve: %d\n",F ); 
  return 0;
}
