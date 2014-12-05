#include <stdio.h>
#include <stddef.h>

extern char _binary_dicmap_bin_start;
extern char _binary_dicmap_bin_end;

int print1()
{
    char *bin_start = &_binary_dicmap_bin_start;
    char *bin_end = &_binary_dicmap_bin_end;

    fprintf(stderr, "print1\n");
    fprintf(stderr,"%x => %x\n", &_binary_dicmap_bin_start, &_binary_dicmap_bin_end);
    fprintf(stderr, "%x => %x\n", bin_start, bin_end);

    char* t1 = &_binary_dicmap_bin_start;
    char* t2 = &_binary_dicmap_bin_end;
    fprintf(stderr, "%x => %x\n", t1, t2);

    return 0;
}
