#include<context.h>
#include<page.h>
#include<memory.h>
#include<lib.h>


//////////////////////  Q1: RR Scheduling   ///////////////////////////////////////
//args:next 
//      ctx: new exec_context to be added in the linked list
void rr_add_context(struct exec_context *ctx)
{
      /*TODO*/
	if(rr_list_head == NULL){
		rr_list_head = ctx;
		rr_list_head->next = NULL;
		return;
	}
	struct exec_context *temp = rr_list_head;
	while(temp->next != NULL){
		temp = temp->next;
	}
	temp->next = ctx;
	temp= temp->next; temp->next = NULL;
       return;
}

//args:
//      ctx: exec_context to be removed from the linked list
void rr_remove_context(struct exec_context *ctx)
{
      /*TODO*/
	if(rr_list_head == ctx){
	       rr_list_head = rr_list_head->next;
       		return;
	}

	struct exec_context *temp = rr_list_head;
	while(temp->next != ctx){
		temp = temp->next;
	}	
	
	temp->next = temp->next->next;
      return;
}

//args:
//      ctx: exec_context corresponding the currently running process
struct exec_context *rr_pick_next_context(struct exec_context *ctx)
{
    /*TODO*/
	if(ctx->pid == 0){
		if(rr_list_head != NULL){
			return rr_list_head;
		} else {
			return ctx;
		}
	}
	
	if(ctx->next != NULL){
		return ctx->next;
	} else {
		if(rr_list_head == NULL){
			return get_ctx_by_pid(0);
		}
		return rr_list_head;
	}
     return get_ctx_by_pid(0);
}

//////////////////////  Q2: Get the PAGE TABLE details for given address   ///////////////////////////////////////


//args:
//      ctx: exec_context corresponding the currently running process
//      addr: address for which the PAGE TABLE details are to be printed

int do_walk_pt(struct exec_context *ctx, unsigned long addr)
{
    u64 *vaddr_base = (u64 *)osmap(ctx->pgd);
    /*TODO*/
	u64* vaddr = vaddr_base + ((addr & PGD_MASK) >> PGD_SHIFT);
	if(((*vaddr)&1) == 0)
	{
		for(int i=1;i<=4;i++) printk("No L%d entry\n",i);
		return -1;
	}
	printk("L1-entry addr: %x, ",vaddr);
	printk("L1-entry contents: %x, ",*vaddr);
	printk("PFN: %x, ",*vaddr >> 12);
	printk("Flags: %x\n",*vaddr & 0xFFF);
	
	vaddr = osmap(((*vaddr) >> 12) & 0xFFFFFFFF) + (((addr & PUD_MASK) >> PUD_SHIFT) << 3);
	if(((*vaddr)&1) == 0)
	{
		for(int i=2;i<=4;i++) printk("No L%d entry\n",i);
		return -1;
	}
	printk("L2-entry addr: %x, ",vaddr);
	printk("L2-entry contents: %x, ",*vaddr);
	printk("PFN: %x, ",*vaddr >> 12);
	printk("Flags: %x\n",*vaddr & 0xFFF);
	
	vaddr = osmap(((*vaddr) >> 12) & 0xFFFFFFFF) + (((addr & PMD_MASK) >> PMD_SHIFT) << 3);
	if(((*vaddr)&1) == 0)
	{
		for(int i=3;i<=4;i++) printk("No L%d entry\n",i);
		return -1;
	}
	printk("L3-entry addr: %x, ",vaddr);
	printk("L3-entry contents: %x, ",*vaddr);
	printk("PFN: %x, ",*vaddr >> 12);
	printk("Flags: %x\n",*vaddr & 0xFFF);
	

	vaddr = osmap(((*vaddr) >> 12) & 0xFFFFFFFF) + (((addr & PTE_MASK) >> PTE_SHIFT) << 3);
	if(((*vaddr)&1) == 0)
	{
		for(int i=4;i<=4;i++) printk("No L%d entry\n",i);
		return -1;
	}
	printk("L4-entry addr: %x, ",vaddr);
	printk("L4-entry contents: %x, ",*vaddr);
	printk("PFN: %x, ",*vaddr >> 12);
	printk("Flags: %x\n",*vaddr & 0xFFF);
	
return 0;

}

