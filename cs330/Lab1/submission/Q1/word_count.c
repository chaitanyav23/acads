#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <assert.h>
#include <unistd.h>

// Use Library function such as fopen, geline, fread etc
// use manpages as mentioned in the writeup. 
// -----------------------
//
//
// Your solution begins here
int main(int argc, char *argv[]) {
	   FILE *stream;
           char *line = NULL;
           size_t len = 0;
           ssize_t nread;
/*           if (argc != 3) {
               fprintf(stderr, "Usage: %s <file>\n", argv[0]);
          	exit(EXIT_FAILURE);
           }*/

           stream = fopen(argv[2], "r");
           if (stream == NULL) {
               perror("fopen");
               exit(EXIT_FAILURE);
           }

	   int word_c = 0;
	   int line_c = 0;
	   int total_chars = 0;
                while ((nread = getline(&line, &len, stream)) != -1) {
//			if(!strcmp(line, "\n") == 0) continue;
                        total_chars += nread;
			line_c++;

                        int in_word = 0;
                        for(int i = 0; i < nread; i++) {
                                if(isspace((unsigned char)line[i])) in_word = 0;
                                else if (!in_word) {
                                        in_word = 1;
                                        word_c++;
                                }
                        }
                }


	   char *argptr = argv[1];
	   if(strcmp(argptr, "-c")==0) {
		printf("%d\n", total_chars);
	   }
	   else if (strcmp(argptr, "-w")==0){
		
		printf("%d\n", word_c);
	   }

	   else if(strcmp(argptr, "-l")==0){
		printf("%d\n", line_c);
	   }
	   else exit("-1");
	   free(line);
           fclose(stream);
           exit(EXIT_SUCCESS);

	return 0;
}
