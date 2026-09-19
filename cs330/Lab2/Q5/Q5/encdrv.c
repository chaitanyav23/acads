#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<fcntl.h>
#include<assert.h>
#include<string.h>
 //define As * 

static void erex(void) {
                printf("Error\n");
                exit(0);
 }


#define MAX_CHARS_IN_LINE 1000

int main(int argc, char **argv)
{
	char buff[MAX_CHARS_IN_LINE+1];
	char obuff[MAX_CHARS_IN_LINE+1];

// NOTE: Do not modify anything above this line	
/***
 *      Your Code goes here
 */

	if(argc != 3)	erex();
	const char *in_path = argv[1];
//	const char *out_path =argv[2];
	int in_fd = open(in_path, O_RDONLY);
	if(in_fd < 0)	{
		printf("1\n");

		erex();
	}
	
//	printf("%s\n", argv[2]);
	int out_fd = open(argv[2], O_CREAT|O_WRONLY|O_TRUNC, 0644);
	if(out_fd < 0)	{
		close(in_fd);
		printf("2\n");
		erex();
	}
//	exit(0);
	
	int p2c[2];
	int c2p[2];
	if(pipe(p2c) < 0) {
		close(in_fd);
		close(out_fd);
		printf("3\n");
		erex();
	}
	if(pipe(c2p) < 0) {
                close(in_fd);
                close(out_fd);
		close(p2c[0]);
		close(c2p[0]);
		printf("4\n");
		erex();
	}
	pid_t pid = fork();
	if(pid < 0) {
		close(in_fd); close(out_fd);
                close(p2c[0]); close(p2c[1]);
		close(c2p[0]); close(c2p[1]);
		printf("5\n");
		erex();
	}
	if(pid == 0) {
		if(dup2(p2c[0], 0) < 0) erex();
		if(dup2(c2p[1], 1) <0)	erex();
                close(p2c[0]); close(p2c[1]);
                close(c2p[0]); close(c2p[1]);
                close(in_fd); close(out_fd);
		execl("./encrypt", "./encrypt", (char  *) NULL);
		printf("6\n");
		erex();
	}
	close(p2c[0]);
	close(c2p[1]);
	auto int write_all(int fd ,const void *buff, size_t n   ){
		const char *p = (const char *)buff;
	       size_t left = n; 
       		while(left > 0){
			ssize_t w = write(fd, p , left);
			if(w <= 0){
				return -1; 
			}
			left -= (size_t)w;
		       p += w;	
		}
 		return 0;		

	}
	ssize_t used = 0;
	for(;;){
		char ch ; 
		ssize_t r = read(in_fd, &ch, 1 );
		if(r <0){
			printf("7\n");
			erex(); 
		}
		if(r == 0){
			if(used > 0) {
				char lenbuff[32];
				int m = sprintf(lenbuff, "%d\n", (int)used);
				if(m <= 0){
					printf("8\n");
					erex();
				}
				if(write_all(p2c[1], lenbuff, (size_t)m ) < 0)erex();
				if(write_all(p2c[1], buff, (size_t)used ) < 0)erex();
				ssize_t left = used;
				while(left > 0){
					ssize_t rr = read(c2p[0] , obuff, (size_t)(left> (ssize_t)sizeof(obuff))  ? sizeof(obuff) : left ); 
					 if(rr <= 0 ){
						 printf("9\n");
						 erex();
					 }
					 if(write_all(out_fd, obuff, (size_t)rr) <  0){
						 printf("10\n");
							erex();
					 }
					 left -= rr;
				}
			}
			break;
		}
		buff[used++]= ch;
		if(used > MAX_CHARS_IN_LINE){
			printf("11\n");
			erex();
		}
		if(ch == '\n') {
			char lenbuff[32]; 
				int m = sprintf(lenbuff, "%d\n", (int)used);
                                if(m <= 0){
					printf("12\n");
				erex();
				}
                                if(write_all(p2c[1], lenbuff, (size_t)m ) < 0){
					printf("13\n");
					erex();
				}
                                if(write_all(p2c[1], buff, (size_t)used ) < 0){
					printf("14\n");	
					erex();
				}
                                ssize_t left = used;
                                while(left > 0){
                                        ssize_t rr = read(c2p[0] , obuff, (size_t)(left> (ssize_t)sizeof(obuff))  ? sizeof(obuff) : left );
                                         if(rr <= 0 ){
						 printf("15\n");
						 erex();
					 }
                                         if(write_all(out_fd, obuff, (size_t)rr) <  0){
						 printf("16\n");
						 erex();
					 }
                                         left -= rr;
                                }
				used = 0;
		}
	}
	close(p2c[1]); 
	for(;;){
		ssize_t rr = read(c2p[0] , obuff , sizeof(obuff));
		if(rr < 0 ){
			printf("17\n");
			erex();
		}
		if(rr == 0) break;
		if(write_all(out_fd, obuff, (size_t)rr) <  0){
			printf("18\n");
			erex();
		}
	}
	close(c2p[0]);
	if(close(in_fd) < 0) {
		printf("19\n");
		erex();
	}
	if(close(out_fd) < 0) {
	printf("20\n");
	erex();
	}

	return 0;
}

