#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

void compact(void *start, void *end)
{
  /* 
   * TODO
   * Your code goes here
   */
	char *src = (char *)start;
	char *dst = (char *)start;
	char *finish = (char *)end;
	for(; src < finish; src++) {
		if(*src != '\0') {
			*dst = *src;
			dst ++;
		}
	}
	void *new_end = dst;
	void *cur_end = sbrk(0);
	if(new_end  < cur_end) {
		sbrk((char *)new_end - (char *)cur_end);
	}

  return;    
}
