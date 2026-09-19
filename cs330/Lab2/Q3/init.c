#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

static int solve(const char* hay, const char *needle, int slen , int hlen ){
	if(slen == 0 || slen > hlen) return 0;
	for(int i =0 ; i +slen < hlen ; i++){
		int j =0 ;		while(j < slen && hay[i+j]== needle[j])	j++;
	if(j == slen)return 1;
	} 	return 0;
}
int main (int argc, char **argv) {
	if(argc != 3){printf("Error\n");		exit(0);}
	const char *fileName = argv[2];
	const char *search = argv[1]; 
	int slen = strlen(search);
	if(slen == 0){   printf("Error\n");     exit(0);}
	int fd = open(fileName, O_RDONLY);
	if(fd < 0 ) {printf("Error\n");exit(0);}
	off_t end = lseek(fd, 0 , SEEK_END);
	if(end == (off_t)-1){		close(fd);	printf("Error\n");     exit(0);	}
	lseek(fd, 0, SEEK_SET) ;
	int f_size = (int)end;
	char *buff =(char *)malloc(f_size+1);
	if(!buff){  close(fd);   printf("Error\n");    exit(0);       }
	int g = 0 ; 
	while(g<f_size){
		ssize_t n = read(fd, buff+g, f_size-g);
		if(n< 0){ free(buff);  close(fd);  printf("Error\n");   exit(0); }  if(n==0) break;
		g+=n;
	}
	buff[g] = '\0';
	if(close(fd)<0){ free(buff);   	printf("Error\n");   exit(0);    }
	int found = solve(buff, search , slen, g );
	if(found) {
		printf("FOUND\n");

	}
	else{
		printf("NOT FOUND\n");
	}
	free(buff);

 
    return 0;
}
