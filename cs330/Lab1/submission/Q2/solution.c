#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "buffer_api.h"


int main(int argc, char* argv[]) {
	if(argc != 2){
		perror("usage: ./solution <testcase number>");
		return -1;
	}
	buffer_init(atoi(argv[1]));
	const struct ring_buffer *rb = buffer_get_base();
	int testcase = atoi(argv[1]);

	uint64_t pos = rb-> data_tail;
	uint64_t end = rb-> data_head; 
	uint64_t buf_size = rb-> data_size;
	uint64_t total_lost = 0;
	uint64_t unknown_size = 0; 

	// start reading at base + (start % size)
	// end reading at base + (end % siz
	//
	while(pos < end){
		void * event_ptr = (char*) rb-> data_base + (pos%buf_size);

		struct perf_event_header *hdr =(struct perf_event_header*) event_ptr;

		if(hdr->type == PERF_RECORD_SAMPLE){
			struct sample_event *se = (struct sample_event*)event_ptr;
//			puts("sample");
			printf("%p\n", se->addr); // to print sample addresses
		}
		else if(hdr->type == PERF_RECORD_LOST){
			struct lost_event *le = (struct lost_event*) event_ptr;
			total_lost += le->lost;
//			puts("lost");
		}
		else{
			unknown_size += hdr->size;
//			puts("lost");
		}
		pos +=hdr->size;
//		puts("loop");
	}
	//pos += hdr->size;
//	printf("%lu\n", total_lost);
//	printf("%lu\n", unknown_size);
	//	const struct sample_event *sam = 
	/* ------ YOUR CODE ENDS HERE ------*/

	/* print formats */
	 printf("number of lost records: %lu\n",total_lost );
	 printf("unknown size: %lu\n", unknown_size);

	/* ------ YOUR CODE ENDS HERE ------*/
	buffer_exit();
	return 0;
}
